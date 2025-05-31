#!/usr/bin/env python3
"""
Script d'auto-génération de documentation API

Ce script parse le code Python du projet pour extraire automatiquement:
- Classes et leurs méthodes publiques
- Docstrings et descriptions
- Signatures de méthodes
- Structure de modules

Usage:
    python scripts/generate_docs.py
"""

import ast
import os
import sys
from pathlib import Path
from typing import Dict, List, Any
import importlib.util


class DocGenerator:
    """Générateur de documentation API automatique."""
    
    def __init__(self, source_dir: str, docs_dir: str):
        self.source_dir = Path(source_dir)
        self.docs_dir = Path(docs_dir)
        self.api_sections = {
            'engine': [],
            'entities': [],
            'world': [],
            'scenes': []
        }
    
    def parse_module(self, file_path: Path) -> Dict[str, Any]:
        """Parse un fichier Python et extrait la documentation."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            module_info = {
                'file_path': str(file_path),
                'classes': [],
                'functions': [],
                'docstring': ast.get_docstring(tree) or ""
            }
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_info = self.parse_class(node)
                    module_info['classes'].append(class_info)
                elif isinstance(node, ast.FunctionDef) and not node.name.startswith('_'):
                    func_info = self.parse_function(node)
                    module_info['functions'].append(func_info)
            
            return module_info
        
        except Exception as e:
            print(f"Erreur parsing {file_path}: {e}")
            return None
    
    def parse_class(self, node: ast.ClassDef) -> Dict[str, Any]:
        """Parse une classe et ses méthodes."""
        class_info = {
            'name': node.name,
            'docstring': ast.get_docstring(node) or "",
            'methods': [],
            'properties': [],
            'base_classes': [base.id for base in node.bases if hasattr(base, 'id')]
        }
        
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                if not item.name.startswith('_') or item.name in ['__init__']:
                    method_info = self.parse_function(item)
                    method_info['is_method'] = True
                    class_info['methods'].append(method_info)
            elif isinstance(item, ast.Assign):
                # Propriétés de classe avec type hints
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        class_info['properties'].append({
                            'name': target.id,
                            'type': getattr(item, 'type_comment', 'Unknown')
                        })
        
        return class_info
    
    def parse_function(self, node: ast.FunctionDef) -> Dict[str, Any]:
        """Parse une fonction ou méthode."""
        args = []
        for arg in node.args.args:
            arg_info = {'name': arg.arg}
            if arg.annotation:
                arg_info['type'] = ast.unparse(arg.annotation)
            args.append(arg_info)
        
        return {
            'name': node.name,
            'docstring': ast.get_docstring(node) or "",
            'args': args,
            'returns': ast.unparse(node.returns) if node.returns else None,
            'is_method': False
        }
    
    def generate_class_doc(self, class_info: Dict[str, Any]) -> str:
        """Génère la documentation Markdown pour une classe."""
        doc = f"### {class_info['name']}\n\n"
        
        if class_info['base_classes']:
            doc += f"**Hérite de**: {', '.join(class_info['base_classes'])}\n\n"
        
        if class_info['docstring']:
            doc += f"{class_info['docstring']}\n\n"
        
        # Propriétés
        if class_info['properties']:
            doc += "#### Propriétés\n\n"
            for prop in class_info['properties']:
                doc += f"- **{prop['name']}**: {prop.get('type', 'Unknown')}\n"
            doc += "\n"
        
        # Méthodes
        if class_info['methods']:
            doc += "#### Méthodes\n\n"
            for method in class_info['methods']:
                doc += self.generate_method_doc(method)
        
        return doc
    
    def generate_method_doc(self, method_info: Dict[str, Any]) -> str:
        """Génère la documentation pour une méthode."""
        args_str = ", ".join([
            f"{arg['name']}: {arg.get('type', '')}" 
            for arg in method_info['args']
        ])
        
        signature = f"**{method_info['name']}**({args_str})"
        if method_info['returns']:
            signature += f" → {method_info['returns']}"
        
        doc = f"##### {signature}\n\n"
        
        if method_info['docstring']:
            doc += f"{method_info['docstring']}\n\n"
        
        return doc
    
    def scan_source_directory(self):
        """Scanne le répertoire source pour tous les fichiers Python."""
        for section in self.api_sections.keys():
            section_path = self.source_dir / section
            if section_path.exists():
                for py_file in section_path.glob("*.py"):
                    if py_file.name != "__init__.py":
                        module_info = self.parse_module(py_file)
                        if module_info and module_info['classes']:
                            self.api_sections[section].append(module_info)
    
    def update_api_docs(self):
        """Met à jour les fichiers de documentation API."""
        for section, modules in self.api_sections.items():
            if not modules:
                continue
            
            doc_file = self.docs_dir / "api" / f"{section}.md"
            
            # Lire le contenu existant jusqu'à la section auto-générée
            existing_content = ""
            if doc_file.exists():
                with open(doc_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                # Garder tout jusqu'à "## Classes Détaillées"
                for line in lines:
                    existing_content += line
                    if line.strip() == "## Classes Détaillées":
                        break
            
            # Générer nouvelle section auto
            auto_content = "\\n<!-- AUTO-GENERATED: Ne pas éditer manuellement -->\\n\\n"
            
            for module in modules:
                module_name = Path(module['file_path']).stem
                auto_content += f"### Module: {module_name}\\n\\n"
                
                if module['docstring']:
                    auto_content += f"{module['docstring']}\\n\\n"
                
                for class_info in module['classes']:
                    auto_content += self.generate_class_doc(class_info)
                
                auto_content += "---\\n\\n"
            
            # Écrire le fichier complet
            with open(doc_file, 'w', encoding='utf-8') as f:
                f.write(existing_content)
                f.write(auto_content)
            
            print(f"Documentation mise à jour: {doc_file}")
    
    def run(self):
        """Lance la génération complète de documentation."""
        print("Génération de la documentation API...")
        self.scan_source_directory()
        self.update_api_docs()
        print("Documentation générée avec succès!")


def main():
    """Point d'entrée principal."""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    source_dir = project_root / "game"
    docs_dir = project_root / "docs"
    
    if not source_dir.exists():
        print(f"Erreur: Répertoire source non trouvé: {source_dir}")
        sys.exit(1)
    
    if not docs_dir.exists():
        print(f"Erreur: Répertoire docs non trouvé: {docs_dir}")
        sys.exit(1)
    
    generator = DocGenerator(str(source_dir), str(docs_dir))
    generator.run()


if __name__ == "__main__":
    main()