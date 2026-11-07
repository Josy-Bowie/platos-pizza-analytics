
import sqlite3
from pathlib import Path

import pandas as pd


# =====================================================
# 1. CHEMINS DU PROJET
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DB_FILE = PROJECT_ROOT / "data" / "pizza.db"

SQL_FILE = PROJECT_ROOT / "sql" / "02_business_analysis.sql"


# =====================================================
# 2. CHARGEMENT DES ANALYSES SQL
# =====================================================

def charger_analyses():

    # Vérifier la présence des fichiers
    if not DB_FILE.is_file():
        raise FileNotFoundError(
            f"Base SQLite introuvable : {DB_FILE}"
        )

    if not SQL_FILE.is_file():
        raise FileNotFoundError(
            f"Fichier SQL introuvable : {SQL_FILE}"
        )

    # Lire les requêtes SQL
    contenu_sql = SQL_FILE.read_text(
        encoding="utf-8-sig"
    )

    # Supprimer les lignes de commentaires SQL
    lignes_sql = []

    for ligne in contenu_sql.splitlines():

        if not ligne.strip().startswith("--"):
            lignes_sql.append(ligne)

    contenu_sql = "\n".join(lignes_sql)

    # Séparer les requêtes grâce au point-virgule
    requetes = [
        requete.strip()
        for requete in contenu_sql.split(";")
        if requete.strip()
    ]

    # Vérifier que les huit requêtes sont présentes
    if len(requetes) != 8:
        raise ValueError(
            f"8 requêtes SQL attendues, "
            f"{len(requetes)} trouvées."
        )

    resultats = {}

    # =================================================
    # 3. CONNEXION À LA BASE SQLITE
    # =================================================

    connexion = sqlite3.connect(
        DB_FILE.as_uri() + "?mode=ro",
        uri=True
    )

    try:

        # Vérifier le contenu de la base
        nombre_commandes = connexion.execute(
            "SELECT COUNT(*) FROM orders"
        ).fetchone()[0]

        nombre_lignes = connexion.execute(
            "SELECT COUNT(*) FROM order_details"
        ).fetchone()[0]

        print("BASE SQLITE :", DB_FILE)
        print("COMMANDES :", nombre_commandes)
        print("LIGNES DE VENTE :", nombre_lignes)

        # Calcul de référence indépendant
        ca_reference = connexion.execute("""
            SELECT ROUND(
                SUM(od.quantity * p.price), 2
            )
            FROM order_details AS od
            INNER JOIN pizzas AS p
                ON od.pizza_id = p.pizza_id
        """).fetchone()[0]

        print("CA DE REFERENCE :", ca_reference)

        # =================================================
        # 4. EXECUTION DES HUIT REQUETES
        # =================================================

        for numero, requete in enumerate(
            requetes,
            start=1
        ):

            print(f"\nEXECUTION QUESTION {numero}")

            # Afficher la requête SQL réellement exécutée
            print("REQUETE SQL :")
            print(requete)

            # Exécuter la requête
            df = pd.read_sql_query(
                requete,
                connexion
            )

            print("DIMENSIONS :", df.shape)

            print("RESULTAT :")
            print(df.head().to_string(index=False))

            # Contrôler la première analyse
            if numero == 1:

                if df.empty:
                    raise ValueError(
                        "La question 1 ne retourne aucune ligne."
                    )

                valeur_ca = df[
                    "chiffre_affaires_total"
                ].iloc[0]

                if pd.isna(valeur_ca):
                    raise ValueError(
                        "La question 1 retourne NULL. "
                        f"CA direct de référence : {ca_reference}. "
                        "Vérifier le contenu de "
                        "sql/02_business_analysis.sql."
                    )

                if ca_reference is not None:

                    if abs(
                        float(valeur_ca) -
                        float(ca_reference)
                    ) > 0.01:

                        raise ValueError(
                            "Incohérence entre le CA SQL "
                            "et le CA de référence."
                        )

            # Stocker le DataFrame
            resultats[f"question_{numero}"] = df

        return resultats

    finally:

        # Toujours fermer la connexion
        connexion.close()


# =====================================================
# 5. EXECUTION DIRECTE
# =====================================================

if __name__ == "__main__":

    resultats = charger_analyses()

    print("\n" + "=" * 45)
    print("RESULTATS DES ANALYSES")
    print("=" * 45)

    for nom, df in resultats.items():

        print(f"\n{nom.upper()}")
        print(df.to_string(index=False))

    print("\nToutes les analyses SQL sont terminées.")
