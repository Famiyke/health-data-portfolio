-- result: latest_regional_diabetes
SELECT r."group" AS health_region, r.value AS percent, r.ci_lower, r.ci_upper,
       ROUND(r.value-p.value,1) AS difference_from_manitoba_pp
FROM data r JOIN data p ON r.indicator=p.indicator AND r.period=p.period
WHERE r.dimension='region_survey' AND p.dimension='province_survey'
  AND r.indicator='Self-reported diabetes' AND r.period='2023/2024' AND r.value IS NOT NULL
ORDER BY health_region;

-- result: ed_income_gaps
SELECT setting,
       MAX(CASE WHEN quintile=1 THEN value END) AS visits_per_1000_lowest,
       MAX(CASE WHEN quintile=5 THEN value END) AS visits_per_1000_highest,
       ROUND(MAX(CASE WHEN quintile=1 THEN value END)/MAX(CASE WHEN quintile=5 THEN value END),2) AS rate_ratio_lowest_to_highest
FROM (
  SELECT CASE WHEN "group" LIKE 'Rural%' THEN 'Rural' ELSE 'Urban' END AS setting,
         CAST(SUBSTR("group",-1) AS INTEGER) AS quintile,value
  FROM data WHERE indicator='Emergency department visits' AND dimension='income' AND period='2023'
) q GROUP BY setting ORDER BY setting;

-- result: heart_attack_region
SELECT "group" AS health_region, value AS rate_per_1000_adults_40_plus, source_ref
FROM data WHERE indicator='Heart attack hospitalizations and deaths'
  AND dimension='region_admin' AND period='2018–2022' ORDER BY health_region;

-- result: source_audit
SELECT source_id, COUNT(*) AS records FROM data GROUP BY source_id ORDER BY source_id;
