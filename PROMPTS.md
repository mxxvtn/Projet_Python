# Journal des Prompts

## Prompt Initial

**Objectif** : Créer une application qui analyse les données démographiques françaises en temps réel via des API publiques, permettant des recherches avancées, des comparaisons entre communes/départements, et des visualisations cartographiques.

**Sources des données (APIs publiques)** :
- API Geo : https://geo.api.gouv.fr/ (communes, départements, régions, codes postaux)
- API données démographiques INSEE : https://api.insee.fr/ ou data.gouv.fr
- Alternative : https://www.data.gouv.fr/fr/datasets/base-officielle-descodes-postaux/

**Fonctionnalités à implémenter** :
- **Fonctionnalités de base** :
    - Recherche de communes par nom, code postal ou population
    - Affichage des informations : population, département, région, coordonnées GPS
    - Classement des communes par taille de population
    - Filtrage multi-critères (population min/max, département, région)
- **Fonctionnalités avancées** :
    - Statistiques comparatives : Comparaison de plusieurs communes/départements
    - Visualisation cartographique : Carte interactive avec folium montrant les communes
    - Analyse de densité : Calcul et visualisation de la densité de population
    - Recherche intelligente : Suggestions automatiques, correction d’orthographe
    - Export de données: CSV, JSON ou Excel avec les résultats de recherche
    - Dashboard web: Interface Streamlit ou Flask pour explorer les données
    - Cache intelligent : Système de cache pour limiter les appels API

**Livrables** :
- Dépôt GitHub avec historique de commits clair
- PROMPTS.md : Journal complet de tous les prompts utilisés (OBLIGATOIRE)
- README.md avec documentation API et exemples d’utilisation
- Application fonctionnelle avec interface utilisateur
- Rapport (2-3 pages) documentant le projet
