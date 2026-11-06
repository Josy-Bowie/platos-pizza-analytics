# 🍕 Plato's Pizza Analytics

## 📊 Présentation du projet

Ce projet de Data Analytics consiste à analyser les ventes de **Plato's Pizza** à partir des données de commandes de l'année 2015.

L'objectif est de transformer des données transactionnelles en indicateurs de performance et en visualisations interactives pour aider à la prise de décision.

## 🎯 Objectifs métier

- Mesurer le chiffre d'affaires et le volume des ventes.
- Identifier les pizzas et catégories les plus performantes.
- Analyser l'évolution mensuelle des ventes.
- Identifier les jours et heures de forte activité.
- Mettre à disposition un dashboard interactif pour explorer les résultats.

## 🛠️ Technologies utilisées

| Technologie | Utilisation |
|---|---|
| Python | Traitement et automatisation des analyses |
| Pandas | Manipulation et préparation des données |
| SQLite / SQL | Stockage et interrogation des données |
| Plotly | Visualisations interactives |
| Streamlit | Développement du dashboard |
| Git / GitHub | Versionnage et partage du projet |

## 🗂️ Organisation du projet

```text
platos-pizza-analytics/
├── app/
│   ├── streamlit_app.py
│   └── pages/
│       ├── overview.py
│       ├── sales.py
│       ├── products.py
│       └── activity.py
├── data/
│   └── raw/
├── docs/
├── notebooks/
├── sql/
├── src/
│   ├── create_db.py
│   ├── run_analysis.py
│   └── dashboard_data.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 📈 Indicateurs clés - 2015

| Indicateur | Résultat |
|---|---:|
| Chiffre d'affaires total | 817 860,05 $ |
| Nombre de commandes | 21 350 |
| Pizzas vendues | 49 574 |
| Panier moyen | 38,31 $ |
| Jour le plus actif | Vendredi |
| Heure de pointe | 12 h |

## 🔎 Analyses réalisées

**1. Vue d'ensemble**

Présentation des principaux indicateurs commerciaux.

**2. Analyse des ventes**

Étude de l'évolution du chiffre d'affaires et comparaison des performances commerciales.

**3. Analyse des produits**

Identification des pizzas les plus vendues et comparaison du chiffre d'affaires par catégorie.

**4. Activité des commandes**

Analyse du nombre de commandes selon les jours de la semaine et les heures.

## 📊 Dashboard Streamlit

Le dashboard comprend quatre pages interactives :

- Vue d'ensemble
- Analyse des ventes
- Analyse des produits
- Activité des commandes

Les visualisations permettent d'explorer les résultats et de mieux comprendre les performances de Plato's Pizza.

## 🚀 Exécution locale

Cloner le dépôt :

```bash
git clone https://github.com/Josy-Bowie/platos-pizza-analytics.git
cd platos-pizza-analytics
```

Créer et activer un environnement virtuel sous Windows avec Git Bash :

```bash
python -m venv .venv
source .venv/Scripts/activate
```

Installer les dépendances :

```bash
python -m pip install -r requirements.txt
```

Après avoir placé les quatre fichiers CSV sources dans `data/raw/`, créer la base SQLite :

```bash
python -m src.create_db
```

Lancer le dashboard :

```bash
python -m streamlit run app/streamlit_app.py
```

**Remarque :** les fichiers CSV et la base SQLite ne sont pas actuellement inclus dans le dépôt GitHub. Ils sont nécessaires pour exécuter localement l'application.

## 💡 Principaux enseignements

L'analyse des ventes montre que :

- Le chiffre d'affaires annuel dépasse 817 000 $.
- Près de 50 000 pizzas ont été vendues.
- Le vendredi est le jour enregistrant le plus grand nombre de commandes.
- L'activité est particulièrement forte autour de midi.
- La catégorie Classic génère le chiffre d'affaires le plus élevé.

Ces résultats peuvent aider à anticiper la demande, organiser les équipes et optimiser la gestion des stocks.

## 👩‍💻 Compétences mobilisées

Ce projet illustre une démarche de Data Analyst :

1. Exploration et contrôle de la qualité des données.
2. Création d'une base de données relationnelle.
3. Construction de requêtes SQL répondant à des questions métier.
4. Préparation et analyse des résultats avec Pandas.
5. Création de visualisations et d'indicateurs de performance.
6. Développement d'une application interactive.
7. Versionnage du code avec Git et GitHub.

## 📌 Statut du projet

- Analyses SQL et Pandas : terminées
- Dashboard Streamlit : développé et testé localement
- Publication du code sur GitHub : effectuée
- Déploiement Streamlit Community Cloud : terminé
