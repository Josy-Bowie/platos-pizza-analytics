
import sqlite3
import pandas as pd
from pathlib import Path

# 1. Chemins du projet
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_FILE = PROJECT_ROOT / "data" / "pizza.db"
SQL_FILE = PROJECT_ROOT / "sql" / "02_business_analysis.sql"


# 2. Fonction réutilisable pour Python et Streamlit
def charger_analyses():

    # Lire les requêtes SQL
    query = SQL_FILE.read_text(encoding="utf-8")

    # Supprimer les commentaires SQL
    lignes_sql = []

    for ligne in query.splitlines():

        if not ligne.strip().startswith("--"):
            lignes_sql.append(ligne)

    query = "\n".join(lignes_sql)

    # Séparer les requêtes
    requetes = [
        requete.strip()
        for requete in query.split(";")
        if requete.strip()
    ]

    # Vérifier le nombre de requêtes SQL
    if len(requetes) != 8:
        raise ValueError(
            f"8 requêtes SQL attendues, {len(requetes)} trouvées."
        )

    # Stocker les DataFrames
    resultats = {}

    # Connexion SQLite en lecture seule
    with sqlite3.connect(
        f"file:{DB_FILE.as_posix()}?mode=ro",
        uri=True
    ) as conn:

        conn.execute("PRAGMA foreign_keys = ON")

        # Diagnostic temporaire : vérifier la base utilisée
        print("\nBASE SQL :", DB_FILE.resolve())

        print(
            "COMMANDES SQL :",
            conn.execute(
                "SELECT COUNT(*) FROM orders"
            ).fetchone()[0]
        )

        print(
            "LIGNES COMMANDES SQL :",
            conn.execute(
                "SELECT COUNT(*) FROM order_details"
            ).fetchone()[0]
        )

        # Exécuter toutes les requêtes
        for numero, requete in enumerate(requetes, start=1):

            # Diagnostic : afficher la requête exécutée
            print(f"\nQUESTION {numero}")
            print("REQUETE SQL :", repr(requete[:300]))

            # Exécuter la requête SQL
            df = pd.read_sql_query(requete, conn)

            # Diagnostic : afficher le résultat
            print(
                "RESULTAT :",
                df.head().to_string(index=False)
            )

            # Stocker le DataFrame
            resultats[f"question_{numero}"] = df

    return resultats


# 3. Exécution directe du script Python
if __name__ == "__main__":

    # Charger les huit résultats SQL
    resultats = charger_analyses()

    # Afficher chaque résultat
    for nom, df in resultats.items():
        print("\n" + "=" * 45)
        print(nom.upper().replace("_", " "))
        print("=" * 45)
        print(df.to_string(index=False))

    # Vérifier les dimensions des DataFrames
    print("\nDATAFRAMES DISPONIBLES :")

    for nom, df in resultats.items():
        print(f"{nom} : {df.shape}")

    # Explorer le chiffre d'affaires mensuel
    df_ca = resultats["question_6"].copy()

    print("\nEXPLORATION PANDAS - CA MENSUEL")
    print(df_ca.head())

    print("\nValeurs manquantes :")
    print(df_ca.isna().sum())

    # Convertir les mois en dates
    df_ca["mois"] = pd.to_datetime(
        df_ca["mois"],
        format="%Y-%m"
    )

    # Trier chronologiquement
    df_ca = df_ca.sort_values("mois")

    print("\nCA MENSUEL - DONNÉES PRÉPARÉES")
    print(df_ca.head())

    print("\nTypes après conversion :")
    print(df_ca.dtypes)

    print("\nToutes les analyses SQL sont terminées.")
