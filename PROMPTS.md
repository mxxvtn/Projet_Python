# Journal des Prompts

Ce document retrace nos echanges avec l'IA pour la conception et le développement de notre application.

--- 

## Phase 1 : Fondation et strcture du code

## Prompt 1
Question : "Je suis étudiant en DEUST Infrastructures Numérique, en seconde année, et je dois créer un analyseur démographique français en Python utilisant l'API Geo Gouv. Peux-tu m'aider à mettre en place la structure de dossiers recommandée par mon énoncé (src/api, src/models, src/cache, src/visualization) et m'expliquer à quoi servira chaque dossier ?"

Réponse de l'IA : "Pour respecter ton énoncé, voici comment structurer ton projet de manière modulaire (principe de modularité):"
- src/api/ : Contiendra la logique brute d'appel aux serveurs de Geo Gouv.
- src/models/ : Contiendra tes classes Python (ex: Commune) pour transformer le JSON de l'API en objets manipulables.
- src/cache/ : Gérera la sauvegarde locale pour éviter de dépasser les quotas de l'API.
- src/visualization/ : Regroupera tout ce qui concerne l'affichage des cartes Folium.

## Prompt 2 
Question : Je veux créer un module geo_api.py pour interroger https://geo.api.gouv.fr/communes. Peux-tu me donner un exemple de fonction simple pour récupérer les informations d'une commune par son code postal ? Explique-moi comment utiliser la bibliothèque requests pour gérer les erreurs si l'API ne répond pas.

Réponse de l'IA : J'utilise requests.get pour interroger l'URL. La méthode raise_for_status() est une bonne pratique pour détecter immédiatement les erreurs réseau (404, 500)"
```python
import requests

def get_commune_by_code(code_postal):
    url = f"https://geo.api.gouv.fr/communes?codePostal={code_postal}&fields=nom,code,codesPostaux,population,codeDepartement"
    try:
        response = requests.get(url)
        response.raise_for_status() # Génère une erreur si le code HTTP n'est pas 200
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de l'appel API : {e}")
        return None
```
## Prompt 3 
Question : Le code précédent fonctionne, mais si je cherche un code postal qui n'existe pas, le programme plante. Comment puis-je ajouter une vérification pour que l'utilisateur reçoive un message d'erreur clair au lieu d'une erreur Python ?

Réponse de l'IA : Tu as raison, il faut anticiper les erreurs de saisie. Si l'utilisateur tape 99999, l'API renverra une liste vide [] sans forcément générer d'erreur de connexion. Il faut donc vérifier le contenu de la réponse avant de manipuler les données."

Code proposé (Mise à jour de geo_api.py) :
```python
def get_commune_by_code(code_postal):
    # Validation simple côté client avant l'appel
    if not code_postal.isdigit() or len(code_postal) != 5:
        print("Erreur : Le code postal doit contenir exactement 5 chiffres.")
        return None

    url = f"https://geo.api.gouv.fr/communes?codePostal={code_postal}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Vérification si la liste est vide (commune non trouvée)
        if not data:
            print(f"Aucune commune trouvée pour le code postal {code_postal}.")
            return None
            
        return data # Retourne la liste des communes
    except Exception as e:
        print(f"Erreur technique : {e}")
        return None
```
## Prompt 4
Question : Pour éviter de solliciter l'API Geo Gouv à chaque fois, je veux implémenter un cache local. Peux-tu m'expliquer le concept de mise en cache avec un fichier JSON et me proposer une classe CacheManager qui vérifie si une donnée existe localement avant de faire une requête réseau ?

