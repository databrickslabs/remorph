-- see https://docs.snowflake.com/en/sql-reference/functions/conditional_true_event

CREATE TABLE borrowers (
    name VARCHAR,
    status_date DATE,
    late_balance NUMERIC(11, 2),
    thirty_day_late_balance NUMERIC(11, 2)
    );
INSERT INTO borrowers (name, status_date, late_balance, thirty_day_late_balance) VALUES

    -- Pays late frequently, but catches back up rather than falling further
    -- behind.
    ('Geoffrey Flake', '2018-01-01'::DATE,    0.0,    0.0),
    ('Geoffrey Flake', '2018-02-01'::DATE, 1000.0,    0.0),
    ('Geoffrey Flake', '2018-03-01'::DATE, 2000.0, 1000.0),
    ('Geoffrey Flake', '2018-04-01'::DATE,    0.0,    0.0),
    ('Geoffrey Flake', '2018-05-01'::DATE, 1000.0,    0.0),
    ('Geoffrey Flake', '2018-06-01'::DATE, 2000.0, 1000.0),
    ('Geoffrey Flake', '2018-07-01'::DATE,    0.0,    0.0),
    ('Geoffrey Flake', '2018-08-01'::DATE,    0.0,    0.0),

    -- Keeps falling further behind.
    ('Cy Dismal', '2018-01-01'::DATE,    0.0,    0.0),
    ('Cy Dismal', '2018-02-01'::DATE,    0.0,    0.0),
    ('Cy Dismal', '2018-03-01'::DATE, 1000.0,    0.0),
    ('Cy Dismal', '2018-04-01'::DATE, 2000.0, 1000.0),
    ('Cy Dismal', '2018-05-01'::DATE, 3000.0, 2000.0),
    ('Cy Dismal', '2018-06-01'::DATE, 4000.0, 3000.0),
    ('Cy Dismal', '2018-07-01'::DATE, 5000.0, 4000.0),
    ('Cy Dismal', '2018-08-01'::DATE, 6000.0, 5000.0),

    -- Fell behind and isn't catching up, but isn't falling further and 
    -- further behind. Essentially, this person just 'failed' once.
    ('Leslie Safer', '2018-01-01'::DATE,    0.0,    0.0),
    ('Leslie Safer', '2018-02-01'::DATE,    0.0,    0.0),
    ('Leslie Safer', '2018-03-01'::DATE, 1000.0, 1000.0),
    ('Leslie Safer', '2018-04-01'::DATE, 2000.0, 1000.0),
    ('Leslie Safer', '2018-05-01'::DATE, 2000.0, 1000.0),
    ('Leslie Safer', '2018-06-01'::DATE, 2000.0, 1000.0),
    ('Leslie Safer', '2018-07-01'::DATE, 2000.0, 1000.0),
    ('Leslie Safer', '2018-08-01'::DATE, 2000.0, 1000.0),

    -- Always pays on time and in full.
    ('Ida Idyll', '2018-01-01'::DATE,    0.0,    0.0),
    ('Ida Idyll', '2018-02-01'::DATE,    0.0,    0.0),
    ('Ida Idyll', '2018-03-01'::DATE,    0.0,    0.0),
    ('Ida Idyll', '2018-04-01'::DATE,    0.0,    0.0),
    ('Ida Idyll', '2018-05-01'::DATE,    0.0,    0.0),
    ('Ida Idyll', '2018-06-01'::DATE,    0.0,    0.0),
    ('Ida Idyll', '2018-07-01'::DATE,    0.0,    0.0),
    ('Ida Idyll', '2018-08-01'::DATE,    0.0,    0.0)

    ;