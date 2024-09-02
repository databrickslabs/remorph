--Query type: DML
INSERT INTO #tool (ID, Name)
SELECT ID, Name
FROM (
    VALUES (1, 'Hammer'),
           (2, 'Screwdriver'),
           (3, 'Pliers')
) AS tool (ID, Name);