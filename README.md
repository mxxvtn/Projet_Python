# France Demographic Analyzer

Application d'analyse démographique française utilisant Streamlit et l'API Geo Gouv.

## Installation

1. Créer un environnement virtuel :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate  # Windows
   ```

2. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

## Démarrage

Lancer l'application Streamlit :
```bash
streamlit run src/app.py
```

## Structure

- `src/api`: Clients pour les API externes
- `src/models`: Modèles de données
- `src/cache`: Gestion du cache
- `src/visualization`: Fonctions de visualisation (cartes, graphiques)
- `tests`: Tests unitaires
