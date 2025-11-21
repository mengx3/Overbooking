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

-- Q4
SELECT
    fs.flight_id,
    COUNT(DISTINCT fs.scenario_id) AS num_scenarios_overbooked
FROM flight_stats fs
WHERE fs.bumped > 0
GROUP BY fs.flight_id
HAVING COUNT(DISTINCT fs.scenario_id) >= 3
ORDER BY num_scenarios_overbooked DESC, fs.flight_id;

-- Q5
SELECT
    p.policy_name,
    s.scenario_id,
    s.total_cost,
    RANK() OVER (PARTITION BY p.policy_name
                 ORDER BY s.total_cost DESC) AS cost_rank
FROM scenario_stats s
JOIN policy p ON s.policy_id = p.policy_id
QUALIFY cost_rank <= 5;

-- Q6
SELECT
    f.flight_id,
    f.scenario_id,
    fs_fifo.bumped  AS fifo_bumped,
    fs_rand.bumped  AS random_bumped
FROM flight f
JOIN flight_stats fs_fifo
  ON f.flight_id = fs_fifo.flight_id
 AND f.scenario_id = fs_fifo.scenario_id
JOIN policy p_fifo
  ON fs_fifo.policy_id = p_fifo.policy_id
JOIN flight_stats fs_rand
  ON f.flight_id = fs_rand.flight_id
 AND f.scenario_id = fs_rand.scenario_id
JOIN policy p_rand
  ON fs_rand.policy_id = p_rand.policy_id
WHERE p_fifo.policy_name = 'FIFOPolicy'
  AND p_rand.policy_name = 'RandomPolicy'
  AND fs_fifo.bumped > fs_rand.bumped
ORDER BY f.scenario_id, f.flight_id;

-- Q7
SELECT
    e.event_id,
    e.scenario_id,
    e.flight_id,
    g.shortfall_sum,
    g.policies,
    g.covered_count
FROM event_gap_overlap g
JOIN risk_event e ON g.event_id = e.event_id
WHERE g.is_gap = TRUE
ORDER BY e.scenario_id, e.flight_id, e.event_id;
