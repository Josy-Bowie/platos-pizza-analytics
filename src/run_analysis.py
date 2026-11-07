
import sqlite3
from pathlib import Path

import pandas as pd


# ============================================
# 1. CHEMINS DU PROJET
# ============================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_FILE = PROJECT_ROOT / "data" / "pizza.db"
SQL_FILE = PROJECT_ROOT / "sql" / "02_business_analysis.sql"


# ============================================
# 2. CHARGEMENT DES ANALYSES SQL
# ============================================

def charger_analyses():

    # Vérifier les fichiers nécessaires
    if not DB_FILE.exists():
        raise FileNotFoundError(
            f"Base SQLite introuvable : {DB_FILE}"
        )

    if not SQL_FILE.exists():
        raise FileNotFoundError(
            f"Fichier SQL introuvable : {SQL_FILE}"
        )

    # Lire le fichier SQL
    contenu_sql = SQL_FILE.read_text(
        encoding="utf-8"
    )

    # Supprimer les commentaires commençant par --
    lignes_sql = [
        ligne
        for ligne in contenu_sql.splitlines()
        if not ligne.strip().startswith("--")
    ]

    contenu_sql = "\n".join(lignes_sql)

    # Séparer les huit requêtes
    requetes = [
        requete.strip()
        for requete in contenu_sql.split(";")
        if requete.strip()
    ]

    if len(requetes) != 8:
        raise ValueError(
            f"8 requêtes attendues, {len(requetes)} trouvées."
        )

    resultats = {}

    # Ouvrir la base SQLite
    with sqlite3.connect(
        f"file:{DB_FILE.as_posix()}?mode=ro",
        uri=True
    ) as conn:

        # Vérification du calcul direct
        chiffre_affaires_direct = conn.execute("""
            SELECT ROUND(SUM(od.quantity * p.price), 2)
            FROM order_details AS od
            INNER JOIN pizzas AS p
                ON od.pizza_id = p.pizza_id
        """).fetchone()[0]

        print(
            "Chiffre d'affaires direct :",
            chiffre_affaires_direct
        )

        # Exécuter les huit requêtes métier
        for numero, requete in enumerate(
            requetes,
            start=1
        ):

            df = pd.read_sql_query(
                requete,
                conn
            )

            resultats[f"question_{numero}"] = df

            print(
                f"Question {numero} :",
                df.shape
            )

            # Vérifier les résultats de la question 1
            if numero == 1:
                print(
                    "Résultat SQL question 1 :"
                )
                print(df.to_string(index=False))

    return resultats


# ============================================
# 3. EXÉCUTION DIRECTE
# ============================================

if __name__ == "__main__":

    resultats = charger_analyses()

    for nom, df in resultats.items():

        print("\n" + "=" * 45)
        print(nom.upper())
        print("=" * 45)

        print(df.to_string(index=False))

    print("\nAnalyses SQL terminées.")
