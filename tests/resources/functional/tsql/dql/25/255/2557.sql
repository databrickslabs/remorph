-- tsql sql:
SELECT DATABASE_ID FROM (VALUES (DB_ID())) AS temp_table(DATABASE_ID);
