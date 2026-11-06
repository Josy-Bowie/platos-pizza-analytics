-- QUESTION MÉTIER 9 :
-- Quel est le chiffre d'affaires et le volume
-- de pizzas vendues par mois et par catégorie ?

SELECT
    strftime('%Y-%m', o.date) AS mois,
    pt.category AS categorie,

    SUM(od.quantity) AS pizzas_vendues,

    ROUND(
        SUM(od.quantity * p.price),
        2
    ) AS chiffre_affaires

FROM orders AS o

INNER JOIN order_details AS od
    ON o.order_id = od.order_id

INNER JOIN pizzas AS p
    ON od.pizza_id = p.pizza_id

INNER JOIN pizza_types AS pt
    ON p.pizza_type_id = pt.pizza_type_id

GROUP BY
    strftime('%Y-%m', o.date),
    pt.category

ORDER BY
    mois,
    categorie;