Réponse de l'IA : Le cache permet de stocker les résultats sur ton disque dur. Si tu recherches 'Paris' deux fois, la deuxième fois, le programme lira le fichier cache.json au lieu de retourner sur internet.
```python
import json
import os

class CacheManager:
    def __init__(self, filename="cache/data_cache.json"):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                json.dump({}, f)

    def get(self, key):
        with open(self.filename, 'r') as f:
            data = json.load(f)
        return data.get(key)

    def set(self, key, value):
        with open(self.filename, 'r') as f:
            data = json.load(f)
        data[key] = value
        with open(self.filename, 'w') as f:
            json.dump(data, f)
```
## Prompt 5 
Question : Maintenant que mes modules API et Cache fonctionnent, je veux créer l'interface avec Streamlit dans app.py. Je veux un champ de saisie pour le code postal, un tableau affichant les données (nom, population, région) et une carte interactive avec Folium pour placer la commune. Comment puis-je lier mes fonctions existantes à l'interface Streamlit ?

Réponse de l'IA : Pour Streamlit, on utilise des 'widgets'. Voici comment lier ton champ de texte à ta fonction API :
```python
import streamlit as st
from api.geo_api import get_commune_by_code

st.title("🇫🇷 Analyseur Démographique")

cp = st.text_input("Entrez un code postal (ex: 75001)")

if cp:
    data = get_commune_by_code(cp)
    if data:
        st.success(f"Commune trouvée : {data[0]['nom']}")
        st.metric("Population", f"{data[0]['population']} habitants")
    else:
        st.error("Aucune donnée trouvée pour ce code postal.")
```
---

## Phase 2 : Optimisation 

## Prompt 6 :  

Question : Le code pour l'API fonctionne, mais c'est un peu compliqué de manipuler des listes et des dictionnaires tout le temps. Est-ce qu'on peut créer une sorte de 'modèle' dans le dossier models pour que chaque commune soit un objet bien défini ? J'aimerais aussi que le calcul de la densité se fasse tout seul dès qu'on récupère une ville, pour ne pas avoir à réécrire la formule tout le temps.

Réponse de l'IA : "Voici un modèle robuste. J'utilise une @property pour convertir la surface en $km^2$ ($1 \text{ hectare} = 0,01 \text{ km}^2$) afin de calculer la densité réelle :"
from pydantic import BaseModel, Field
from typing import List, Optional
```python
class Commune(BaseModel):
    nom: str
    code: str
    codeDepartement: Optional[str] = None
    codeRegion: Optional[str] = None
    codesPostaux: Optional[List[str]] = []
    population: Optional[int] = 0
    surface: Optional[float] = 0.0  
    centre: Optional[dict] = Field(default_factory=dict)

    @property
    def density(self) -> float:
        if self.surface and self.surface > 0 and self.population:
            surface_km2 = self.surface / 100
            return round(self.population / surface_km2, 1)
        return 0.0
```

## Prompt 7 :

Question : Mon système de cache avec le fichier JSON ( Du prompt 4) est un peu lourd. Si je cherche beaucoup de villes, j'ai peur que ça ralentisse l'application. Est-ce qu'il existe une bibliothèque Python qui gère le cache automatiquement pour les requêtes internet sans que j'aie à écrire dans un fichier à la main à chaque fois ? Quelque chose qui garderait les données un jour ou deux par exemple.

Réponse de l'IA : "Je te suggère requests-cache. C'est transparent et permet de définir une durée d'expiration. Voici comment configurer la session dans src/cache/cache_manager.py :"
```python
import requests_cache
import datetime

def get_session():
    return requests_cache.CachedSession(
        'geo_cache',
        backend='sqlite',
        expire_after=datetime.timedelta(days=1)
    )
```

## Prompt 8 : 

Question : J'ai essayé d'afficher plein de communes sur la carte Folium, mais on ne voit plus rien quand les points se superposent. Est-ce qu'on peut regrouper les points qui sont proches dans des bulles ? Et aussi, j'ai un souci : l'API me donne [Longitude, Latitude] mais ma carte affiche les villes au mauvais endroit, je crois qu'il faut inverser les deux.

