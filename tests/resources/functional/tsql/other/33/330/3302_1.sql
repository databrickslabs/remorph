-- tsql sql:
IF EXISTS (SELECT 1 FROM (VALUES ('reminder')) AS trigger_names(name) WHERE name = 'reminder')
    DROP TRIGGER reminder;
