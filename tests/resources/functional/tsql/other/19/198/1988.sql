--Query type: DDL
CREATE TABLE #customer
(
    c_custkey INT,
    c_name VARCHAR(100),
    c_address VARCHAR(200)
);

INSERT INTO #customer (c_custkey, c_name, c_address)
VALUES
    (1, 'Customer 1', 'Address 1'),
    (2, 'Customer 2', 'Address 2'),
    (3, 'Customer 3', 'Address 3');

WITH customer_data AS
(
    SELECT c_custkey, c_name, c_address
    FROM #customer
)
SELECT *
FROM customer_data;

CREATE FULLTEXT STOPLIST myStoplist;

ALTER FULLTEXT STOPLIST myStoplist
ADD 'the' LANGUAGE 'English';

ALTER FULLTEXT STOPLIST myStoplist
ADD 'and' LANGUAGE 'English';

SELECT *
FROM sys.fulltext_stopwords
WHERE stoplist_id = (
    SELECT stoplist_id
    FROM sys.fulltext_stoplists
    WHERE name = 'myStoplist'
);

DROP FULLTEXT STOPLIST myStoplist;

DROP TABLE #customer;