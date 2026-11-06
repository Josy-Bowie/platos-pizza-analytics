
import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# 1. TITRE DE LA PAGE
# =====================================================

st.title("🕒 Activité des commandes")
st.caption("Plato's Pizza | Analyse de l'activité 2015")

# =====================================================
# 2. RECUPERER LES ANALYSES SQL EXISTANTES
# =====================================================

from src.run_analysis import charger_analyses

@st.cache_data
def charger_donnees_activite():
    return charger_analyses()

resultats = charger_donnees_activite()

# Récupérer les deux analyses nécessaires
df_jours = resultats["question_7"].copy()
df_heures = resultats["question_8"].copy()

# =====================================================
# 3. PREPARER LES DONNEES
# =====================================================

# Définir l'ordre chronologique des jours
ordre_jours = [
    "Lundi", "Mardi", "Mercredi", "Jeudi",
    "Vendredi", "Samedi", "Dimanche"
]

df_jours["jour_semaine"] = pd.Categorical(
    df_jours["jour_semaine"],
    categories=ordre_jours,
    ordered=True
)

df_jours = df_jours.sort_values("jour_semaine")

# Convertir les heures en nombres entiers
df_heures["heure"] = pd.to_numeric(
    df_heures["heure"]
)

df_heures = df_heures.sort_values("heure")

# =====================================================
# 4. CALCULER LES INDICATEURS DE PERFORMANCE
# =====================================================

total_commandes = int(
    df_jours["nombre_commandes"].sum()
)

jour_plus_actif = df_jours.loc[
    df_jours["nombre_commandes"].idxmax()
]

heure_plus_active = df_heures.loc[
    df_heures["nombre_commandes"].idxmax()
]

ca_total = df_jours["chiffre_affaires"].sum()

# =====================================================
# 5. AFFICHER LES KPI
# =====================================================

st.subheader("📊 Indicateurs de performance")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(
        "Commandes totales",
        f"{total_commandes:,.0f}"
    )

with kpi2:
    st.metric(
        "Jour le plus actif",
        str(jour_plus_actif["jour_semaine"])
    )

with kpi3:
    st.metric(
        "Heure de pointe",
        f"{int(heure_plus_active['heure']):02d} h"
    )

with kpi4:
    st.metric(
        "Chiffre d'affaires",
        f"{ca_total:,.2f} $"
    )

st.divider()

# =====================================================
# 6. GRAPHIQUE : COMMANDES PAR JOUR
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
    texttemplate="%{text:,.0f}"
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
# 7. GRAPHIQUE : CHIFFRE D'AFFAIRES PAR JOUR
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
    textposition="outside"
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
# 8. GRAPHIQUE : COMMANDES PAR HEURE
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
# 9. ANALYSE METIER
# =====================================================

st.subheader("💡 Analyse et recommandations métier")

jour_leader = str(jour_plus_actif["jour_semaine"])
commandes_jour = int(jour_plus_actif["nombre_commandes"])

heure_pointe = int(heure_plus_active["heure"])
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
    "- **Personnel :** adapter les effectifs aux "
    "jours et heures de forte activité.\n"
    "- **Préparation :** anticiper les besoins en "
    "ingrédients avant les heures de pointe.\n"
    "- **Organisation :** étudier les créneaux "
    "moins actifs pour optimiser les ressources.\n"
    "- **Marketing :** envisager des promotions "
    "sur les périodes moins fréquentées."
)

# =====================================================
# 10. VERIFICATION DES DONNEES
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

    st.write(
        "Total des commandes (jours) :",
        total_commandes
    )

    st.write(
        "Total des commandes (heures) :",
        int(df_heures["nombre_commandes"].sum())
    )
