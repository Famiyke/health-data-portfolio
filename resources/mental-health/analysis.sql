-- result: national_change
SELECT old.indicator, old.value AS percent_2012, new.value AS percent_2022,
       ROUND(new.value-old.value,1) AS change_percentage_points
FROM data old JOIN data new ON old.indicator=new.indicator
  AND old.dimension=new.dimension AND old."group"=new."group"
WHERE old.dimension='national' AND old.period='2012' AND new.period='2022'
  AND old.value IS NOT NULL AND new.value IS NOT NULL
ORDER BY old.indicator;

-- result: age_comparison_2022
SELECT "group" AS age_group, value AS percentage, ci_lower, ci_upper, status
FROM data WHERE dimension='age' AND period='2022'
  AND indicator='Fair or poor perceived mental health'
ORDER BY age_group;

-- result: provincial_unmet_need_2022
SELECT "group" AS province, value AS percentage, ci_lower, ci_upper, status
FROM data WHERE dimension='province' AND period='2022'
  AND indicator='Mental health care needs not met'
ORDER BY province;

-- result: disclosure_audit
SELECT dimension,status,COUNT(*) AS records FROM data GROUP BY dimension,status ORDER BY dimension,status;
