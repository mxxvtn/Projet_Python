# Rapport de Projet - France Demographic Analyzer

> **Etudiants** : Lorthios, Verstrepen <br>
> **Formation** : DEUST infrastructure Numérique <br>
> **Module** : Python avec l'IA <br>

---

## 1. Introduction et Périmètre du Projet 

Le présent projet consiste en la conception et la réalisation d'une application de Business Intelligence (BI) appliquée aux données démographiques françaises. L'objectif primaire est de fournir une interface de visualisation dynamique capable de consommer des API RESTful publiques (Geo Gouv) pour restituer des indicateurs statistiques (population, densité, zonage administratif) sous forme de tableaux de bord et de cartographies interactives.

L'enjeu technique réside dans l'équilibre entre la réactivité de l'IHM (Interface Homme-Machine) et la gestion des contraintes réseau, tout en maintenant un code modulaire, extensible et documenté.

---

## 2. Architecture Système et Patterns de Conception 
Pour répondre aux exigences de maintenabilité, l'application a été segmentée suivant un pattern de séparation des préoccupations (Separation of Concerns). L'architecture se décline en quatre strates logiques :

## 2.1. Couche d'Abstraction API (src/api)
Cette couche gère l'intégralité des communications sortantes. Elle encapsule la logique de requêtage vers les endpoints de l'API Geo Gouv. L'utilisation de la bibliothèque requests a été couplée à des mécanismes de validation de schémas JSON pour garantir que les payloads reçus sont conformes aux modèles de données attendus avant tout traitement ultérieur.

## 2.2. Modélisation et Typage (src/models)
Afin d'éviter le "Primitive Obsession" (manipuler uniquement des dictionnaires bruts), des classes Python ont été implémentées pour modéliser les entités Commune, Departement et Region. Ce passage d'une structure de données non-typée à des objets métier permet une manipulation plus sécurisée et facilite l'implémentation de méthodes de calcul internes (ex: calcul de densité de population).

## 2.3. Moteur de Persistance et Cache (src/cache)
Le système repose sur requests-cache avec un backend SQLite. Contrairement à un simple fichier JSON, cette solution offre une persistance robuste et des performances accrues.

- Cache Hit : La donnée est lue instantanément depuis la base SQLite locale.

- Cache Miss : La requête API est exécutée, puis le résultat est automatiquement indexé en base pour 24 heures.

## 2.4. Couche de Présentation (src/visualization & app.py)
L'interface, développée sous Streamlit, agit comme un orchestrateur. Elle gère le State Management (état de la session) pour conserver les filtres utilisateurs et assure le rendu des composants géospatiaux via l'intégration de la bibliothèque Folium.

---

## 3. Implémentation Technique et Résilience 
Le développement a nécessité une attention particulière sur la programmation défensive.

## 3.1. Gestion des Flux et Résilience Réseau
Contrairement aux approches naïves, l'intégration de l'API ne se limite pas à un appel get(). Nous avons implémenté une logique de gestion d'exceptions multi-niveaux :

Exceptions de transport : Capture des erreurs de timeout et de résolution DNS.

Erreurs de protocole : Analyse des codes de statut HTTP (404 pour les codes postaux invalides, 429 pour le rate limiting).

Validation sémantique : Traitement des cas où l'API retourne un succès technique (200 OK) mais un corps de réponse vide, signe d'une entrée utilisateur inexistante dans le référentiel Insee.

## 3.2. Optimisation de la Complexité Temporelle
Pour gérer l'affichage de centaines de communes simultanément, nous avons intégré le plugin MarkerCluster de Folium. Cette technique regroupe les points proches dynamiquement, évitant ainsi la surcharge visuelle et optimisant les performances de rendu du navigateur.

---

## 4. Analyse Critique du Développement Assisté par Intelligence Artificielle 
Dans le cadre de ce projet, l'usage de l'IA (GitHub Copilot / LLM) a été piloté par une approche de revue de code critique et de refactoring dirigé.

## 4.1. Itération et Levée de la Dette Technique
Les suggestions initiales de l'IA tendaient vers un code monolithique et peu sécurisé. Mon rôle a été de déconstruire ces propositions pour introduire des concepts d'injection de dépendances et d'externalisation de la configuration. Par exemple, l'IA suggérait de stocker les URL des API en dur ; j'ai imposé l'usage de variables d'environnement via un fichier .env, garantissant ainsi la portabilité et la sécurité des informations sensibles.

## 4.2. Arbitrages sur le Cache et les E/S (Entrées/Sorties)
Une confrontation technique a eu lieu lors de l'implémentation du cache. Là où l'IA proposait une réécriture complète du fichier JSON à chaque mise à jour (risque de corruption de données et latence élevée), , j'ai imposé l'usage de requests-cache. Ce choix illustre un esprit critique visant la fiabilité système et l'efficacité des entrées/sorties.

---

## 5. Défis Techniques et Solutions Apportées 
Désérialisation des caractères spéciaux : Les données géographiques françaises comportent de nombreux accents. Il a fallu configurer l'encodage UTF-8 de manière stricte sur toute la chaîne de traitement (API -> JSON -> Streamlit) pour éviter les erreurs de décodage.

Interopérabilité des systèmes de coordonnées : L'affichage cartographique via Folium nécessite des coordonnées au format WGS84. Une étape de normalisation des données a été insérée dans le modèle Commune pour convertir les formats bruts de l'API en objets géospatiaux exploitables.

---

## 6. Conclusion et Perspectives d'Évolution
Ce projet valide la capacité de mettre en œuvre une application Python complète, du backend (API/Cache) au frontend (Streamlit). L'architecture modulaire permet d'envisager des évolutions futures telles que :

L'intégration d'un moteur de recherche asynchrone pour améliorer l'expérience utilisateur.

Le passage d'un stockage JSON à une base de données légère de type SQLite pour gérer de plus gros volumes de données démographiques historiques.

L'implémentation de tests unitaires automatisés via pytest pour valider la non-régression sur la couche API.
