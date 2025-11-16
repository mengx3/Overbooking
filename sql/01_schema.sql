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

CREATE TABLE flight_stats (
    flight_id      VARCHAR(50) NOT NULL,
    scenario_id    INTEGER NOT NULL,
    policy_id      INTEGER NOT NULL REFERENCES policy(policy_id)
                   ON DELETE CASCADE,
    booked         INTEGER NOT NULL CHECK (booked >= 0),
    showed_up      INTEGER NOT NULL CHECK (showed_up >= 0),
    bumped         INTEGER NOT NULL CHECK (bumped >= 0),
    cost           NUMERIC(10,2) NOT NULL CHECK (cost >= 0),

    PRIMARY KEY (flight_id, scenario_id, policy_id),
    FOREIGN KEY (flight_id, scenario_id)
        REFERENCES flight(flight_id, scenario_id)
        ON DELETE CASCADE
);

CREATE TABLE scenario_stats (
    scenario_id        INTEGER NOT NULL REFERENCES scenario(scenario_id)
                        ON DELETE CASCADE,
    policy_id          INTEGER NOT NULL REFERENCES policy(policy_id)
                        ON DELETE CASCADE,
    total_bumped       INTEGER NOT NULL CHECK (total_bumped >= 0),
    total_cost         NUMERIC(12,2) NOT NULL CHECK (total_cost >= 0),
    bumping_rate       DOUBLE PRECISION NOT NULL CHECK (bumping_rate >= 0),
    flights_affected   INTEGER NOT NULL CHECK (flights_affected >= 0),

    PRIMARY KEY (scenario_id, policy_id)
);


CREATE TABLE risk_event (
    event_id      VARCHAR(100) PRIMARY KEY,
    scenario_id   INTEGER NOT NULL REFERENCES scenario(scenario_id)
                  ON DELETE CASCADE,
    flight_id     VARCHAR(50) NOT NULL,

    label         TEXT,

    FOREIGN KEY (flight_id, scenario_id)
        REFERENCES flight(flight_id, scenario_id)
        ON DELETE CASCADE
);
