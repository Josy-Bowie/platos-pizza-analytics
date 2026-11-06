
import streamlit as st
import plotly.express as px

# =====================================================
# 1. TITRE DE LA PAGE
# =====================================================

st.title("🍕 Analyse des produits")
st.caption("Plato's Pizza | Performances produits 2015")

# =====================================================
# 2. RECUPERER LES ANALYSES SQL
# =====================================================

# Charger les analyses SQL existantes
from src.run_analysis import charger_analyses

@st.cache_data
def charger_donnees_produits():
    return charger_analyses()

resultats = charger_donnees_produits()

# Copier les données pour ne pas modifier les originaux
df_pizzas = resultats["question_4"].copy()
df_categories = resultats["question_5"].copy()
# Récupérer le total global des pizzas vendues
df_total = resultats["question_3"].copy()

# =====================================================
# 3. PREPARER LES DONNEES
# =====================================================

df_pizzas = df_pizzas.sort_values(
    "quantite_vendue",
    ascending=False
)

df_categories = df_categories.sort_values(
    "chiffre_affaires",
    ascending=False
)

# =====================================================
# 4. INDICATEURS DE PERFORMANCE
# =====================================================

st.subheader("📊 Indicateurs de performance")

# Total global de toutes les pizzas vendues
total_pizzas = int(
    df_total["total_pizzas_vendues"].iloc[0]
)

# Quantité vendue par les 10 pizzas les plus populaires
pizzas_top10 = int(
    df_pizzas["quantite_vendue"].sum()
)

# Nombre de pizzas présentes dans le Top 10
nombre_pizzas = df_pizzas["nom_pizza"].nunique()

pizza_top = df_pizzas.iloc[0]
categorie_top = df_categories.iloc[0]

kpi1, kpi2, kpi3 = st.columns(3)

with kpi1:
    st.metric(
        "Pizzas vendues",
        f"{total_pizzas:,.0f}"
    )

with kpi2:
    st.metric(
        "Pizzas vendues - Top 10",
        f"{pizzas_top10:,.0f}"
    )

with kpi3:
    st.metric(
        "Catégorie leader",
        categorie_top["categorie"]
    )

st.divider()

# =====================================================
# 5. TOP 10 DES PIZZAS LES PLUS VENDUES
# =====================================================

st.subheader("🏆 Top 10 des pizzas les plus vendues")

df_top10 = df_pizzas.head(10).sort_values(
    "quantite_vendue",
    ascending=True
)

fig_top10 = px.bar(
    df_top10,
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
    cliponaxis=False
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
# 6. CHIFFRE D'AFFAIRES PAR CATEGORIE
# =====================================================

st.subheader("💰 Chiffre d'affaires par catégorie")

fig_categories = px.bar(
    df_categories.sort_values("chiffre_affaires"),
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
    cliponaxis=False
)

fig_categories.update_layout(
    template="plotly_white",
    height=350,
    margin=dict(l=20, r=120, t=20, b=30),
    yaxis_title=""
)

st.plotly_chart(fig_categories, width="stretch")

st.divider()

# =====================================================
# 7. ANALYSE METIER
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
    "- **Stocks :** surveiller les ingrédients des pizzas "
    "les plus populaires.\n"
    "- **Marketing :** étudier les pizzas les moins vendues "
    "avant de proposer des promotions.\n"
    "- **Rentabilité :** compléter l'analyse avec les coûts "
    "pour identifier les pizzas les plus rentables."
)

# =====================================================
# 8. VERIFICATION DES DONNEES
# =====================================================

with st.expander("📋 Consulter les données produits"):
    st.dataframe(
        df_pizzas,
        hide_index=True,
        width="stretch"
    )
