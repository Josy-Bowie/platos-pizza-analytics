
# =====================================================
# PROJET : PLATO'S PIZZA ANALYTICS
# PAGE 4 : ACTIVITE DES COMMANDES
# =====================================================

import pandas as pd
import plotly.express as px
import streamlit as st


# =====================================================
# 1. TITRE DE LA PAGE
# =====================================================

st.title("🕒 Activité des commandes")
st.caption("Plato's Pizza | Analyse de l'activité 2015")


# =====================================================
# 2. RECUPERATION DES ANALYSES SQL
# =====================================================

# Les analyses sont déjà chargées dans streamlit_app.py.
resultats = st.session_state.get("resultats")

if resultats is None:
    st.error("Les analyses SQL sont indisponibles.")
    st.stop()

# Vérifier la présence des analyses nécessaires.
questions_requises = [
    "question_7",
    "question_8"
]

for question in questions_requises:

    if question not in resultats:
        st.error(f"Analyse SQL manquante : {question}")
        st.stop()

# Copier les DataFrames pour préserver les originaux.
df_jours = resultats["question_7"].copy()
df_heures = resultats["question_8"].copy()


# =====================================================
# 3. VERIFICATION DES DONNEES
# =====================================================

# Vérifier que les analyses ne sont pas vides.
if df_jours.empty or df_heures.empty:
    st.error("Les données d'activité sont indisponibles.")
    st.stop()

# Définir les colonnes nécessaires.
colonnes_jours = {
    "jour_semaine",
    "nombre_commandes",
    "chiffre_affaires"
}

colonnes_heures = {
    "heure",
    "nombre_commandes"
}

# Vérifier la présence des colonnes.
if not colonnes_jours.issubset(df_jours.columns):
    st.error("Certaines colonnes des jours sont absentes.")
    st.stop()

if not colonnes_heures.issubset(df_heures.columns):
    st.error("Certaines colonnes des heures sont absentes.")
    st.stop()


# =====================================================
# 4. PREPARATION DES DONNEES
# =====================================================

# Définir l'ordre chronologique des jours.
ordre_jours = [
    "Lundi",
    "Mardi",
    "Mercredi",
    "Jeudi",
    "Vendredi",
    "Samedi",
    "Dimanche"
]

# Convertir les valeurs numériques.
df_jours["nombre_commandes"] = pd.to_numeric(
    df_jours["nombre_commandes"],
    errors="coerce"
)

df_jours["chiffre_affaires"] = pd.to_numeric(
    df_jours["chiffre_affaires"],
    errors="coerce"
)

df_heures["heure"] = pd.to_numeric(
    df_heures["heure"],
    errors="coerce"
)

df_heures["nombre_commandes"] = pd.to_numeric(
    df_heures["nombre_commandes"],
    errors="coerce"
)

# Vérifier les valeurs manquantes ou invalides.
if (
    df_jours[list(colonnes_jours)].isna().any().any()
    or df_heures[list(colonnes_heures)].isna().any().any()
):
    st.error("Les données d'activité contiennent des valeurs invalides.")
    st.stop()

# Organiser les jours dans l'ordre de la semaine.
df_jours["jour_semaine"] = pd.Categorical(
    df_jours["jour_semaine"],
    categories=ordre_jours,
    ordered=True
)

# Vérifier que les jours sont reconnus.
if df_jours["jour_semaine"].isna().any():
    st.error("Un jour de la semaine est inconnu.")
    st.stop()

df_jours = df_jours.sort_values("jour_semaine")

# Convertir les heures en nombres entiers.
df_heures["heure"] = df_heures["heure"].astype(int)

df_heures = df_heures.sort_values("heure")


# =====================================================
# 5. CALCUL DES INDICATEURS
# =====================================================

# Nombre total de commandes.
total_commandes = int(
    df_jours["nombre_commandes"].sum()
)

# Jour enregistrant le plus de commandes.
jour_plus_actif = df_jours.loc[
    df_jours["nombre_commandes"].idxmax()
]

# Heure enregistrant le plus de commandes.
heure_plus_active = df_heures.loc[
    df_heures["nombre_commandes"].idxmax()
]

# Chiffre d'affaires total.
ca_total = float(
    df_jours["chiffre_affaires"].sum()
)


# =====================================================
# 6. INDICATEURS DE PERFORMANCE
# =====================================================

st.subheader("📊 Indicateurs de performance")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(
        label="Commandes totales",
        value=f"{total_commandes:,}"
    )

with kpi2:
    st.metric(
        label="Jour le plus actif",
        value=str(jour_plus_actif["jour_semaine"])
    )

with kpi3:
    st.metric(
        label="Heure de pointe",
        value=f"{int(heure_plus_active['heure']):02d} h"
    )

with kpi4:
    st.metric(
        label="Chiffre d'affaires",
        value=f"{ca_total:,.2f} $"
    )

st.divider()


# =====================================================
# 7. GRAPHIQUE : COMMANDES PAR JOUR
# =====================================================

st.subheader("📅 Nombre de commandes par jour")

