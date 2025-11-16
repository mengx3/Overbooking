DROP TABLE IF EXISTS event_gap_overlap CASCADE;
DROP TABLE IF EXISTS event_policy CASCADE;
DROP TABLE IF EXISTS flight_stats CASCADE;
DROP TABLE IF EXISTS flight CASCADE;
DROP TABLE IF EXISTS scenario_stats CASCADE;
DROP TABLE IF EXISTS scenario CASCADE;
DROP TABLE IF EXISTS policy CASCADE;


CREATE TABLE policy (
    policy_id      SERIAL PRIMARY KEY,
    policy_name    VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE scenario (
    scenario_id    INTEGER PRIMARY KEY,
    description    TEXT
);

CREATE TABLE flight (
    flight_id      VARCHAR(50) NOT NULL,
    scenario_id    INTEGER NOT NULL REFERENCES scenario(scenario_id)
                   ON DELETE CASCADE,
    capacity       INTEGER NOT NULL CHECK (capacity > 0),
    PRIMARY KEY (flight_id, scenario_id)
);
