
# =====================================================
# PROJET : PLATO'S PIZZA ANALYTICS
# PAGE 3 : ANALYSE DES PRODUITS
# =====================================================

import pandas as pd
import plotly.express as px
import streamlit as st


# =====================================================
# 1. TITRE DE LA PAGE
# =====================================================

st.title("🍕 Analyse des produits")
st.caption("Plato's Pizza | Performances produits 2015")


# =====================================================
# 2. RECUPERATION DES ANALYSES SQL
# =====================================================

# Les analyses sont déjà chargées dans streamlit_app.py.
resultats = st.session_state.get("resultats")

if resultats is None:
    st.error("Les analyses SQL sont indisponibles.")
    st.stop()

# Vérifier la présence des trois analyses nécessaires.
questions_requises = [
    "question_3",
    "question_4",
    "question_5"
]

for question in questions_requises:
    if question not in resultats:
        st.error(f"Analyse SQL manquante : {question}")
        st.stop()

# Copier les DataFrames pour préserver les originaux.
df_total = resultats["question_3"].copy()
df_pizzas = resultats["question_4"].copy()
df_categories = resultats["question_5"].copy()


# =====================================================
# 3. VERIFICATION ET PREPARATION DES DONNEES
# =====================================================

# Vérifier que les résultats ne sont pas vides.
if df_total.empty or df_pizzas.empty or df_categories.empty:
    st.error("Une ou plusieurs analyses SQL sont vides.")
    st.stop()

# Définir les colonnes attendues.
colonnes_total = {"total_pizzas_vendues"}
colonnes_pizzas = {"nom_pizza", "quantite_vendue"}
colonnes_categories = {"categorie", "chiffre_affaires"}

# Vérifier les colonnes.
if not colonnes_total.issubset(df_total.columns):
    st.error("Colonne du total des pizzas manquante.")
    st.stop()

if not colonnes_pizzas.issubset(df_pizzas.columns):
    st.error("Colonnes des pizzas manquantes.")
    st.stop()

if not colonnes_categories.issubset(df_categories.columns):
    st.error("Colonnes des catégories manquantes.")
    st.stop()

# Convertir les valeurs numériques.
df_total["total_pizzas_vendues"] = pd.to_numeric(
    df_total["total_pizzas_vendues"],
    errors="coerce"
)

df_pizzas["quantite_vendue"] = pd.to_numeric(
    df_pizzas["quantite_vendue"],
    errors="coerce"
)

df_categories["chiffre_affaires"] = pd.to_numeric(
    df_categories["chiffre_affaires"],
    errors="coerce"
)

# Vérifier les valeurs manquantes.
if (
    df_total["total_pizzas_vendues"].isna().any()
    or df_pizzas[["nom_pizza", "quantite_vendue"]].isna().any().any()
    or df_categories[["categorie", "chiffre_affaires"]].isna().any().any()
):
    st.error("Certaines données produits sont manquantes ou invalides.")
    st.stop()

# Trier les pizzas par quantité vendue.
df_pizzas = df_pizzas.sort_values(
    "quantite_vendue",
    ascending=False
)

# Trier les catégories par chiffre d'affaires.
df_categories = df_categories.sort_values(
    "chiffre_affaires",
    ascending=False
)


# =====================================================
# 4. CALCUL DES INDICATEURS
# =====================================================

# Total de toutes les pizzas vendues.
total_pizzas = int(
    df_total["total_pizzas_vendues"].iloc[0]
)

# Conserver les 10 pizzas les plus vendues.
df_top10 = df_pizzas.head(10).copy()

# Quantité vendue par les pizzas du Top 10.
pizzas_top10 = int(
    df_top10["quantite_vendue"].sum()
)

# Identifier la pizza la plus vendue.
pizza_top = df_top10.iloc[0]

# Identifier la catégorie générant le plus de CA.
categorie_top = df_categories.iloc[0]


# =====================================================
# 5. INDICATEURS DE PERFORMANCE
# =====================================================

st.subheader("📊 Indicateurs de performance")

kpi1, kpi2, kpi3 = st.columns(3)

