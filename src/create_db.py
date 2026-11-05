
import pandas as pd


# Projet : Plato's Pizza Analytics
# Étape 4 : Création de la base SQLite

# 1. Importer les modules nécessaires
import sqlite3
from pathlib import Path

# 2. Identifier la racine du projet
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 3. Définir le chemin du script SQL
SQL_FILE = PROJECT_ROOT / "sql" / "01_create_tables.sql"

# 4. Définir le chemin de la base SQLite
DB_FILE = PROJECT_ROOT / "data" / "pizza.db"


# Dossier contenant les quatre fichiers CSV
DATA_RAW = PROJECT_ROOT / "data" / "raw"


# 5. Afficher les chemins pour vérification
print("Dossier du projet :", PROJECT_ROOT)
print("Fichier SQL :", SQL_FILE)
print("Base SQLite :", DB_FILE)

# 6. Créer le dossier data s'il n'existe pas
DB_FILE.parent.mkdir(parents=True, exist_ok=True)

# 7. Créer la connexion à SQLite
conn = sqlite3.connect(DB_FILE)

print("Connexion SQLite établie !")

# 8. Activer les contraintes de clés étrangères
conn.execute("PRAGMA foreign_keys = ON;")

print("Contraintes de clés étrangères activées !")

# 9. Vérifier que les clés étrangères sont activées
resultat = conn.execute("PRAGMA foreign_keys;").fetchone()

print("Clés étrangères activées :", resultat[0] == 1)


# 10. Lire le contenu du fichier SQL
sql_script = SQL_FILE.read_text(encoding="utf-8")

print("Fichier SQL chargé avec succès !")


# 11. Exécuter les instructions SQL
conn.executescript(sql_script)

print("Tables SQL créées avec succès !")


# 12. Vérifier les tables présentes dans SQLite
tables = conn.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
    ORDER BY name;
