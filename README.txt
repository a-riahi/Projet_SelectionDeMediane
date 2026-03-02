PROJET SELECTIONMEDIANE - DEMONSTRATEUR
BINOME : GAOUAOUI Amine, RIAHI Mohamed Ayoub


================================================================================
DESCRIPTION
================================================================================

Ce projet implémente et compare différents algorithmes de sélection pour trouver la médiane d'un array avec une interface graphique interactive qui permet de visualiser les étapes de comparaison en temps réel.

Algorithmes implémentés :
- Quickselect : Algorithme de sélection rapide randomisé
- Médiane Probabiliste : Algorithme probabiliste moderne
- Tri complet : Méthode de référence pour vérification

================================================================================
UTILISATION
================================================================================

Interface Graphique Interactive

Lancez le démonstrateur avec :
    python main.py

Une fenêtre graphique s'ouvre avec les fonctionnalités suivantes :

Configuration du Tableau
- Taille du tableau : Choisissez la taille (1-1000 éléments)
- Mode tableau :
  - Aléatoire : Génération automatique d'un tableau aléatoire
  - Manuel : Entrez votre propre tableau (format: 1,2,3,4,5 ou 1 2 3 4 5)
  - Bouton "Générer" : Génère un tableau aléatoire et l'affiche

Configuration des Pivots (Quickselect)
- Mode aléatoire : Les pivots sont choisis aléatoirement (par défaut)
- Mode manuel : Spécifiez les pivots à utiliser (un par niveau récursif)
  - Format: pivot1,pivot2,pivot3,...

Position k
- Position recherchée : Entrez la position k (optionnel, médiane par défaut)

Navigation dans les Étapes
- Boutons Précédent/Suivant : Naviguez entre les étapes
- Mode Auto : Parcourt automatiquement toutes les étapes
- Affichage persistant : Toutes les étapes restent visibles et s'accumulent
- Mise en évidence : L'étape courante est mise en évidence avec une bordure

