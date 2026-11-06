
import streamlit as st
import pandas as pd
import plotly.express as px

from src.dashboard_data import charger_donnees_dashboard

# =====================================================
# 1. TITRE ET CHARGEMENT DES DONNEES
# =====================================================

st.title("📈 Analyse des ventes")
st.caption("Plato's Pizza | Performances commerciales 2015")

@st.cache_data
def charger_donnees():
    return charger_donnees_dashboard()

df = charger_donnees().copy()


# =====================================================
# 2. PREPARATION DES DONNEES
# =====================================================

df["mois"] = pd.to_datetime(df["mois"], format="%Y-%m-%d")

mois_fr = [
    "Janvier", "Février", "Mars", "Avril",
    "Mai", "Juin", "Juillet", "Août",
    "Septembre", "Octobre", "Novembre", "Décembre"
]

df["numero_mois"] = df["mois"].dt.month
df["mois_label"] = df["numero_mois"].map(
    dict(enumerate(mois_fr, start=1))
)

categories_disponibles = sorted(
    df["categorie"].unique().tolist()
)

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
        format_func=lambda m: mois_fr[m - 1]
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

df_categories_choisies = df[
    df["categorie"].isin(categories_selectionnees)
].copy()

df_filtre = df_categories_choisies[
    df_categories_choisies["numero_mois"].between(
        mois_debut, mois_fin
    )
].copy()

if df_filtre.empty:
    st.warning("Aucune donnée pour cette sélection.")
    st.stop()

# =====================================================
# 5. KPI ET COMPARAISONS
# =====================================================

ca_filtre = df_filtre["chiffre_affaires"].sum()
pizzas_filtrees = df_filtre["pizzas_vendues"].sum()

part_ca = (
    ca_filtre / ca_global * 100
    if ca_global != 0 else 0
)

part_pizzas = (
    pizzas_filtrees / pizzas_global * 100
    if pizzas_global != 0 else 0
)

st.markdown("### Indicateurs de performance")

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
# 6. PREPARER LES COMPARAISONS MENSUELLES
# =====================================================

# On conserve tous les mois pour calculer les évolutions.
# Le filtre de catégories est appliqué avant le calcul.

df_evolution = (
    df_categories_choisies
    .groupby(["numero_mois", "mois_label"], as_index=False)
    .agg(chiffre_affaires=("chiffre_affaires", "sum"))
    .sort_values("numero_mois")
)

# pct_change compare chaque mois au précédent.
# fill_method=None évite le remplissage automatique.

df_evolution["evolution_pct"] = (
    df_evolution["chiffre_affaires"]
    .pct_change(fill_method=None) * 100
)

# Une variation en pourcentage n'est pas définie
# lorsque le chiffre d'affaires précédent est nul.

ca_precedent = df_evolution["chiffre_affaires"].shift(1)

df_evolution.loc[
    ca_precedent == 0, "evolution_pct"
] = float("nan")

# Vérifier que les mois comparés sont consécutifs.
numero_precedent = df_evolution["numero_mois"].shift(1)

df_evolution.loc[
    (df_evolution["numero_mois"] - numero_precedent) != 1,
    "evolution_pct"
] = float("nan")

# Conserver uniquement les mois visibles dans le dashboard.

df_mensuel = df_evolution[
    df_evolution["numero_mois"].between(
        mois_debut, mois_fin
    )
].copy()

# =====================================================
# 7. GRAPHIQUE DU CHIFFRE D'AFFAIRES MENSUEL
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

fig_mensuel.update_xaxes(
    categoryorder="array",
    categoryarray=mois_fr
)

fig_mensuel.update_yaxes(rangemode="tozero")

st.plotly_chart(fig_mensuel, width="stretch")

# =====================================================
# 8. NOUVEAU GRAPHIQUE : VARIATION MENSUELLE DU CA
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
        "Aucune variation mensuelle calculable pour "
        "la sélection actuelle."
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
        legend_title="Évolution",
        bargap=0.30
    )

    st.plotly_chart(fig_variation, width="stretch")

    # Identifier les meilleures et moins bonnes évolutions.

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
# 9. GRAPHIQUE DU CA PAR CATEGORIE
# =====================================================

st.subheader("🍕 Chiffre d'affaires par catégorie")

df_categories = (
    df_filtre
    .groupby("categorie", as_index=False)
    .agg(chiffre_affaires=("chiffre_affaires", "sum"))
    .sort_values("chiffre_affaires", ascending=True)
)

fig_categories = px.bar(
    df_categories,
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
# 10. ANALYSE ET RECOMMANDATIONS METIER
# =====================================================

st.subheader("💡 Analyse et recommandations métier")

meilleur_mois = df_mensuel.loc[
    df_mensuel["chiffre_affaires"].idxmax()
]

meilleure_categorie = df_categories.loc[
    df_categories["chiffre_affaires"].idxmax()
]


st.markdown(
    f"""
    **Synthèse des performances sélectionnées**

    Le mois le plus performant est
    **{meilleur_mois['mois_label']}**, avec un chiffre
    d'affaires de **{meilleur_mois['chiffre_affaires']:,.2f} $**.

    La catégorie dominante est
    **{meilleure_categorie['categorie']}**, avec un chiffre
    d'affaires de **{meilleure_categorie['chiffre_affaires']:,.2f} $**.
    """
)


st.markdown("#### Pistes d'action pour la direction")

st.markdown(
    "- **Stocks :** examiner les besoins en ingrédients "
    "des catégories les plus vendues.\n"
    "- **Planification :** analyser les périodes de forte "
    "activité pour adapter les ressources.\n"
    "- **Marketing :** étudier les catégories moins "
    "performantes avant de lancer des promotions.\n"
    "- **Suivi mensuel :** examiner les baisses de chiffre "
    "d'affaires pour identifier leurs causes possibles."
)

# =====================================================
# 11. CONTROLE DES DONNEES
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
