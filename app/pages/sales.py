
# =====================================================
# PROJET : PLATO'S PIZZA ANALYTICS
# PAGE 2 : ANALYSE DES VENTES
# =====================================================

import pandas as pd
import plotly.express as px
import streamlit as st


# =====================================================
# 1. RECUPERATION DES DONNEES
# =====================================================

st.title("📈 Analyse des ventes")
st.caption("Plato's Pizza | Performances commerciales 2015")

# Les données sont déjà chargées dans streamlit_app.py.
donnees = st.session_state.get("df_dashboard")

if donnees is None or donnees.empty:
    st.error("Les données des ventes sont indisponibles.")
    st.stop()

df = donnees.copy()

colonnes_requises = {
    "mois",
    "categorie",
    "chiffre_affaires",
    "pizzas_vendues"
}

if not colonnes_requises.issubset(df.columns):
    st.error("Certaines colonnes nécessaires sont absentes.")
    st.stop()


# =====================================================
# 2. PREPARATION DES DONNEES
# =====================================================

mois_fr = [
    "Janvier", "Février", "Mars", "Avril",
    "Mai", "Juin", "Juillet", "Août",
    "Septembre", "Octobre", "Novembre", "Décembre"
]

df["mois"] = pd.to_datetime(df["mois"], errors="coerce")

for colonne in ["chiffre_affaires", "pizzas_vendues"]:
    df[colonne] = pd.to_numeric(df[colonne], errors="coerce")

if df[list(colonnes_requises)].isna().any().any():
    st.error("Les données contiennent des valeurs manquantes ou invalides.")
    st.stop()

df["numero_mois"] = df["mois"].dt.month
df["mois_label"] = df["numero_mois"].map(
    dict(enumerate(mois_fr, start=1))
)

categories_disponibles = sorted(df["categorie"].unique())

ca_global = df["chiffre_affaires"].sum()
pizzas_global = df["pizzas_vendues"].sum()


# =====================================================
# 3. FILTRES INTERACTIFS
# =====================================================

st.subheader("🔎 Explorer les performances")

col_filtre1, col_filtre2 = st.columns(2)

with col_filtre1:
    periode = st.select_slider(
        "Période d'analyse",
        options=list(range(1, 13)),
        value=(1, 12),
        format_func=lambda mois: mois_fr[mois - 1]
    )

with col_filtre2:
    categories_selectionnees = st.multiselect(
        "Catégories de pizzas",
        options=categories_disponibles,
        default=categories_disponibles,
        placeholder="Choisir les catégories"
    )


# =====================================================
# 4. APPLICATION DES FILTRES
# =====================================================

mois_debut, mois_fin = periode

# Filtrer d'abord les catégories.
df_categories = df[
    df["categorie"].isin(categories_selectionnees)
].copy()

# Puis filtrer la période.
df_filtre = df_categories[
    df_categories["numero_mois"].between(
        mois_debut, mois_fin
    )
].copy()

if df_filtre.empty:
    st.warning("Aucune donnée pour cette sélection.")
    st.stop()


# =====================================================
# 5. INDICATEURS DE PERFORMANCE
# =====================================================

ca_filtre = df_filtre["chiffre_affaires"].sum()
pizzas_filtrees = df_filtre["pizzas_vendues"].sum()

part_ca = (
    ca_filtre / ca_global * 100
    if ca_global > 0 else 0
)

part_pizzas = (
    pizzas_filtrees / pizzas_global * 100
    if pizzas_global > 0 else 0
)

st.subheader("📊 Indicateurs de performance")

kpi1, kpi2, kpi3 = st.columns(3)

with kpi1:
    st.metric(
        "Chiffre d'affaires sélectionné",
        f"{ca_filtre:,.2f} $"
    )

with kpi2:
    st.metric(
        "Pizzas vendues",
        f"{pizzas_filtrees:,.0f}"
    )

with kpi3:
    st.metric(
        "Part du CA annuel global",
        f"{part_ca:.2f} %"
    )

