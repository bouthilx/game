# Directives de Conception du Jeu

## **Specifications du Joueur Principal**

### **Systeme de Combat**
- **Types d'Attaque**: Melee (epee), a distance (magie), capacites speciales
- **Statistiques**: Vie, force, defense, vitesse
- **Equipement**: Armes, armures (entière) avec défense et/ou resistances thermiques, accessoires avec modificateurs de stats (colliers et bagues)
- **Capacites**: Competences debloquables par niveau (guerison, dash, attaques de zone) avec points d'expérience. Dans certain coffre il va y avoir des parchemins pour apprendre des capacités.

### **Amelioration Visuelle**
- **Animation de Sprite**: Cycles de marche, animations d'attaque, etats d'inactivite
- **Visuels d'Equipement**: Changements visuels selon l'equipement porte
- **Effets de Statut**: Indicateurs visuels (icone, pas de modification du personnage) pour les buffs/debuffs

### **Systeme de Progression**
- **Arbres de Competences**: Branches combat, magie, survie
- **Inventaire**: Collection d'objets, gestion d'equipement
- **Quetes**: Objectifs et progression de l'histoire

## **Specifications des Ennemis**

### **Types d'Ennemis** (correspondant a vos sprites disponibles)
- **Gobelins**: Rapides, peu de vie, tactiques d'essaim
- **Gardes**: Stats moyennes, patterns de patrouille autour des batiments
- **Betes**: Beaucoup de vie, lents, territoriaux autour des arbres/zones naturelles
- **Boss**: Capacites uniques, combats multi-phases

### **Comportements IA**
- **IA de Patrouille**: Mouvement base sur des routes entre points de passage
- **IA de Poursuite**: Poursuite quand le joueur entre dans le rayon de detection
- **IA de Combat**: Patterns d'attaque, conditions de retraite, coordination de groupe
- **Machine d'Etat**: Etats Inactif → Alerte → Poursuite → Attaque → Retour

## **Mecaniques de Jeu Principales**

### **Systeme de Combat**
- Combat **temps reel** 
- **Types de Degats**: un seul type
- **Effets de Statut**: Poison, etourdissement, bouclier, hypothermie, surchauffe
- **Butin**: Experience, or, equipement des ennemis vaincus (épées, bombes, shurikens)

### **Interaction avec le Monde**
- **Coffres**: Contenants de butin prédéterminé.
- **PNJ**: Donneurs de quetes, marchands, personnages d'histoire
- **Objets Interactifs**: Leviers, portes, blocs qu'on peut pousser ou tirer, interrupteurs pour puzzles
- **Dangers Environnementaux**: Pieges, zones empoisonnees, plateformes mobiles

### **Progression du Jeu**
- **Cartes Multiples**: Zones connectees avec differents themes/difficultes
- **Systeme de Quetes**: Histoire principale + quetes secondaires avec recompenses
- **Systeme de Sauvegarde**: Persistance des progres entre sessions. Sauvegarde automatique et par le menu.
- **Adaptation de Difficulte**: Stats ennemies evoluent avec niveau joueur.

## **Notes d'Architecture**

Votre architecture actuelle supporte bien tous ces ajouts. Le systeme d'entites peut facilement s'etendre aux ennemis, le systeme de carte gere les zones multiples, et la base des stats RPG est deja en place.