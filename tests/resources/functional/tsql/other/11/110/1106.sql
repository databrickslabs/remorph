-- tsql sql:
CREATE TABLE ExpenseQueue
(
    QueueName VARCHAR(100),
    Status VARCHAR(10)
);

INSERT INTO ExpenseQueue (QueueName, Status)
VALUES ('ExpenseQueue', 'OFF');

SELECT *
FROM ExpenseQueue;

-- REMORPH CLEANUP: DROP TABLE ExpenseQueue;
