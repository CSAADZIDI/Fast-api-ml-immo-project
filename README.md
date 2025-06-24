# Prédiction du prix au m² en immobilier en France

## Contexte

Une agence immobilière souhaite intégrer un outil d’estimation automatique du **prix au m²** dans ses applications internes. L’objectif est de mieux appuyer les décisions commerciales sur le marché immobilier des villes de **Lille** et **Bordeaux**, en s’appuyant sur les données publiques de transactions immobilières.

## Démarche 

### Phase 0 : Préparation des Données de valeur foncière (DVF) 
Nettoyage des données DVF 2022 pour Lille et Bordeaux afin de préparer l'analyse.

Étapes :

Chargement du fichier brut (format .txt, séparateur |)

Filtrage : ventes à Lille ou Bordeaux avec surface bâtie et valeur foncière non nulles

Conversion des valeurs en float

Calcul du prix au m²

Export des jeux de données nettoyés :

data/lille_2022.csv

data/bordeaux_2022.csv