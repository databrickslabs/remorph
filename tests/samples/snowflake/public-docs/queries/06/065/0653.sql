-- see https://docs.snowflake.com/en/sql-reference/functions/median

INSERT INTO aggr VALUES(1, 10), (1,20), (1, 21);
INSERT INTO aggr VALUES(2, 10), (2, 20), (2, 25), (2, 30);
INSERT INTO aggr VALUES(3, NULL);