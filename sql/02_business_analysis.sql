-- QUESTION MÉTIER 1 :
-- Quel est le chiffre d'affaires total ?

SELECT
    ROUND(SUM(od.quantity * p.price), 2)
        AS chiffre_affaires_total

FROM order_details AS od

INNER JOIN pizzas AS p
    ON od.pizza_id = p.pizza_id;


    -- QUESTION MÉTIER 2 :
-- Quel est le panier moyen par commande ?

SELECT
    ROUND(
        SUM(od.quantity * p.price)
        / COUNT(DISTINCT od.order_id),
        2
    ) AS panier_moyen

FROM order_details AS od

INNER JOIN pizzas AS p
    ON od.pizza_id = p.pizza_id;


    -- QUESTION MÉTIER 3 :
-- Combien de pizzas ont été vendues au total ?

SELECT
    SUM(quantity) AS total_pizzas_vendues
FROM order_details;


-- QUESTION MÉTIER 4 :
-- Quelles sont les 10 pizzas les plus vendues ?

SELECT
    pt.name AS nom_pizza,
    SUM(od.quantity) AS quantite_vendue

FROM order_details AS od

INNER JOIN pizzas AS p
    ON od.pizza_id = p.pizza_id

INNER JOIN pizza_types AS pt
    ON p.pizza_type_id = pt.pizza_type_id

GROUP BY pt.name

ORDER BY quantite_vendue DESC

LIMIT 10;


-- QUESTION MÉTIER 5 :
-- Quel est le chiffre d'affaires par catégorie de pizza ?

SELECT
    pt.category AS categorie,
    ROUND(SUM(od.quantity * p.price), 2) AS chiffre_affaires

FROM order_details AS od

INNER JOIN pizzas AS p
    ON od.pizza_id = p.pizza_id

INNER JOIN pizza_types AS pt
    ON p.pizza_type_id = pt.pizza_type_id

GROUP BY pt.category

ORDER BY chiffre_affaires DESC;


-- QUESTION MÉTIER 6 :
-- Comment évolue le chiffre d'affaires par mois ?

SELECT
    strftime('%Y-%m', o.date) AS mois,
    ROUND(
        SUM(od.quantity * p.price),
        2
    ) AS chiffre_affaires

FROM orders AS o

INNER JOIN order_details AS od
    ON o.order_id = od.order_id

INNER JOIN pizzas AS p
    ON od.pizza_id = p.pizza_id

GROUP BY strftime('%Y-%m', o.date)

ORDER BY mois ASC;


-- QUESTION MÉTIER 7 :
-- Quel est le chiffre d'affaires par jour de la semaine ?

SELECT
    CASE strftime('%w', o.date)
        WHEN '0' THEN 'Dimanche'
        WHEN '1' THEN 'Lundi'
        WHEN '2' THEN 'Mardi'
        WHEN '3' THEN 'Mercredi'
        WHEN '4' THEN 'Jeudi'
        WHEN '5' THEN 'Vendredi'
        WHEN '6' THEN 'Samedi'
    END AS jour_semaine,

    COUNT(DISTINCT o.order_id) AS nombre_commandes,

    ROUND(
        SUM(od.quantity * p.price),
        2
    ) AS chiffre_affaires

FROM orders AS o

INNER JOIN order_details AS od
    ON o.order_id = od.order_id

INNER JOIN pizzas AS p
    ON od.pizza_id = p.pizza_id

GROUP BY strftime('%w', o.date)

ORDER BY strftime('%w', o.date);



-- QUESTION MÉTIER 8 :
-- À quelles heures les commandes sont-elles
-- les plus nombreuses ?

SELECT
    strftime('%H', time) AS heure,

    COUNT(order_id) AS nombre_commandes

FROM orders

GROUP BY strftime('%H', time)

ORDER BY heure ASC;
