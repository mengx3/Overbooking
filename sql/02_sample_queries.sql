--Q1
SELECT
    p.policy_name,
    AVG(s.total_bumped) AS avg_bumped,
    AVG(s.total_cost)   AS avg_cost
FROM scenario_stats s
JOIN policy p ON s.policy_id = p.policy_id
GROUP BY p.policy_name
ORDER BY avg_cost;

-- Q2
SELECT
    s.scenario_id,
    p.policy_name,
    s.total_cost,
    s.total_bumped,
    s.total_cost - MIN(s.total_cost) OVER (PARTITION BY s.scenario_id)
        AS cost_above_best
FROM scenario_stats s
JOIN policy p ON s.policy_id = p.policy_id
ORDER BY s.scenario_id, s.total_cost;

-- Q3
SELECT
    sr.scenario_id,
    sr.total_cost  AS random_cost,
    sf.total_cost  AS fifo_cost,
    ROUND((sf.total_cost - sr.total_cost) / sf.total_cost * 100, 2)
        AS random_savings_pct
FROM scenario_stats sr
JOIN policy pr ON sr.policy_id = pr.policy_id
JOIN scenario_stats sf ON sf.scenario_id = sr.scenario_id
JOIN policy pf ON sf.policy_id = pf.policy_id
WHERE pr.policy_name = 'RandomPolicy'
  AND pf.policy_name = 'FIFOPolicy'
  AND sf.total_cost > 0
  AND (sf.total_cost - sr.total_cost) / sf.total_cost >= 0.20
ORDER BY random_savings_pct DESC;
