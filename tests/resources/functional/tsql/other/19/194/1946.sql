--Query type: DML
DECLARE @title_view TABLE (title_name VARCHAR(50));
INSERT INTO @title_view (title_name)
VALUES ('NewTitle');
DELETE FROM @title_view;
SELECT * FROM @title_view;
-- REMORPH CLEANUP: DROP TABLE @title_view;
