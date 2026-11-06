
import sqlite3
import pandas as pd
from pathlib import Path

# Identifier la racine du projet
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Localiser la base SQLite et la requête SQL
DB_FILE = PROJECT_ROOT / "data" / "pizza.db"
SQL_FILE = PROJECT_ROOT / "sql" / "03_dashboard_filters.sql"


def charger_donnees_dashboard():
    """
    Charger les ventes par mois et catégorie
    depuis la base SQLite.
    """

    # Lire la requête SQL
    query = SQL_FILE.read_text(encoding="utf-8")

    # Connexion SQLite en lecture seule
    with sqlite3.connect(
        f"file:{DB_FILE.as_posix()}?mode=ro",
        uri=True
    ) as conn:

        # Exécuter la requête et récupérer un DataFrame
        df = pd.read_sql_query(query, conn)

    # Convertir le mois en date
    df["mois"] = pd.to_datetime(
        df["mois"],
        format="%Y-%m"
    )

    # Trier les données chronologiquement
    df = df.sort_values(
        ["mois", "categorie"]
    ).reset_index(drop=True)

    return df


# Test uniquement si le fichier est exécuté directement
if __name__ == "__main__":

    df = charger_donnees_dashboard()

    print("\nDONNÉES DASHBOARD CHARGÉES")
    print(df.head())

    print("\nDIMENSIONS :", df.shape)
    print("\nTYPES DES COLONNES :")
    print(df.dtypes)