""").fetchall()

print("\nTABLES PRÉSENTES DANS LA BASE :")

for table in tables:
    print("-", table[0])


# 13. Charger les types de pizzas depuis le CSV
df_pizza_types = pd.read_csv(
    DATA_RAW / "pizza_types.csv",
    encoding="cp1252"
)

print("\nAPERÇU DES TYPES DE PIZZAS :")
print(df_pizza_types.head())

print("Nombre de lignes :", len(df_pizza_types))


# 14. Vérifier si la table pizza_types contient déjà des données
nombre_existant = conn.execute(
    "SELECT COUNT(*) FROM pizza_types"
).fetchone()[0]

print("Lignes déjà présentes dans SQLite :", nombre_existant)

# 15. Importer les données uniquement si la table est vide
if nombre_existant == 0:

    df_pizza_types.to_sql(
        name="pizza_types",
        con=conn,
        if_exists="append",
        index=False
    )

    print("Importation des types de pizzas terminée !")

elif nombre_existant == len(df_pizza_types):

    print("Importation ignorée : volume déjà complet.")

else:

    raise ValueError(
        f"Importation incomplète dans pizza_types : "
        f"{nombre_existant} lignes présentes "
        f"sur {len(df_pizza_types)} attendues."
    )



# 16. Vérifier le nombre de lignes après importation
total_sql = conn.execute(
    "SELECT COUNT(*) FROM pizza_types"
).fetchone()[0]

print("\nVÉRIFICATION DE L'IMPORTATION")
print("Nombre de lignes dans le CSV :", len(df_pizza_types))
print("Nombre de lignes dans SQLite :", total_sql)

if total_sql == len(df_pizza_types):
    print("Contrôle réussi : les volumes correspondent.")
else:
    print("Attention : les volumes ne correspondent pas.")


# 17. Charger les commandes depuis le CSV
df_orders = pd.read_csv(
    DATA_RAW / "orders.csv"
)

print("\nAPERÇU DES COMMANDES :")
print(df_orders.head())

print("Nombre de commandes dans le CSV :", len(df_orders))


# 18. Vérifier si la table orders est vide
nombre_orders = conn.execute(
    "SELECT COUNT(*) FROM orders"
).fetchone()[0]

print("Commandes déjà présentes dans SQLite :", nombre_orders)

# 19. Importer les commandes si la table est vide
if nombre_orders == 0:

    df_orders.to_sql(
        name="orders",
        con=conn,
        if_exists="append",
        index=False
    )

    print("Importation des commandes terminée !")

elif nombre_orders == len(df_orders):
    print("Importation ignorée : volume déjà complet.")
else:
    raise ValueError(
        f"Importation incomplète dans orders : "
        f"{nombre_orders} lignes sur {len(df_orders)} attendues."
    )


# 20. Vérifier le nombre de commandes importées
total_orders_sql = conn.execute(
    "SELECT COUNT(*) FROM orders"
).fetchone()[0]

print("\nVÉRIFICATION DES COMMANDES")
print("Commandes dans le CSV :", len(df_orders))
print("Commandes dans SQLite :", total_orders_sql)

if total_orders_sql == len(df_orders):
    print("Contrôle réussi : les volumes correspondent.")
else:
    print("Attention : les volumes ne correspondent pas.")



# 21. Charger les références des pizzas
df_pizzas = pd.read_csv(
    DATA_RAW / "pizzas.csv"
)

print("\nAPERÇU DES PIZZAS :")
print(df_pizzas.head())

print("Nombre de pizzas dans le CSV :", len(df_pizzas))



# 22. Vérifier si la table pizzas est vide
nombre_pizzas = conn.execute(
    "SELECT COUNT(*) FROM pizzas"
).fetchone()[0]

print("Pizzas déjà présentes dans SQLite :", nombre_pizzas)

# 23. Importer uniquement si la table est vide
if nombre_pizzas == 0:

    df_pizzas.to_sql(
        name="pizzas",
        con=conn,
        if_exists="append",
        index=False
    )

    print("Importation des pizzas terminée !")

elif nombre_pizzas == len(df_pizzas):
    print("Importation ignorée : volume déjà complet.")
else:
    raise ValueError(
        f"Importation incomplète dans pizzas : "
        f"{nombre_pizzas} lignes sur {len(df_pizzas)} attendues."
    )


# 24. Contrôler le volume importé
total_pizzas_sql = conn.execute(
    "SELECT COUNT(*) FROM pizzas"
).fetchone()[0]

print("\nVÉRIFICATION DES PIZZAS")
print("Pizzas dans le CSV :", len(df_pizzas))
print("Pizzas dans SQLite :", total_pizzas_sql)

if total_pizzas_sql == len(df_pizzas):
    print("Contrôle réussi : les volumes correspondent.")
else:
    print("Attention : les volumes ne correspondent pas.")


# 25. Charger les détails des commandes

df_order_details = pd.read_csv(
    DATA_RAW / "order_details.csv"
)

print("\nAPERÇU DES DÉTAILS DES COMMANDES")
print(df_order_details.head())

print(
    "Nombre de lignes dans le CSV :",
    len(df_order_details)
)


# 26. Vérifier les données parentes

total_orders = conn.execute(
    "SELECT COUNT(*) FROM orders"
).fetchone()[0]

total_pizzas = conn.execute(
    "SELECT COUNT(*) FROM pizzas"
).fetchone()[0]

print("Commandes disponibles :", total_orders)
print("Pizzas disponibles :", total_pizzas)

if total_orders != 21350 or total_pizzas != 96:
    raise ValueError(
        "Importation arrêtée : vérifier les tables orders et pizzas."
    )



# 27. Vérifier si order_details contient déjà des données

nombre_details = conn.execute(
    "SELECT COUNT(*) FROM order_details"
).fetchone()[0]

print("Lignes déjà présentes :", nombre_details)

# Nombre de lignes attendu dans le CSV
nombre_attendu = len(df_order_details)

if nombre_details == 0:

    # La table est vide : on importe les données
    df_order_details.to_sql(
        name="order_details",
        con=conn,
        if_exists="append",
        index=False
    )

    print("Importation des détails terminée !")

elif nombre_details == nombre_attendu:

    # Le volume est déjà complet
    print("Importation ignorée : volume déjà complet.")

else:

    # Le volume est différent du volume attendu
    raise ValueError(
        f"Importation incomplète : "
        f"{nombre_details} lignes présentes "
        f"sur {nombre_attendu} attendues."
    )



# 28. Vérifier le nombre de lignes importées

total_details_sql = conn.execute(
    "SELECT COUNT(*) FROM order_details"
).fetchone()[0]

print("\nVÉRIFICATION DES DÉTAILS")

print("Lignes dans le CSV :", len(df_order_details))
print("Lignes dans SQLite :", total_details_sql)

if total_details_sql == len(df_order_details):
    print("Contrôle réussi : les volumes correspondent.")
else:
    print("Attention : les volumes ne correspondent pas.")


# 29. Vérifier l'intégrité référentielle

print("\nCONTRÔLE DES CLÉS ÉTRANGÈRES")

erreurs_fk = conn.execute(
    "PRAGMA foreign_key_check;"
).fetchall()

print("Nombre de violations :", len(erreurs_fk))

if len(erreurs_fk) == 0:
    print("Contrôle réussi : aucune violation détectée.")
else:
    print("Attention : violations détectées !")
    for erreur in erreurs_fk:
        print(erreur)



# 30. Vérifier l'unicité des identifiants

print("\nCONTRÔLE DE L'UNICITÉ")

cles_primaires = {
    "orders": "order_id",
    "order_details": "order_details_id",
    "pizzas": "pizza_id",
    "pizza_types": "pizza_type_id"
}

for table, identifiant in cles_primaires.items():

    resultat = conn.execute(
        f"""
        SELECT
            COUNT(*) AS total_lignes,
            COUNT(DISTINCT {identifiant}) AS total_uniques
        FROM {table}
        """
    ).fetchone()

    print(
        f"{table} : {resultat[0]} lignes, "
        f"{resultat[1]} identifiants uniques"
    )



# 31. Vérifier les quantités vendues

print("\nCONTRÔLE DES QUANTITÉS")

quantites_invalides = conn.execute(
    """
    SELECT COUNT(*)
    FROM order_details
    WHERE quantity <= 0 OR quantity IS NULL
    """
).fetchone()[0]

print("Quantités invalides :", quantites_invalides)

if quantites_invalides == 0:
    print("Contrôle réussi : quantités valides.")
else:
    print("Attention : quantités invalides détectées.")




# 32. Fermer la connexion
conn.close()

print("Connexion SQLite fermée.")