-- Retail data are nominal CAD thousands. Adjusted and unadjusted series remain separate.
SELECT geography,period,ROUND(value/1000000,3) AS retail_cad_billions,status FROM observations WHERE dimension='Seasonally adjusted' AND period='2026-09' ORDER BY value DESC;
-- Same-month YoY sales growth for September 2026.
SELECT a.geography,a.period,ROUND((a.value/NULLIF(b.value,0)-1)*100,2) AS yoy_percent FROM observations a JOIN observations b ON a.geography=b.geography AND a.dimension=b.dimension AND a.metric=b.metric WHERE a.dimension='Unadjusted' AND a.period='2026-09' AND b.period='2025-09' ORDER BY yoy_percent DESC;
-- Independently recompute holdout WAPE and MAE from predictions.
SELECT geography,model,ROUND(100*SUM(ABS(actual_cad_thousands-forecast_cad_thousands))/SUM(ABS(actual_cad_thousands)),6) AS wape_percent,ROUND(AVG(ABS(actual_cad_thousands-forecast_cad_thousands))/1000,6) AS mae_cad_millions FROM backtest WHERE phase='Holdout' GROUP BY geography,model ORDER BY geography,wape_percent;
-- Forecast records are intentionally separate from observed sales.
SELECT geography,month,model,ROUND(forecast_cad_thousands/1000000,3) AS forecast_cad_billions,training_through FROM forecasts ORDER BY geography,month;
