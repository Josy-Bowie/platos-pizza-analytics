
import sqlite3
import pandas as pd
from pathlib import Path

# 1. Localiser les fichiers du projet
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DB_FILE = PROJECT_ROOT / "data" / "pizza.db"
SQL_FILE = PROJECT_ROOT / "sql" / "03_dashboard_filters.sql"

# 2. Lire notre requête SQL
query = SQL_FILE.read_text(encoding="utf-8")

# 3. Exécuter la requête sur SQLite
with sqlite3.connect(
    f"file:{DB_FILE.as_posix()}?mode=ro",
    uri=True
) as conn:
    df = pd.read_sql_query(query, conn)

# 4. Examiner les résultats
print("\nAPERÇU DES DONNÉES")
print(df.head(10).to_string(index=False))

print("\nDIMENSIONS DU DATAFRAME")
print(df.shape)

print("\nVALEURS MANQUANTES")
print(df.isna().sum())

# 5. Vérifier les indicateurs
print("\nCONTRÔLE DES TOTAUX")
print("Chiffre d'affaires :", round(df["chiffre_affaires"].sum(), 2))
print("Pizzas vendues :", df["pizzas_vendues"].sum())

# 6. Vérifier les mois et catégories
print("\nMOIS DISPONIBLES")
print(sorted(df["mois"].unique()))

print("\nCATÉGORIES DISPONIBLES")
print(sorted(df["categorie"].unique()))

# 7. Vérifier les combinaisons uniques
print("\nDOUBLONS MOIS / CATÉGORIE")
print(df.duplicated(subset=["mois", "categorie"]).sum())
