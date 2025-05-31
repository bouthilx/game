# Jeux Papa - Documentation

Bienvenue dans la documentation du projet **Jeux Papa**, un RPG 2D développé en Python avec Pygame.

## Vue d'ensemble

Jeux Papa est un jeu de rôle 2D dans lequel le joueur explore un monde ouvert, combat des ennemis, collecte de l'équipement et progresse dans un système d'expérience classique.

## Sections de Documentation

### 🎮 [Design](design/index.md)
Spécifications complètes du design du jeu, incluant les mécaniques de gameplay, les systèmes de combat, et les concepts d'environnement.

### 🔧 [API](api/index.md)
Documentation technique de l'architecture du code, des classes principales et des systèmes de base.

## Architecture Technique

- **Moteur**: Pygame avec architecture personnalisée
- **Style**: RPG 2D vue du dessus
- **Rendu**: Système de tuiles 32x32 pixels
- **Maps**: Format bitmap PNG pour définir les terrains
- **Tests**: Couverture >97% avec pytest

## Démarrage Rapide

```bash
# Installer les dépendances
uv sync

# Lancer le jeu
python main.py

# Tests
uv run pytest

# Documentation
uv run --group docs mkdocs serve
```