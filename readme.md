# Visualisations Visées

## Comparaison du coût des médicaments VS la prévalence de ce qu'ils soignent dans la population Française

L'objectif est de voir si les maladies les plus fréquentes sont celles qui coûtent le plus cher à la sécurité sociale.
### Types de visualisations

- Nuage de points avec prévalence en x et cout en y (ou vice versa)
### Détails d'implémentation

- Données : Aggrégation par pathologie ou ATC.
- Axe X : Prévalence (Nombre de patients traités ou Nombre de boîtes vendues).
- Axe Y : Coût Total Remboursé (€).
- Taille du point : Coût unitaire moyen du traitement.
- Couleur : Grande catégorie de maladie.
- Tooltip : Nom de la pathologie, Coût total, Nb Patients.
## Evolution de la somme du nombre de boites ET de la somme du coût total des remboursements ET somme cout / somme boites VS évolution de la population Française sur tout le dataset

L'objectif est de voir comment évolue les consommations de médicaments / les dépenses en santé selon l'évolution de la population française, à voir si intéressant par département
### Type de visualisations

- Line Graph avec toutes les valeurs, trouver un moyen de représenter correctement les différences entre ce qu'on plot et la pop
### Détails d'implémentation

- Axe X : Temps (Années/Mois).
- Axe Y : Indice d'évolution (Base 100).
- Courbes (Lignes) :
    - Somme du nombre de boîtes.
    - Somme du coût total remboursé.
    - Coût moyen (Somme coût / Somme boîtes).
    - Population Française totale.
    

## Maladie la plus traîtée par région

L'objectif est simplement de visualiser le medicament le plus remboursé (nb boites) par région (et la pathologie associée), à voir si clique sur une région affiche un top en graph barre

### Type de Visualisations

- Choropleth avec la maladie par région
### Détails d'implémentation

- Catégorie la plus présente par région
    - Couleur : Maladie traitée
    - Métrique : Volume de vente
    

## Pour un médicament, évolution du prix au cours des années + évolution du nombre de boites vendues

L'objectif est de suivre l'évolution du prix au niveau d'un seul médicament au cours des années

### Type de Visualisation

- Line Graph avec année en X et prix en y
### Détails d'implémentation

- Input : L'utilisateur choisit un médicament.
- Axe X : Temps (Années).
- Axe Y de Gauche (Barres) : Nombre de boîtes vendues (Volume).
- Axe Y de Droite (Ligne) : Prix unitaire ou Base de Remboursement.
- Insight : Permet de voir si une baisse du prix de remboursement corrèle avec une hausse des volumes.
## Médicament préféré des Français par catégorie / Catégorie préféré des Français

On cherche ici à voir les médcaments les plus consommés par les français.

### Type de Visualisation

- Choropleth 
### Détails d'implémentation

- Niveau 1: "Catégorie préférée des Français par région".
    - Couleur : Classe ATC niveau 1 (ex: Système Nerveux, Système Digestif).
    - Métrique : Plus gros volume de vente par région.
- Niveau 2: "Médicament préféré".
    - Couleur : Soit une échelle de chaleur (Heatmap) montrant la concentration de consommation d'un médicament spécifique, soit une carte catégorielle du "Top 1 médicament" par région.

- Diagramme en barre
