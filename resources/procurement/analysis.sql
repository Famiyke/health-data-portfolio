-- The cohort contains C instrument records with original value above CAD 10,000.
-- All sums use integer cents. Award commitments differ from actual expenditure.

-- Annual profile by reporting entity.
SELECT fiscal_year, entity,
    COUNT(*) AS disclosure_records,
    SUM(original_value_cents) AS original_value_cents
FROM contracts
GROUP BY fiscal_year, entity
ORDER BY fiscal_year, entity;

-- Quarterly totals by reporting entity.
SELECT reporting_period, entity,
    COUNT(*) AS disclosure_records,
    SUM(original_value_cents) AS original_value_cents
FROM contracts
GROUP BY reporting_period, entity
ORDER BY reporting_period, entity;

-- Procurement route mix.
SELECT fiscal_year, entity, solicitation,
    COUNT(*) AS disclosure_records,
    SUM(original_value_cents) AS original_value_cents
FROM contracts
GROUP BY fiscal_year, entity, solicitation
ORDER BY fiscal_year, entity, solicitation;

-- Commodity mix.
SELECT fiscal_year, entity, commodity,
    COUNT(*) AS disclosure_records,
    SUM(original_value_cents) AS original_value_cents
FROM contracts
GROUP BY fiscal_year, entity, commodity
ORDER BY fiscal_year, entity, commodity;

-- Top-five supplier-name concentration by entity and fiscal year.
WITH vendor AS (
    SELECT fiscal_year, entity, supplier_group,
        SUM(original_value_cents) AS value_cents
    FROM contracts
    GROUP BY fiscal_year, entity, supplier_group
), ranked AS (
    SELECT *, ROW_NUMBER() OVER (
        PARTITION BY fiscal_year, entity
        ORDER BY value_cents DESC, supplier_group
    ) AS supplier_rank
    FROM vendor
)
SELECT fiscal_year, entity,
    COUNT(*) AS supplier_name_groups,
    SUM(value_cents) AS total_value_cents,
    SUM(CASE WHEN supplier_rank <= 5 THEN value_cents ELSE 0 END) AS top5_value_cents,
    ROUND(100.0 * SUM(CASE WHEN supplier_rank <= 5 THEN value_cents ELSE 0 END)
        / SUM(value_cents), 6) AS top5_share_percent
FROM ranked
GROUP BY fiscal_year, entity
ORDER BY fiscal_year, entity;
