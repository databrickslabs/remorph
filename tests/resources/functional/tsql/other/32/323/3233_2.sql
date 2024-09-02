--Query type: DML
INSERT INTO dbo.Equipment (Name)
SELECT Name
FROM (
    VALUES ('Drill'), ('Wrench'), ('Pliers'), ('Tape Measure')
) AS Equipment (Name);