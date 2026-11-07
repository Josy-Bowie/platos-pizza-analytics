
# =====================================================
# PROJET : PLATO'S PIZZA ANALYTICS
# PAGE 1 : VUE D'ENSEMBLE
# =====================================================

import pandas as pd
import streamlit as st


# =====================================================
# 1. RECUPERATION DES ANALYSES SQL
# =====================================================

# Les analyses sont déjà chargées dans streamlit_app.py
# et partagées entre les pages via session_state.

resultats = st.session_state.get("resultats")

if resultats is None:
    st.error("Les analyses SQL ne sont pas disponibles.")
    st.stop()


# =====================================================
# 2. FONCTION DE LECTURE DES INDICATEURS
# =====================================================

def lire_indicateur(numero_question, colonne):
    """
    Récupérer une valeur numérique depuis les résultats SQL.
    Vérifier que l'analyse, la colonne et la valeur existent.
    """

    nom_question = f"question_{numero_question}"

    if nom_question not in resultats:
        st.error(f"Analyse SQL introuvable : {nom_question}")
        st.stop()

    df = resultats[nom_question]

    if df.empty or colonne not in df.columns:
        st.error(
            f"Données indisponibles pour {nom_question} : {colonne}"
        )
        st.stop()

    valeur = df[colonne].iloc[0]

    if pd.isna(valeur):
        st.error(
            f"Valeur manquante pour {nom_question} : {colonne}"
        )
        st.stop()

    return valeur


# =====================================================
# 3. TITRE DE LA PAGE
# =====================================================

st.title("🍕 Vue d'ensemble")

st.caption("Plato's Pizza | Performances commerciales 2015")


# =====================================================
# 4. RECUPERATION DES INDICATEURS
# =====================================================

# Chiffre d'affaires total
ca = float(
    lire_indicateur(1, "chiffre_affaires_total")
)

# Panier moyen
panier = float(
    lire_indicateur(2, "panier_moyen")
)

# Nombre total de pizzas vendues
pizzas = int(
    lire_indicateur(3, "total_pizzas_vendues")
)

# Nombre total de commandes
# Chaque commande appartient à un seul jour de la semaine.

df_jours = resultats.get("question_7")

if (
    df_jours is None
    or df_jours.empty
    or "nombre_commandes" not in df_jours.columns
    or df_jours["nombre_commandes"].isna().any()
):
    st.error("Les données des commandes sont indisponibles.")
    st.stop()

commandes = int(df_jours["nombre_commandes"].sum())


# =====================================================
# 5. INDICATEURS DE PERFORMANCE
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
# 8. VERIFICATION DE COHERENCE DES KPI
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
