-- Separate grains and units: never sum wage/rate estimates or add overlapping sectors.
-- Latest Canadian labour market snapshot, selected industries.
SELECT dimension, metric, value, unit, status FROM observations
WHERE source_file='workforce-statcan.zip' AND geography='Canada' AND period=(SELECT MAX(period) FROM observations WHERE source_file='workforce-statcan.zip')
ORDER BY dimension,metric;
-- Same-quarter vacancy-rate comparison, 2025 versus 2026.
WITH rates AS (SELECT geography, dimension, period, value FROM observations WHERE metric='Job vacancy rate' AND period IN ('2025 Q2','2026 Q2'))
SELECT current.geography,current.dimension,ROUND(previous.value,1) AS rate_2025,ROUND(current.value,1) AS rate_2026,ROUND(current.value-previous.value,1) AS change_pp
FROM rates current JOIN rates previous ON current.geography=previous.geography AND current.dimension=previous.dimension
WHERE current.period='2026 Q2' AND previous.period='2025 Q2' AND current.value IS NOT NULL AND previous.value IS NOT NULL ORDER BY change_pp DESC;
-- Paid sick leave hours per calculated hospital FTE, totals only.
SELECT a.geography,a.period,ROUND(a.value/NULLIF(b.value,0),2) AS sick_hours_per_fte
FROM observations a JOIN observations b ON a.source_id=b.source_id AND a.period=b.period AND a.geography=b.geography AND a.dimension=b.dimension
WHERE a.metric='Paid sick leave hours' AND b.metric='Calculated FTEs' AND a.dimension='Total' AND a.value IS NOT NULL AND b.value>0 ORDER BY a.period,a.geography;
-- Health supply density by selected profession and jurisdiction.
SELECT geography,dimension,period,value,status FROM observations WHERE metric='Supply per 100,000' AND period='2024' ORDER BY dimension,geography;