Visualisation
- Tableaux à chaque étape : Visualisez les tableaux originaux, partitions, pivots, etc.
  - Affichage en grille colorée pour une meilleure lisibilité (jusqu'à 25 éléments par ligne)
  - Couleurs différentes selon le type de tableau (original, gauche, droite, etc.)
  - Scrollbar pour les grands tableaux
  - Interface optimisée pour utiliser toute la largeur disponible (fenêtre 1600x800)
- Opérations détaillées : Voir toutes les comparaisons et opérations effectuées
- Statistiques : Nombre de comparaisons, temps d'exécution, résultat
- Comparaison côte à côte : Comparez les deux algorithmes directement
- Affichage amélioré : Frames d'étapes avec style moderne, mise en évidence de l'étape courante

Affichage Terminal
- Résultats dans le terminal : Tous les résultats sont également affichés dans la console
- Tableaux formatés : Les tableaux sont affichés de manière lisible dans le terminal
- Étapes détaillées : Chaque étape avec ses tableaux est visible dans le terminal
- Comparaison côte à côte : Comparaison des deux algorithmes dans le terminal

================================================================================
STRUCTURE DU PROJET (ARCHITECTURE MVC)
================================================================================

Le projet suit le pattern Model-View-Controller (MVC) pour une séparation claire des responsabilités :

SelectionMediane/
├── models/               # MODEL: Logique métier
│   ├── __init__.py
│   └── model.py         # Classe SelectionModel avec les algorithmes
├── views/                # VIEW: Interfaces utilisateur
│   ├── __init__.py
│   ├── view.py          # Interface console (SelectionView)
│   └── graphical_view.py # Interface graphique (GraphicalView)
├── controllers/          # CONTROLLER: Coordination MVC
│   ├── __init__.py
│   └── controller.py    # SelectionController
├── utils/                # Utilitaires réutilisables
│   ├── __init__.py
│   ├── utils.py         # Génération de données, mesure de performance
│   └── pivot_selector.py # Gestion des pivots personnalisés
├── main.py               # Point d'entrée principal
├── test.py               # Suite de tests complète
└── README.md             # Ce fichier

Architecture MVC

- Model (models/model.py) : Contient la logique métier pure (algorithmes Quickselect et Médiane Probabiliste)
- View (views/view.py, views/graphical_view.py) : Gère uniquement l'affichage (console et graphique)
- Controller (controllers/controller.py) : Coordonne le Model et les Views, ne contient pas de logique métier
- Utils (utils/utils.py, utils/pivot_selector.py) : Fonctions utilitaires réutilisables (génération de données, mesure de performance)

Chaque module est organisé dans son propre dossier avec un fichier __init__.py pour faciliter les imports.

================================================================================
ALGORITHMES IMPLEMENTES
================================================================================

1. Quickselect
- Type : Randomisé
- Complexité : O(n) en moyenne, O(n²) dans le pire cas
- Avantages : Simple, efficace en pratique
- Fonctionnalités :
  - Pivot aléatoire par défaut
  - Possibilité de spécifier des pivots personnalisés
  - Affichage détaillé de chaque partition

2. Médiane Probabiliste
- Type : Probabiliste
- Complexité : O(n) en moyenne
- Avantages : Performance théorique intéressante
- Inconvénients : Peut échouer (retourne "ECHEC")
- Fallback : Utilise Quickselect en cas d'échec
- Étapes détaillées :
  - Échantillonnage de R
  - Tri de R et calcul des bornes a et b
  - Parcours et partition
  - Vérifications et tri final

3. Tri Complet
- Type : Déterministe
- Complexité : O(n log n)
- Usage : Référence pour vérification des résultats

================================================================================
FONCTIONNALITES DE L'INTERFACE GRAPHIQUE
================================================================================

Affichage des Étapes
- Étapes persistantes : Toutes les étapes restent affichées et s'accumulent
- Navigation intuitive : Boutons Précédent/Suivant pour parcourir les étapes
- Mise en évidence : L'étape courante est mise en évidence avec une bordure épaisse
- Défilement automatique : L'interface défile automatiquement vers l'étape courante

Visualisation des Tableaux
- Tableaux originaux : Voir le tableau initial à chaque étape
- Partitions : Visualiser les partitions (gauche, égal, droite) pour Quickselect
- Pivots et bornes : Afficher les pivots sélectionnés et les bornes a et b
- Échantillons : Voir les échantillons R et partitions P pour la médiane probabiliste
- Affichage adaptatif : Les grands tableaux sont tronqués intelligemment

Statistiques en Temps Réel
- Comparaisons : Nombre total de comparaisons effectuées
- Comparaisons par étape : Détail des comparaisons à chaque étape
- Temps d'exécution : Temps réel d'exécution de l'algorithme
- Résultat : Valeur trouvée et vérification

================================================================================
TESTS
================================================================================

Exécution des tests
    python test.py

Le fichier test.py inclut :
1. Tests sur petits arrays (1-10 éléments)
2. Tests sur arrays moyens (50-500 éléments)
3. Tests sur grands arrays (1000-5000 éléments)
4. Tests des cas limites :
   - Premier/dernier élément
   - Arrays avec doublons
   - Arrays triés/décroissants
5. Comparaison de performance

================================================================================
COMPARAISON GRAPHIQUE
================================================================================

Le programme peut générer des graphiques de comparaison (via compare_growth()) :
- Nombre d'étapes vs taille d'array
- Temps d'exécution vs taille d'array
- Performance relative des algorithmes

================================================================================
CAS D'ECHEC DE L'ALGORITHME PROBABILISTE
================================================================================

L'algorithme probabiliste peut retourner "ECHEC" dans ces cas :
- Arrays très petits (< 10 éléments)
- Arrays avec beaucoup de doublons
- Cas où la partition est trop grande
- Conditions de cohérence non respectées

Le système de fallback garantit qu'un résultat sera toujours retourné en utilisant Quickselect.

================================================================================
DEPENDANCES
================================================================================

- Python 3.6+
- tkinter : Interface graphique (généralement inclus avec Python)
- matplotlib : Pour les graphiques de comparaison
- Modules standards : random, math, time

================================================================================
EXEMPLES D'UTILISATION
================================================================================

Exemple 1 : Tableau personnalisé
1. Lancez python main.py
2. Choisissez "Manuel" pour le tableau
3. Entrez : 10,5,8,3,1,9,2,7,4,6
4. Laissez k vide (médiane par défaut)
5. Cliquez sur "▶ Lancer la démonstration"

Exemple 2 : Pivots personnalisés
1. Choisissez un tableau (aléatoire ou manuel)
2. Sélectionnez "Manuel" pour les pivots
3. Entrez : 5,3,1 (pour 3 niveaux récursifs)
4. Lancez la démonstration

Exemple 3 : Navigation dans les étapes
1. Lancez une démonstration
2. Utilisez "Suivant ▶" pour voir chaque étape
3. Toutes les étapes précédentes restent visibles
4. Utilisez "▶▶ Auto" pour un parcours automatique

================================================================================
UTILISATION RECOMMANDEE
================================================================================

1. Apprentissage : Utilisez l'interface graphique pour comprendre le fonctionnement des algorithmes
2. Développement : Utilisez test.py pour vérifier les modifications
3. Démonstration : Parfait pour présenter les algorithmes visuellement
4. Recherche : Testez différents tableaux et pivots pour analyser les performances

================================================================================
NOTES
================================================================================

- L'interface graphique permet de visualiser jusqu'à 1000 éléments
- Fenêtre principale : 1600x800 pixels pour une meilleure utilisation de l'espace
- Pour les grands tableaux, l'affichage est optimisé (troncature intelligente)
- Les pivots personnalisés doivent être présents dans le tableau courant
- Le mode auto parcourt les étapes toutes les 2 secondes (ajustable)
- Affichage des tableaux : jusqu'à 25 éléments par ligne pour une meilleure lisibilité

================================================================================

Projet SelectionMediane - Démonstrateur interactif avec visualisation des étapes de comparaison

