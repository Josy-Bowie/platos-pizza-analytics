
import streamlit as st
from src.run_analysis import charger_analyses


# =====================================================
# 1. CHARGER LES ANALYSES SQL
# =====================================================

@st.cache_data
def charger_donnees():
    return charger_analyses()


resultats = charger_donnees()


# =====================================================
# 2. TITRE DE LA PAGE
# =====================================================

st.title("🍕 Vue d'ensemble")
st.caption("Plato's Pizza | Performances commerciales 2015")


# =====================================================
# 3. RECUPERER LES INDICATEURS SQL
# =====================================================

# Question 1 : chiffre d'affaires total
ca = float(
    resultats["question_1"]["chiffre_affaires_total"].iloc[0]
)

# Question 2 : panier moyen
panier = float(
    resultats["question_2"]["panier_moyen"].iloc[0]
)

# Question 3 : pizzas vendues
pizzas = int(
    resultats["question_3"]["total_pizzas_vendues"].iloc[0]
)

# Question 7 : nombre total de commandes
# Les commandes sont regroupées par jour de semaine.
commandes = int(
    resultats["question_7"]["nombre_commandes"].sum()
)


# =====================================================
# 4. INDICATEURS DE PERFORMANCE
# =====================================================

st.subheader("📊 Indicateurs de performance")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Chiffre d'affaires",
        value=f"{ca:,.2f} $"
    )

with col2:
    st.metric(
        label="Commandes",
        value=f"{commandes:,}"
    )

with col3:
    st.metric(
        label="Pizzas vendues",
        value=f"{pizzas:,}"
    )

with col4:
    st.metric(
        label="Panier moyen",
        value=f"{panier:,.2f} $"
    )

st.divider()


# =====================================================
# 5. SYNTHESE DE L'ACTIVITE
# =====================================================

st.subheader("📋 Synthèse de l'activité")

st.write(
    f"En 2015, Plato's Pizza a réalisé un chiffre "
    f"d'affaires de **{ca:,.2f} $**, "
    f"avec **{commandes:,} commandes** "
    f"et **{pizzas:,} pizzas vendues**."
)

st.write(
    f"Le panier moyen s'élève à **{panier:,.2f} $** "
    f"par commande."
)


# =====================================================
# 6. OBJECTIFS METIER
# =====================================================

st.subheader("🎯 Objectifs de l'analyse")

st.markdown(
    """
    Ce dashboard permet à la direction de :

    - **Suivre les ventes** et le chiffre d'affaires.
    - **Identifier les pizzas les plus populaires.**
    - **Analyser les jours et heures de forte activité.**
    - **Améliorer la planification** du personnel et des stocks.
    """
)


# =====================================================
# 7. VERIFICATION DES KPI
# =====================================================

with st.expander(
    "🔎 Vérification des indicateurs",
    expanded=False
):
    panier_recalcule = (
        ca / commandes if commandes > 0 else 0
    )

    st.write(
        "Panier moyen SQL :",
        f"{panier:,.2f} $"
    )

    st.write(
        "Panier moyen recalculé :",
        f"{panier_recalcule:,.2f} $"
    )

    if round(panier, 2) == round(panier_recalcule, 2):
        st.success("Les indicateurs sont cohérents.")
    else:
        st.warning("Écart détecté dans le panier moyen.")
