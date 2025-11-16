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
