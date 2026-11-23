-- The source cohort contains C instrument records with original value above CAD 10,000.
-- All sums are exact integer cents. These are disclosed award values, not expenditure.
-- 1. Annual selected-entity profile.
SELECT fiscal_year, entity, COUNT(*) AS disclosure_records, SUM(original_value_cents) AS original_value_cents FROM contracts GROUP BY 1,2 ORDER BY 1,2;
-- 2. Quarterly trend by reporting period.
SELECT reporting_period, entity, COUNT(*) AS disclosure_records, SUM(original_value_cents) AS original_value_cents FROM contracts GROUP BY 1,2 ORDER BY 1,2;
-- 3. Procurement route mix.
SELECT fiscal_year, entity, solicitation, COUNT(*) AS disclosure_records, SUM(original_value_cents) AS original_value_cents FROM contracts GROUP BY 1,2,3 ORDER BY 1,2,3;
-- 4. Commodity mix.
SELECT fiscal_year, entity, commodity, COUNT(*) AS disclosure_records, SUM(original_value_cents) AS original_value_cents FROM contracts GROUP BY 1,2,3 ORDER BY 1,2,3;
-- 5. Top-five supplier-name concentration by entity and fiscal year.
WITH vendor AS (SELECT fiscal_year,entity,supplier_group,SUM(original_value_cents) AS value_cents FROM contracts GROUP BY 1,2,3), ranked AS (SELECT *,ROW_NUMBER() OVER(PARTITION BY fiscal_year,entity ORDER BY value_cents DESC,supplier_group) AS supplier_rank FROM vendor) SELECT fiscal_year,entity,COUNT(*) AS supplier_name_groups,SUM(value_cents) AS total_value_cents,SUM(CASE WHEN supplier_rank<=5 THEN value_cents ELSE 0 END) AS top5_value_cents,ROUND(100.0*SUM(CASE WHEN supplier_rank<=5 THEN value_cents ELSE 0 END)/SUM(value_cents),6) AS top5_share_percent FROM ranked GROUP BY 1,2 ORDER BY 1,2;
