# Plato’s Pizza - Document de cadrage métier

**Projet :** Analyse des ventes et développement d'une application décisionnelle  
**Rôle :** Data Analyst  
**Technologies :** SQL, Python, Pandas, Streamlit, Git/GitHub  
**Version :** 1.0  5 novembre 2026

## 1. Contexte

Plato’s Pizza dispose de données historiques relatives aux commandes et aux produits vendus.

La direction souhaite exploiter ces données afin de mieux comprendre les performances commerciales, les comportements d'achat et les variations de l'activité.

Le projet consiste à construire une base relationnelle SQL, à analyser les données avec SQL et Python, puis à rendre les résultats accessibles dans une application Streamlit interactive.

## 2. Problématique

Comment exploiter les données historiques de commandes de Plato’s Pizza pour identifier les leviers d'amélioration des ventes, optimiser l'offre de produits et mieux anticiper les périodes de forte activité ?

## 3. Objectifs métier

- Mesurer les performances commerciales de la pizzeria.
- Identifier les produits, tailles et catégories qui contribuent le plus aux ventes.
- Comprendre les variations de l'activité selon les heures, les jours et les mois.
- Étudier la composition des commandes et le panier moyen.
- Fournir à la direction des analyses et recommandations fondées sur les données.

## 4. Objectifs opérationnels SMART


1. Construire et contrôler une base relationnelle comportant les quatre tables du jeu de données.
2. Calculer et vérifier cinq indicateurs commerciaux prioritaires.
3. Produire des analyses couvrant trois axes : Produits, Temps et Commandes.
4. Développer une application Streamlit interactive exploitant la base SQL.
5. Présenter au moins trois constats métier accompagnés de recommandations justifiées.

## 5. Sources de données

Le jeu de données Pizza Place Sales comprend quatre fichiers :

- `orders.csv` : commandes, dates et heures.
- `order_details.csv` : lignes de commande et quantités.
- `pizzas.csv` : références, tailles et prix.
- `pizza_types.csv` : noms, catégories et ingrédients.

Les fichiers seront importés dans une base relationnelle SQL. Leur qualité et leurs relations seront vérifiées avant les analyses.

## 6. KPI prioritaires

| Indicateur | Définition |
|---|---|
| Chiffre d'affaires | Somme des quantités multipliées par les prix |
| Nombre de commandes | Nombre de commandes distinctes |
| Pizzas vendues | Somme des quantités commandées |
| Panier moyen | Chiffre d'affaires divisé par le nombre de commandes |
| Pizzas par commande | Quantité totale vendue divisée par le nombre de commandes |

Les règles de calcul seront documentées et validées après contrôle des données.

## 7. Axes d'analyse

**Axe 1 - Produits :** analyser les meilleures ventes, les catégories, les tailles et la contribution au chiffre d'affaires.

**Axe 2 - Temps :** identifier les heures de pointe, les jours les plus actifs et les variations mensuelles.

**Axe 3 - Commandes :** analyser le panier moyen, le nombre de pizzas par commande et la part des commandes contenant une seule pizza.

## 8. Hypothèses initiales

- H1 : certaines pizzas concentrent une part importante du chiffre d'affaires.
- H2 : l'activité est plus élevée à certaines heures.
- H3 : certains jours enregistrent davantage de commandes.
- H4 : les grandes tailles contribuent fortement au chiffre d'affaires.
- H5 : les commandes d'une seule pizza représentent une opportunité potentielle de ventes additionnelles.

Ces hypothèses seront testées et non considérées comme des conclusions acquises.

## 9. Livrables

- Base SQL et scripts de création/import.
- Requêtes SQL documentées.
- Notebook Python d'exploration et d'analyse.
- Application Streamlit interactive connectée à SQL.
- Restitution des résultats et recommandations.
- README GitHub permettant de reproduire le projet.

## 10. Limites identifiées

Le jeu de données ne fournit pas de coûts de production, de données clients ni de distinction entre consommation sur place, vente à emporter et livraison.

L'historique étant limité à 2015, les comparaisons entre années ne sont pas possibles.

Les recommandations devront respecter ces limites et être confirmées par l'analyse des données disponibles.

## 11. Critères de réussite

Le projet sera considéré comme réussi si les données sont correctement structurées, les KPI vérifiés, les analyses interprétables et l'application Streamlit fonctionnelle.

La direction doit pouvoir comprendre les principaux résultats et les utiliser pour orienter ses décisions commerciales.
