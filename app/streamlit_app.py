
import sys
from pathlib import Path
from src.create_db import creer_base
import streamlit as st


# =====================================================
# 1. CONFIGURATION DES CHEMINS
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Permet à Streamlit de trouver les fichiers du dossier src
sys.path.insert(0, str(PROJECT_ROOT))


# =====================================================
# 2. IMPORTATION DES FONCTIONS PYTHON
# =====================================================

from src.run_analysis import charger_analyses
from src.dashboard_data import charger_donnees_dashboard


# =====================================================
# 3. CONFIGURATION DE STREAMLIT
# =====================================================

st.set_page_config(
    page_title="Plato's Pizza Analytics",
    page_icon="🍕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialisation de la base SQLite
DB_FILE = PROJECT_ROOT / "data" / "pizza.db"

if not DB_FILE.exists():
    st.info("Initialisation de la base de données...")
    creer_base()

    
# =====================================================
# 4. CHARGEMENT DES DONNEES
# =====================================================

@st.cache_data
def charger_donnees():
    """Charger les 8 analyses SQL."""
    return charger_analyses()


@st.cache_data
def charger_donnees_filtres():
    """Charger les ventes par mois et categorie."""
    return charger_donnees_dashboard()


# Charger les deux ensembles de donnees
resultats = charger_donnees()

df_dashboard = charger_donnees_filtres()


# =====================================================
# 5. PARTAGE DES DONNEES ENTRE LES PAGES
# =====================================================

st.session_state["resultats"] = resultats

st.session_state["df_dashboard"] = df_dashboard


# =====================================================
# 6. MENU DE NAVIGATION
# =====================================================

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


# =====================================================
# 7. INFORMATIONS DANS LA BARRE LATERALE
# =====================================================

with st.sidebar:

    st.title("🍕 Plato's Pizza")

    st.caption("Business Intelligence | 2015")

    st.divider()

    st.caption("Source : SQLite")

    st.caption("Analyses : SQL + Pandas")

    st.divider()

    # Verification temporaire des donnees
    with st.expander("🔎 Vérification des données"):

        st.write("Analyses SQL :", len(resultats))

        st.write("Lignes dashboard :", len(df_dashboard))

        st.write(
            "Colonnes dashboard :",
            df_dashboard.shape[1]
        )


# =====================================================
# 8. EXECUTION DE LA PAGE SELECTIONNEE
# =====================================================

navigation.run()