st.caption(
    f"Référence annuelle : {ca_global:,.2f} $ "
    f"et {pizzas_global:,.0f} pizzas vendues."
)

st.divider()


# =====================================================
# 6. CALCUL DE L'EVOLUTION MENSUELLE
# =====================================================

# Calculer le CA mensuel pour les catégories choisies.
# On conserve tous les mois avant de filtrer la période,
# afin de comparer chaque mois au mois précédent.

df_evolution = (
    df_categories
    .groupby(["numero_mois", "mois_label"], as_index=False)
    .agg(chiffre_affaires=("chiffre_affaires", "sum"))
    .sort_values("numero_mois")
)

# Créer la référence du mois précédent.
df_evolution["ca_precedent"] = (
    df_evolution["chiffre_affaires"].shift(1)
)

df_evolution["numero_precedent"] = (
    df_evolution["numero_mois"].shift(1)
)

# Calculer la variation en pourcentage.
df_evolution["evolution_pct"] = (
    (
        df_evolution["chiffre_affaires"]
        - df_evolution["ca_precedent"]
    )
    / df_evolution["ca_precedent"]
    * 100
)

# Une variation n'est pas calculable si le mois
# précédent est absent ou si son CA est nul.
comparaison_invalide = (
    (df_evolution["ca_precedent"] == 0)
    | (
        df_evolution["numero_mois"]
        - df_evolution["numero_precedent"] != 1
    )
)

df_evolution.loc[
    comparaison_invalide, "evolution_pct"
] = float("nan")

# Conserver les mois de la période sélectionnée.
df_mensuel = df_evolution[
    df_evolution["numero_mois"].between(
        mois_debut, mois_fin
    )
].copy()


# =====================================================
# 7. EVOLUTION DU CHIFFRE D'AFFAIRES
# =====================================================

st.subheader("📊 Évolution du chiffre d'affaires mensuel")

fig_mensuel = px.line(
    df_mensuel,
    x="mois_label",
    y="chiffre_affaires",
    markers=True,
    category_orders={"mois_label": mois_fr},
    labels={
        "mois_label": "Mois",
        "chiffre_affaires": "Chiffre d'affaires ($)"
    }
)

fig_mensuel.update_traces(
    line=dict(color="#2563EB", width=3),
    marker=dict(size=9),
    hovertemplate=(
        "<b>%{x}</b>"
        "<br>CA : %{y:,.2f} $"
        "<extra></extra>"
    )
)

fig_mensuel.update_layout(
    template="plotly_white",
    height=400,
    margin=dict(l=20, r=20, t=30, b=30),
    hovermode="x unified",
    xaxis_title="Mois",
    yaxis_title="Chiffre d'affaires ($)"
)

fig_mensuel.update_yaxes(rangemode="tozero")

st.plotly_chart(fig_mensuel, width="stretch")


# =====================================================
# 8. VARIATION MENSUELLE DU CA
# =====================================================

st.subheader("📉 Variation du chiffre d'affaires par mois")

st.caption(
    "Chaque mois est comparé au mois calendaire précédent, "
    "pour les mêmes catégories sélectionnées."
)

df_variations = df_mensuel.dropna(
    subset=["evolution_pct"]
).copy()

if df_variations.empty:
    st.info(
        "Aucune variation mensuelle calculable "
        "pour cette sélection."
    )

