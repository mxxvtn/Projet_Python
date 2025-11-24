# Rapport de Projet - France Demographic Analyzer

## 1. Architecture et Choix Techniques

### Architecture
Le projet suit une architecture modulaire classique pour une application Python :
- **src/api** : Contient la logique de communication avec les APIs externes (`geo.api.gouv.fr`).
- **src/models** : Définit les structures de données (modèles Pydantic) pour assurer la validation et le typage des données.
- **src/cache** : Gère le cache des requêtes API pour optimiser les performances et limiter les appels réseau.
- **src/visualization** : Contient la logique de génération des cartes (Folium).
- **src/app.py** : Le point d'entrée de l'application Streamlit, gérant l'interface utilisateur et l'orchestration des composants.

### Choix Techniques

1.  **Streamlit** : Choisi pour sa rapidité de développement d'interfaces web de data science interactives. Il permet de créer des dashboards rapidement sans connaissances approfondies en frontend (HTML/CSS/JS).
2.  **Pydantic** : Utilisé pour la modélisation des données. Cela garantit que les données reçues de l'API respectent le format attendu et facilite la manipulation des objets (ex: calcul de densité).
3.  **Requests-Cache** : Une solution simple et efficace pour le caching HTTP. Elle permet de stocker les réponses de l'API Geo dans une base SQLite locale, réduisant la latence et la charge sur l'API publique.
4.  **Folium & Streamlit-Folium** : Folium est la bibliothèque standard pour créer des cartes Leaflet en Python. Streamlit-Folium permet d'intégrer ces cartes directement dans l'application Streamlit.
5.  **Plotly Express** : Utilisé pour les graphiques interactifs (scatter plots, bar charts) car il s'intègre parfaitement avec Streamlit et offre une bonne expérience utilisateur.
6.  **Geo API Gouv** : Une API publique fiable et gratuite ne nécessitant pas de clé API complexe, idéale pour ce type de démonstration.

## 2. Analyse de l'Utilisation de l'IA

L'IA a été utilisée comme un assistant de développement complet (Full Stack Developer Assistant).

### Exemples de Prompts (Synthèse)
*Voir `PROMPTS.md` pour le détail complet.*

- **Initialisation** : "Créer une application qui analyse les données démographiques françaises..." -> Ce prompt a défini le périmètre et les fonctionnalités attendues.
- **Planification** : L'IA a généré un plan d'action structuré (Models, API, Viz, App, Tests).
- **Génération de Code** : L'IA a généré le code pour chaque module (`geo_api.py`, `commune.py`, `app.py`).

### Rôle de l'IA
- **Architecte** : Proposition de la structure des dossiers.
- **Codeur** : Écriture du code Python (Pydantic, Streamlit, API requests).
- **Testeur** : Écriture des tests unitaires `pytest`.
- **Débuggeur** : Identification des problèmes d'environnement (installation des dépendances manquantes, `ModuleNotFoundError`).

## 3. Difficultés Rencontrées et Résolutions

### Problème d'Environnement Python
**Difficulté** : Lors de l'exécution des tests, `pytest` ne trouvait pas le module `requests` alors qu'il semblait installé.
**Analyse** : Il y avait une divergence entre l'environnement où `pip install` a été exécuté et celui où `pytest` était lancé (commande `pytest` vs `python3 -m pytest`).
**Résolution** : Utilisation de `python3 -m pytest` pour garantir l'utilisation du même interpréteur Python que celui où les paquets ont été installés.

### Gestion des Données Manquantes
**Difficulté** : Certaines communes peuvent ne pas avoir de données de population ou de surface complètes.
**Résolution** : Utilisation de champs optionnels dans le modèle Pydantic (`Optional`) et gestion des valeurs par défaut (0) lors du calcul de la densité pour éviter les erreurs de division par zéro.

### Performance de la Carte
**Difficulté** : Afficher toutes les communes de France (~35 000) sur une carte Folium rendrait l'application très lente.
**Résolution** : Mise en place d'une limitation aux 500 communes les plus peuplées lors de l'affichage global, et utilisation du clustering de marqueurs (`MarkerCluster`) pour améliorer la lisibilité.

## 4. Apprentissages

- **Streamlit** : J'ai renforcé ma compréhension de la gestion de l'état et de la mise en page (tabs, sidebar) dans Streamlit.
- **Pydantic** : L'utilisation de `Field(alias=...)` ou de validateurs personnalisés (ici via `@property`) est très puissante pour nettoyer les données à la source.
- **Intégration Continue** : L'importance de vérifier l'environnement d'exécution (chemins, versions de python) est cruciale, surtout dans des environnements conteneurisés ou scriptés.