with kpi1:
    st.metric(
        "Pizzas vendues",
        f"{total_pizzas:,}"
    )

with kpi2:
    st.metric(
        "Pizzas vendues - Top 10",
        f"{pizzas_top10:,}"
    )

with kpi3:
    st.metric(
        "Catégorie leader",
        categorie_top["categorie"]
    )

st.divider()


# =====================================================
# 6. TOP 10 DES PIZZAS LES PLUS VENDUES
# =====================================================

st.subheader("🏆 Top 10 des pizzas les plus vendues")

# Trier dans l'ordre croissant pour le graphique horizontal.
df_top10_graphique = df_top10.sort_values(
    "quantite_vendue",
    ascending=True
)

fig_top10 = px.bar(
    df_top10_graphique,
    x="quantite_vendue",
    y="nom_pizza",
    orientation="h",
    text="quantite_vendue",
    labels={
        "nom_pizza": "Pizza",
        "quantite_vendue": "Quantité vendue"
    }
)

fig_top10.update_traces(
    marker_color="#2563EB",
    textposition="outside",
    cliponaxis=False,
    hovertemplate=(
        "<b>%{y}</b>"
        "<br>Quantité vendue : %{x:,.0f}"
        "<extra></extra>"
    )
)

fig_top10.update_layout(
    template="plotly_white",
    height=500,
    margin=dict(l=20, r=90, t=20, b=30),
    yaxis_title="",
    xaxis_title="Quantité vendue"
)

st.plotly_chart(fig_top10, width="stretch")

st.divider()


# =====================================================
# 7. CHIFFRE D'AFFAIRES PAR CATEGORIE
# =====================================================

st.subheader("💰 Chiffre d'affaires par catégorie")

df_categories_graphique = df_categories.sort_values(
    "chiffre_affaires",
    ascending=True
)

fig_categories = px.bar(
    df_categories_graphique,
    x="chiffre_affaires",
    y="categorie",
    orientation="h",
    text="chiffre_affaires",
    labels={
        "categorie": "Catégorie",
        "chiffre_affaires": "Chiffre d'affaires ($)"
    }
)

fig_categories.update_traces(
    marker_color="#2563EB",
    texttemplate="%{text:,.0f} $",
    textposition="outside",
    cliponaxis=False,
    hovertemplate=(
        "<b>%{y}</b>"
        "<br>CA : %{x:,.2f} $"
        "<extra></extra>"
    )
)

fig_categories.update_layout(
    template="plotly_white",
    height=350,
    margin=dict(l=20, r=120, t=20, b=30),
    yaxis_title="",
    xaxis_title="Chiffre d'affaires ($)"
)

st.plotly_chart(fig_categories, width="stretch")

st.divider()


# =====================================================
# 8. ANALYSE ET RECOMMANDATIONS METIER
# =====================================================

st.subheader("💡 Analyse et recommandations métier")

st.write(
    f"La pizza la plus vendue est "
    f"**{pizza_top['nom_pizza']}**, avec "
    f"**{pizza_top['quantite_vendue']:,.0f} unités**."
)

st.write(
    f"La catégorie générant le plus de revenus est "
    f"**{categorie_top['categorie']}**, avec "
    f"**{categorie_top['chiffre_affaires']:,.2f} $**."
)

st.markdown("#### Pistes d'action pour la direction")

st.markdown(
    """
    - **Stocks :** surveiller les ingrédients des pizzas
      les plus populaires.
    - **Marketing :** étudier les pizzas les moins vendues
      avant de proposer des promotions.
    - **Rentabilité :** compléter l'analyse avec les coûts
      pour identifier les pizzas les plus rentables.
    """
)


# =====================================================
# 9. CONSULTATION DES DONNEES
# =====================================================

with st.expander("📋 Consulter les données produits"):

    st.dataframe(
        df_pizzas,
        hide_index=True,
        width="stretch"
    )

    st.write(
        "Nombre de pizzas dans le Top 10 :",
        len(df_top10)
    )

    st.write(
        "Quantité vendue par le Top 10 :",
        f"{pizzas_top10:,}"
    )