Réponse de l'IA : "Il faut inverser les coordonnées car Folium attend [Lat, Lon]. Pour la lisibilité, on utilise MarkerCluster. Voici le code pour src/visualization/maps.py :"
```python
import folium
from folium.plugins import MarkerCluster

def create_map(communes):
    m = folium.Map(location=[46.6, 1.8], zoom_start=6)
    marker_cluster = MarkerCluster().add_to(m)
    for commune in communes:
        if commune.centre and 'coordinates' in commune.centre:
            lon, lat = commune.centre['coordinates']
            folium.Marker(
                location=[lat, lon],
                popup=f"{commune.nom}: {commune.population} hab"
            ).add_to(marker_cluster)
    return m
```

## Prompt 9 : 

Question : Je veux que mon interface Streamlit soit plus complète. Comment je peux faire pour organiser ma page avec des onglets, par exemple : un la carte, un pour les tableaux ? J'aimerais aussi ajouter des graphiques qui bougent quand on passe la souris dessus (pour comparer la taille des villes) et un menu pour que l'utilisateur puisse choisir plusieurs villes et les comparer entre elles

Réponse de l'IA : "Voici une structure complète. On utilise st.tabs pour l'organisation et plotly.express pour les statistiques interactives. J'ajoute aussi un système de comparaison avec st.multiselect :"
```python
import streamlit as st
import plotly.express as px
from src.visualization.maps import create_map

st.title("🇫🇷 France Demographic Analyzer")
tab1, tab2, tab3 = st.tabs(["📊 Données", "🗺️ Carte", "📈 Statistiques"])

with tab1:
    st.dataframe(df) # Affichage du tableau triable
with tab2:
    m = create_map(map_communes)
    st_folium(m) # Affichage de la carte
with tab3:
    fig = px.scatter(df, x="surface", y="population", color="density")
    st.plotly_chart(fig)
```

# Analyse critique des réponses de l'IA 

L’intégration de l’IA générative dans ce workflow de développement a dépassé le simple stade de la génération de "boilerplate code". Ma démarche s'est structurée autour d'un cycle itératif de revue de code et de refactoring, visant à garantir la maintenabilité et la robustesse de l'application.

Dès la phase de conception, si l'IA a permis d'initialiser rapidement un socle technique modulaire respectant la séparation des responsabilités (couches API, Modèles, Services de Cache), j'ai dû intervenir pour corriger des lacunes de conception critiques. Par exemple, sur le module geo_api.py, les implémentations initiales ignoraient la gestion des cas limites (edge cases). J'ai imposé une gestion d'exceptions rigoureuse via la méthode raise_for_status() de la bibliothèque requests et le traitement des payloads JSON vides, transformant une simple requête HTTP en un service résilient aux erreurs 4xx et 5xx.

Concernant le système de cache persistant, l'IA proposait initialement une approche synchrone peu optimisée provoquant un overhead d'entrées/sorties (I/O) à chaque appel. En exerçant mon esprit critique, j'ai réorienté le développement vers une solution hybride : un chargement en mémoire vive (via un dictionnaire Python) pour les lectures fréquentes, couplé à une sérialisation JSON pour la persistance locale. Cette optimisation réduit la latence de l'application et limite les appels redondants vers les points de terminaison (endpoints) de l'API Geo Gouv.

Enfin, l’interface développée avec Streamlit a nécessité un travail d'intégration spécifique pour lier les widgets de l'UI aux méthodes de traitement de données. J'ai dû refuser certaines suggestions de l'IA qui introduisaient un couplage trop fort entre la vue et la logique métier. En imposant l'utilisation de variables d'environnement (.env) pour la configuration et en exigeant un formatage typé des données démographiques, j'ai pu garantir une expérience utilisateur (UX) fluide et sécurisée. Cette collaboration avec l'IA a été un catalyseur pour approfondir mes connaissances en architecture logicielle et en programmation défensive.

Après avoir itéré avec l'IA pour obtenir des fonctions, j'ai intégré le code manuellement, testé sa robustesse et effectué le commit pour valider l'ensemble des étapes demandées.
