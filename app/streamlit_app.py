
# ==================================================
# PROJET : PLATO'S PIZZA ANALYTICS
# Application principale Streamlit
# ==================================================

# 1. IMPORTATION DES MODULES
import sys
from pathlib import Path

import streamlit as st


# ==================================================
# 2. CONFIGURATION DES CHEMINS
# ==================================================

# Identifier la racine du projet
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Permettre à Python de trouver les modules du dossier src
sys.path.insert(0, str(PROJECT_ROOT))


# ==================================================
# 3. IMPORTATION DES FONCTIONS DU PROJET
# ==================================================

from src.create_db import creer_base
from src.run_analysis import charger_analyses
from src.dashboard_data import charger_donnees_dashboard


# ==================================================
# 4. CONFIGURATION DE STREAMLIT
# ==================================================

st.set_page_config(
    page_title="Plato's Pizza Analytics",
    page_icon="🍕",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# 5. INITIALISATION DE LA BASE SQLITE
# ==================================================

DB_FILE = PROJECT_ROOT / "data" / "pizza.db"

# Créer la base de données uniquement si elle n'existe pas
if not DB_FILE.exists():

    with st.spinner("Initialisation de la base de données..."):
        creer_base()


# ==================================================
# 6. CHARGEMENT DES DONNEES
# ==================================================

@st.cache_data
def charger_donnees():
    """Charger les huit analyses SQL."""
    return charger_analyses()


@st.cache_data
def charger_donnees_filtres():
    """Charger les données des ventes par mois et catégorie."""
    return charger_donnees_dashboard()


# Charger les analyses métier
resultats = charger_donnees()

# Charger les données utilisées par les filtres
df_dashboard = charger_donnees_filtres()


# ==================================================
# 7. PARTAGE DES DONNEES ENTRE LES PAGES
# ==================================================

# Rendre les données accessibles aux différentes pages
st.session_state["resultats"] = resultats

st.session_state["df_dashboard"] = df_dashboard


# ==================================================
# 8. MENU DE NAVIGATION
# ==================================================

navigation = st.navigation(
    [
        st.Page(
            "pages/overview.py",
            title="Vue d'ensemble",
            icon=":material/dashboard:",
            default=True
        ),

        st.Page(
            "pages/sales.py",
            title="Analyse des ventes",
            icon=":material/trending_up:"
        ),

        st.Page(
            "pages/products.py",
            title="Analyse des produits",
            icon=":material/local_pizza:"
        ),

        st.Page(
            "pages/activity.py",
            title="Activité des commandes",
            icon=":material/schedule:"
        )
    ],
    position="sidebar"
)


# ==================================================
# 9. INFORMATIONS DANS LA BARRE LATERALE
# ==================================================

with st.sidebar:

    st.title("🍕 Plato's Pizza")

    st.caption("Business Intelligence | 2015")

    st.divider()

    st.caption("Source : SQLite")

    st.caption("Analyses : SQL + Pandas")


# ==================================================
# 10. EXECUTION DE LA PAGE SELECTIONNEE
# ==================================================

navigation.run()
