-- Projet : Plato's Pizza Analytics
-- Étape 4 : Création de la base SQLite
-- Table 1 : orders

CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,
    time TEXT NOT NULL
);

-- ==========================================
-- TABLE 2 : PIZZA_TYPES
-- Informations sur les types de pizzas
-- ==========================================

CREATE TABLE IF NOT EXISTS pizza_types (
    pizza_type_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    ingredients TEXT NOT NULL
);

-- ==========================================
-- TABLE 3 : PIZZAS
-- Références, tailles et prix des pizzas
-- ==========================================

CREATE TABLE IF NOT EXISTS pizzas (
    pizza_id TEXT PRIMARY KEY,
    pizza_type_id TEXT NOT NULL,
    size TEXT NOT NULL,
    price REAL NOT NULL,

    FOREIGN KEY (pizza_type_id)
        REFERENCES pizza_types(pizza_type_id)
);

-- ==========================================
-- TABLE 4 : ORDER_DETAILS
-- Détails des pizzas vendues par commande
-- ==========================================

CREATE TABLE IF NOT EXISTS order_details (
    order_details_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    pizza_id TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),

    FOREIGN KEY (order_id)
        REFERENCES orders(order_id),

    FOREIGN KEY (pizza_id)
        REFERENCES pizzas(pizza_id)
);