fig_jours = px.bar(
    df_jours,
    x="jour_semaine",
    y="nombre_commandes",
    text="nombre_commandes",
    labels={
        "jour_semaine": "Jour de la semaine",
        "nombre_commandes": "Nombre de commandes"
    }
)

fig_jours.update_traces(
    marker_color="#2563EB",
    textposition="outside",
    texttemplate="%{text:,.0f}",
    cliponaxis=False
)

fig_jours.update_layout(
    template="plotly_white",
    height=420,
    margin=dict(l=20, r=20, t=30, b=30),
    xaxis_title="Jour de la semaine",
    yaxis_title="Nombre de commandes"
)

fig_jours.update_yaxes(rangemode="tozero")

st.plotly_chart(fig_jours, width="stretch")


# =====================================================
# 8. GRAPHIQUE : CHIFFRE D'AFFAIRES PAR JOUR
# =====================================================

st.subheader("💰 Chiffre d'affaires par jour")

fig_ca = px.bar(
    df_jours,
    x="jour_semaine",
    y="chiffre_affaires",
    text="chiffre_affaires",
    labels={
        "jour_semaine": "Jour",
        "chiffre_affaires": "Chiffre d'affaires ($)"
    }
)

fig_ca.update_traces(
    marker_color="#16A34A",
    texttemplate="%{text:,.0f} $",
    textposition="outside",
    cliponaxis=False
)

fig_ca.update_layout(
    template="plotly_white",
    height=420,
    margin=dict(l=20, r=20, t=30, b=30),
    xaxis_title="Jour de la semaine",
    yaxis_title="Chiffre d'affaires ($)"
)

fig_ca.update_yaxes(rangemode="tozero")

st.plotly_chart(fig_ca, width="stretch")

st.divider()


# =====================================================
# 9. GRAPHIQUE : COMMANDES PAR HEURE
# =====================================================

st.subheader("⏰ Répartition des commandes par heure")

fig_heures = px.bar(
    df_heures,
    x="heure",
    y="nombre_commandes",
    labels={
        "heure": "Heure de la journée",
        "nombre_commandes": "Nombre de commandes"
    }
)

fig_heures.update_traces(
    marker_color="#F97316",
    hovertemplate=(
        "<b>%{x} h</b>"
        "<br>Commandes : %{y:,.0f}"
        "<extra></extra>"
    )
)

fig_heures.update_layout(
    template="plotly_white",
    height=420,
    margin=dict(l=20, r=20, t=30, b=30),
    xaxis_title="Heure de la journée",
    yaxis_title="Nombre de commandes",
    xaxis=dict(
        tickmode="array",
        tickvals=df_heures["heure"].tolist()
    )
)

fig_heures.update_yaxes(rangemode="tozero")

st.plotly_chart(fig_heures, width="stretch")

st.divider()


# =====================================================
# 10. ANALYSE ET RECOMMANDATIONS METIER
# =====================================================

st.subheader("💡 Analyse et recommandations métier")

# Récupérer les valeurs des périodes les plus actives.
jour_leader = str(jour_plus_actif["jour_semaine"])

commandes_jour = int(
    jour_plus_actif["nombre_commandes"]
)

heure_pointe = int(
    heure_plus_active["heure"]
)

commandes_heure = int(
    heure_plus_active["nombre_commandes"]
)

st.markdown("#### Synthèse de l'activité")

st.write(
    f"Le jour enregistrant le plus de commandes "
    f"est **{jour_leader}**, avec "
    f"**{commandes_jour:,} commandes**."
)

st.write(
    f"L'heure la plus active est **{heure_pointe:02d} h**, "
    f"avec **{commandes_heure:,} commandes** "
    f"sur l'ensemble de l'année."
)

st.markdown("#### Pistes d'action pour la direction")

st.markdown(
    """
    - **Personnel :** adapter les effectifs aux jours
      et heures de forte activité.
    - **Préparation :** anticiper les besoins en
      ingrédients avant les heures de pointe.
    - **Organisation :** étudier les créneaux moins
      actifs pour optimiser les ressources.
    - **Marketing :** envisager des promotions sur
      les périodes moins fréquentées.
    """
)


# =====================================================
# 11. CONSULTATION DES DONNEES
# =====================================================

with st.expander("📋 Consulter les données d'activité"):

    st.markdown("**Activité par jour**")

    st.dataframe(
        df_jours,
        hide_index=True,
        width="stretch"
    )

    st.markdown("**Activité par heure**")

    st.dataframe(
        df_heures,
        hide_index=True,
        width="stretch"
    )

    # Contrôle de cohérence des commandes.
    total_commandes_heures = int(
        df_heures["nombre_commandes"].sum()
    )

    st.write(
        "Total des commandes (jours) :",
        total_commandes
    )

    st.write(
        "Total des commandes (heures) :",
        total_commandes_heures
    )

    if total_commandes == total_commandes_heures:
        st.success("Les totaux des commandes sont cohérents.")
    else:
        st.warning("Écart détecté entre les totaux.")
