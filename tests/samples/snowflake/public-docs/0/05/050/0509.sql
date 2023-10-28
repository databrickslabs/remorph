SELECT 'a' IN (
    SELECT column1 FROM VALUES ('b'), ('c'), ('d')
    ) AS RESULT;