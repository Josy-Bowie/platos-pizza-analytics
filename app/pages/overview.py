
import streamlit as st
from src.run_analysis import charger_analyses


# =====================================================
# 1. CHARGEMENT DES ANALYSES SQL
# =====================================================

@st.cache_data
def charger_donnees():
    return charger_analyses()


resultats = charger_donnees()


# =====================================================
# 2. FONCTION DE VERIFICATION DES INDICATEURS
# =====================================================

def lire_indicateur(numero_question, colonne):
    """
    Récupère une valeur numérique depuis un résultat SQL.
    Arrête la page si le résultat est vide ou manquant.
    """
    nom_question = f"question_{numero_question}"

    if nom_question not in resultats:
        st.error(f"Analyse SQL absente : {nom_question}")
        st.stop()

    df = resultats[nom_question]

    if df.empty:
        st.error(f"L'analyse {nom_question} ne retourne aucune ligne.")
        st.stop()

    if colonne not in df.columns:
        st.error(
            f"Colonne '{colonne}' absente dans {nom_question}."
        )
        st.stop()

    valeur = df[colonne].iloc[0]

    if valeur is None or st.session_state.get(
        "_unused_check", False
    ):
        st.error(
            f"L'analyse {nom_question} retourne une valeur NULL "
            f"pour '{colonne}'. Vérifie le chargement SQL."
        )
        st.stop()

    return valeur


# =====================================================
# 3. TITRE
# =====================================================

st.title("🍕 Vue d'ensemble")
st.caption("Plato's Pizza | Performances commerciales 2015")


# =====================================================
# 4. INDICATEURS SQL
# =====================================================

ca = float(lire_indicateur(1, "chiffre_affaires_total"))

panier = float(lire_indicateur(2, "panier_moyen"))

pizzas = int(lire_indicateur(3, "total_pizzas_vendues"))

df_jours = resultats["question_7"]

if df_jours.empty:
    st.error("L'analyse des commandes par jour est vide.")
    st.stop()

commandes = int(df_jours["nombre_commandes"].sum())


# =====================================================
# 5. KPI
# =====================================================

st.subheader("📊 Indicateurs de performance")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Chiffre d'affaires",
        f"{ca:,.2f} $"
    )

with col2:
    st.metric(
        "Commandes",
        f"{commandes:,}"
    )

with col3:
    st.metric(
        "Pizzas vendues",
        f"{pizzas:,}"
    )

with col4:
    st.metric(
        "Panier moyen",
        f"{panier:,.2f} $"
    )

st.divider()


# =====================================================
# 6. SYNTHESE DE L'ACTIVITE
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
# 7. OBJECTIFS METIER
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
# 8. VERIFICATION DES KPI
# =====================================================

with st.expander("🔎 Vérification des indicateurs"):

    panier_recalcule = ca / commandes if commandes > 0 else 0

    st.write("Panier moyen SQL :", f"{panier:,.2f} $")
    st.write(
        "Panier moyen recalculé :",
        f"{panier_recalcule:,.2f} $"
    )

    if round(panier, 2) == round(panier_recalcule, 2):
        st.success("Les indicateurs sont cohérents.")
    else:
        st.warning("Écart détecté dans le panier moyen.")