else:
    df_variations["tendance"] = df_variations[
        "evolution_pct"
    ].apply(
        lambda valeur: "Hausse" if valeur >= 0 else "Baisse"
    )

    fig_variation = px.bar(
        df_variations,
        x="mois_label",
        y="evolution_pct",
        color="tendance",
        color_discrete_map={
            "Hausse": "#16A34A",
            "Baisse": "#DC2626"
        },
        category_orders={"mois_label": mois_fr},
        labels={
            "mois_label": "Mois",
            "evolution_pct": "Variation (%)",
            "tendance": "Tendance"
        }
    )

    fig_variation.update_traces(
        hovertemplate=(
            "<b>%{x}</b>"
            "<br>Évolution : %{y:+.2f} %"
            "<extra></extra>"
        )
    )

    fig_variation.add_hline(
        y=0,
        line_color="#64748B",
        line_width=1
    )

    fig_variation.update_layout(
        template="plotly_white",
        height=380,
        margin=dict(l=20, r=20, t=30, b=30),
        xaxis_title="Mois",
        yaxis_title="Variation du CA (%)",
        bargap=0.30
    )

    st.plotly_chart(fig_variation, width="stretch")

    # Identifier les plus fortes variations.
    plus_forte_hausse = df_variations.loc[
        df_variations["evolution_pct"].idxmax()
    ]

    plus_forte_baisse = df_variations.loc[
        df_variations["evolution_pct"].idxmin()
    ]

    col_hausse, col_baisse = st.columns(2)

    with col_hausse:
        if plus_forte_hausse["evolution_pct"] > 0:
            st.metric(
                "Plus forte progression",
                plus_forte_hausse["mois_label"],
                f"{plus_forte_hausse['evolution_pct']:+.2f} %"
            )
        else:
            st.info("Aucune progression sur la sélection.")

    with col_baisse:
        if plus_forte_baisse["evolution_pct"] < 0:
            st.metric(
                "Plus forte baisse",
                plus_forte_baisse["mois_label"],
                f"{plus_forte_baisse['evolution_pct']:+.2f} %",
                delta_color="normal"
            )
        else:
            st.info("Aucune baisse sur la sélection.")

st.divider()


# =====================================================
# 9. CHIFFRE D'AFFAIRES PAR CATEGORIE
# =====================================================

st.subheader("🍕 Chiffre d'affaires par catégorie")

df_ca_categories = (
    df_filtre
    .groupby("categorie", as_index=False)
    .agg(chiffre_affaires=("chiffre_affaires", "sum"))
    .sort_values("chiffre_affaires", ascending=True)
)

fig_categories = px.bar(
    df_ca_categories,
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
    xaxis_title="Chiffre d'affaires ($)",
    yaxis_title=""
)

st.plotly_chart(fig_categories, width="stretch")

st.divider()


# =====================================================
# 10. SYNTHESE ET RECOMMANDATIONS METIER
# =====================================================

st.subheader("💡 Analyse et recommandations métier")

meilleur_mois = df_mensuel.loc[
    df_mensuel["chiffre_affaires"].idxmax()
]

meilleure_categorie = df_ca_categories.loc[
    df_ca_categories["chiffre_affaires"].idxmax()
]

st.markdown(
    f"""
    **Synthèse des performances sélectionnées**

    Le mois le plus performant est
    **{meilleur_mois['mois_label']}**,
    avec un chiffre d'affaires de
    **{meilleur_mois['chiffre_affaires']:,.2f} $**.

    La catégorie dominante est
    **{meilleure_categorie['categorie']}**,
    avec un chiffre d'affaires de
    **{meilleure_categorie['chiffre_affaires']:,.2f} $**.
    """
)

st.markdown("#### Pistes d'action pour la direction")

st.markdown(
    """
    - **Stocks :** examiner les besoins en ingrédients
      des catégories les plus vendues.
    - **Planification :** analyser les périodes de forte
      activité pour adapter les ressources.
    - **Marketing :** étudier les catégories moins
      performantes avant de lancer des promotions.
    - **Suivi mensuel :** examiner les baisses de chiffre
      d'affaires pour identifier leurs causes possibles.
    """
)


# =====================================================
# 11. CONSULTATION DES DONNEES
# =====================================================

with st.expander("📋 Consulter les données filtrées"):

    st.dataframe(
        df_filtre[
            [
                "mois_label",
                "categorie",
                "pizzas_vendues",
                "chiffre_affaires"
            ]
        ],
        hide_index=True,
        width="stretch"
    )

    st.write("Lignes sélectionnées :", len(df_filtre))

    st.write(
        "Part des pizzas vendues :",
        f"{part_pizzas:.2f} %"
    )
