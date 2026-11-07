
# =====================================================
# PROJET : PLATO'S PIZZA ANALYTICS
# MODULE : EXECUTION DES ANALYSES SQL
# =====================================================

import sqlite3
from pathlib import Path

import pandas as pd


# =====================================================
# 1. CHEMINS DU PROJET
# =====================================================

# Dossier racine du projet
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Base de données SQLite
DB_FILE = PROJECT_ROOT / "data" / "pizza.db"

# Fichier contenant les huit requêtes métier
SQL_FILE = PROJECT_ROOT / "sql" / "02_business_analysis.sql"


# =====================================================
# 2. FONCTION PRINCIPALE
# =====================================================

def charger_analyses():
    """
    Charge et exécute les huit requêtes SQL du projet.

    Retourne :
        Un dictionnaire contenant huit DataFrames Pandas.

    Exemple :
        resultats["question_1"]
        resultats["question_2"]
        ...
        resultats["question_8"]

    Un contrôle indépendant vérifie également
    la cohérence du chiffre d'affaires total.
    """

    # =================================================
    # ETAPE 1 : VERIFIER LES FICHIERS
    # =================================================

    if not DB_FILE.is_file():
        raise FileNotFoundError(
            f"Base SQLite introuvable : {DB_FILE}"
        )

    if not SQL_FILE.is_file():
        raise FileNotFoundError(
            f"Fichier SQL introuvable : {SQL_FILE}"
        )

    # =================================================
    # ETAPE 2 : LIRE LE FICHIER SQL
    # =================================================

    # utf-8-sig accepte les fichiers UTF-8 avec ou sans BOM.
    contenu_sql = SQL_FILE.read_text(
        encoding="utf-8-sig"
    )

    # Supprimer les lignes de commentaires SQL.
    lignes_sql = [
        ligne
        for ligne in contenu_sql.splitlines()
        if not ligne.strip().startswith("--")
    ]

    contenu_sql = "\n".join(lignes_sql)

    # Séparer les requêtes avec le point-virgule.
    requetes = [
        requete.strip()
        for requete in contenu_sql.split(";")
        if requete.strip()
    ]

    # Vérifier que les huit requêtes sont présentes.
    if len(requetes) != 8:
        raise ValueError(
            f"8 requêtes SQL attendues, "
            f"{len(requetes)} trouvées."
        )

    # Dictionnaire pour enregistrer les résultats.
    resultats = {}

    # =================================================
    # ETAPE 3 : OUVRIR LA CONNEXION SQLITE
    # =================================================

    # mode=ro : connexion en lecture seule.
    connexion = sqlite3.connect(
        DB_FILE.as_uri() + "?mode=ro",
        uri=True
    )

    try:

        # =============================================
        # ETAPE 4 : CONTROLER LE CHIFFRE D'AFFAIRES
        # =============================================

        # Calcul indépendant du chiffre d'affaires.
        ca_reference = connexion.execute(
            """
            SELECT ROUND(
                SUM(od.quantity * p.price),
                2
            )
            FROM order_details AS od
            INNER JOIN pizzas AS p
                ON od.pizza_id = p.pizza_id
            """
        ).fetchone()[0]

        # Vérifier que le calcul retourne une valeur.
        if ca_reference is None:
            raise ValueError(
                "Le chiffre d'affaires de référence "
                "est NULL. Vérifier les données SQLite."
            )

        # =============================================
        # ETAPE 5 : EXECUTER LES HUIT REQUETES
        # =============================================

        for numero, requete in enumerate(
            requetes,
            start=1
        ):

            # Exécuter la requête SQL.
            # Pandas transforme le résultat en DataFrame.
            df = pd.read_sql_query(
                requete,
                connexion
            )

            # =========================================
            # CONTROLE SPECIFIQUE DE LA QUESTION 1
            # =========================================

            if numero == 1:

                # Vérifier la présence du résultat.
                if df.empty:
                    raise ValueError(
                        "La question 1 ne retourne "
                        "aucune ligne."
                    )

                # Vérifier la colonne attendue.
                if "chiffre_affaires_total" not in df.columns:
                    raise ValueError(
                        "Colonne chiffre_affaires_total "
                        "absente de la question 1."
                    )

                # Récupérer le chiffre d'affaires SQL.
                valeur_ca = df[
                    "chiffre_affaires_total"
                ].iloc[0]

                # Vérifier les valeurs manquantes.
                if pd.isna(valeur_ca):
                    raise ValueError(
                        "Le chiffre d'affaires SQL "
                        "est NULL."
                    )

                # Comparer le CA SQL au calcul indépendant.
                ecart_ca = abs(
                    float(valeur_ca)
                    - float(ca_reference)
                )

                if ecart_ca > 0.01:
                    raise ValueError(
                        "Incohérence entre le chiffre "
                        "d'affaires SQL et le chiffre "
                        "d'affaires de référence."
                    )

            # =========================================
            # ENREGISTRER LE RESULTAT
            # =========================================

            resultats[f"question_{numero}"] = df

    finally:

        # =================================================
        # ETAPE 6 : FERMER LA CONNEXION SQLITE
        # =================================================

        # Cette instruction est exécutée même
        # lorsqu'une erreur survient.
        connexion.close()

    # =================================================
    # ETAPE 7 : RETOURNER LES RESULTATS
    # =================================================

    return resultats


# =====================================================
# 3. TEST DU MODULE EN EXECUTION DIRECTE
# =====================================================

# Ce bloc s'exécute uniquement lorsque le fichier
# est lancé directement depuis le terminal.
#
# Il ne s'exécute pas lorsque Streamlit importe
# la fonction charger_analyses().

if __name__ == "__main__":

    resultats = charger_analyses()

    print("\nAnalyses SQL exécutées avec succès.")
    print("-" * 40)

    for nom, df in resultats.items():
        print(
            f"{nom} : "
            f"{df.shape[0]} lignes, "
            f"{df.shape[1]} colonnes"
        )

    print("-" * 40)
    print("Les huit analyses SQL sont terminées.")
