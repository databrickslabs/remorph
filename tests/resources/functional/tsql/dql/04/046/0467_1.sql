--Query type: DQL
DECLARE @regionname nvarchar(25);
DECLARE region_cursor CURSOR FOR
    SELECT r_name
    FROM (
        VALUES ('AFRICA'),
               ('AMERICA'),
               ('ASIA'),
               ('EUROPE'),
               ('MIDDLE EAST')
    ) AS regions (r_name);
OPEN region_cursor;
FETCH NEXT FROM region_cursor INTO @regionname;
