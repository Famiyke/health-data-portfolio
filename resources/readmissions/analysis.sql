-- result: national_trend
SELECT period, value AS risk_adjusted_rate_per_100
FROM data
WHERE dimension = 'national' AND indicator = 'Overall' AND value IS NOT NULL
ORDER BY period;

-- result: latest_province_comparison
SELECT "group" AS jurisdiction, value AS risk_adjusted_rate_per_100, ci_lower, ci_upper,
       ROUND(value - (SELECT value FROM data WHERE dimension='national' AND indicator='Overall' AND period='2025–2026'), 1) AS difference_from_canada_pp
FROM data
WHERE dimension = 'province' AND indicator='Overall' AND period='2025–2026' AND value IS NOT NULL
ORDER BY jurisdiction;

-- result: latest_patient_groups
SELECT indicator, value AS risk_adjusted_rate_per_100
FROM data WHERE dimension='national' AND period='2025–2026' AND indicator<>'Overall' AND value IS NOT NULL
ORDER BY indicator;

-- result: disclosure_audit
SELECT dimension, status, COUNT(*) AS records
FROM data GROUP BY dimension,status ORDER BY dimension,status;
