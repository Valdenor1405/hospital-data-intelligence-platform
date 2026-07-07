-- KPIs por setor
SELECT setor, COUNT(*) AS atendimentos, ROUND(AVG(custo_total),2) AS custo_medio, ROUND(AVG(dias_internacao),2) AS dias_medios, ROUND(AVG(readmissao_30_dias)*100,2) AS taxa_readmissao_pct
FROM fato_atendimentos
GROUP BY setor
ORDER BY taxa_readmissao_pct DESC;
