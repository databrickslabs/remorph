-- tsql sql:
CREATE TABLE #my_new_events
(
    id INT,
    event_name VARCHAR(50)
);

INSERT INTO #my_new_events (id, event_name)
VALUES
    (1, 'event1'),
    (2, 'event2');

SELECT *
FROM #my_new_events;

-- REMORPH CLEANUP: DROP TABLE #my_new_events;
