-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/openjson-transact-sql?view=sql-server-ver16

DECLARE @array VARCHAR(MAX);
SET @array = '[{"month":"Jan", "temp":10},{"month":"Feb", "temp":12},{"month":"Mar", "temp":15},
               {"month":"Apr", "temp":17},{"month":"May", "temp":23},{"month":"Jun", "temp":27}
              ]';

SELECT * FROM OPENJSON(@array)
        WITH (  month VARCHAR(3),
                temp int,
                month_id tinyint '$.sql:identity()') as months