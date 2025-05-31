# Système d'Ennemis

Le système d'ennemis offre une variété de défis adaptés aux différentes zones et niveaux de progression du joueur.

## Types d'Ennemis

### Gobelins
- **Caractéristiques**: Rapides, peu de points de vie
- **Tactiques**: Attaques en essaim, harcèlement
- **Zones**: Forêts, grottes, zones débutantes
- **Butin**: Expérience de base, petites armes

### Gardes
- **Caractéristiques**: Statistiques équilibrées
- **Tactiques**: Patrouilles organisées, défense territoriale
- **Zones**: Autour des bâtiments, villages, avant-postes
- **Butin**: Équipement militaire, or

### Bêtes
- **Caractéristiques**: Beaucoup de vie, déplacements lents
- **Tactiques**: Attaques puissantes, comportement territorial
- **Zones**: Forêts denses, autour des arbres
- **Butin**: Matériaux rares, objets de survie

### Boss
- **Caractéristiques**: Capacités uniques, très résistants
- **Tactiques**: Combats multi-phases, patterns complexes
- **Zones**: Fins de donjons, zones spéciales
- **Butin**: Équipement légendaire, progression d'histoire

## Système d'Intelligence Artificielle

### Machine d'États
Tous les ennemis suivent le cycle d'états suivant:
```
Inactif → Alerte → Poursuite → Attaque → Retour
```

### Comportements Détaillés

#### État Inactif
- **Patrouille**: Mouvement entre points définis
- **Détection passive**: Surveillance de zone limitée
- **Animations**: Mouvements d'attente réalistes

#### État Alerte
- **Détection**: Joueur entré dans rayon de perception
- **Investigation**: Mouvement vers dernière position connue
- **Transition**: Vers poursuite si contact confirmé

#### État Poursuite
- **Traque**: Mouvement direct vers le joueur
- **Persistance**: Continue même si joueur sort du champ
- **Vitesse**: Adaptée au type d'ennemi

#### État Attaque
- **Engagement**: Combat direct avec le joueur
- **Patterns**: Séquences d'attaques spécifiques
- **Coordination**: Avec autres ennemis si applicable

#### État Retour
- **Désengagement**: Joueur hors de portée ou fui
- **Retour**: Vers position ou patrouille initiale
- **Réinitialisation**: Récupération des points de vie

## Patterns d'Attaque

### Attaques de Base
- **Contact direct**: Dégâts au toucher
- **Projectiles**: Attaques à distance
- **Zones d'effet**: Attaques affectant une aire

### Coordination de Groupe
- **Encerclement**: Positionnement tactique
- **Attaques combinées**: Séquences synchronisées
- **Rôles spécialisés**: Attaquants et soutiens

## Adaptation et Difficulté

### Évolution avec le Joueur
- **Statistiques**: Augmentent avec le niveau du joueur
- **Nouvelles capacités**: Déblocage progressif
- **Zones avancées**: Ennemis plus sophistiqués

### Conditions de Retraite
- **Seuil de vie**: Fuite si blessés gravement
- **Supériorité numérique**: Retraite si seuls
- **Zones de sécurité**: Retour vers alliés