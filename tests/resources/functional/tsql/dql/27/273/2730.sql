-- tsql sql:
SELECT REVERSE('abcdef') AS ReversedString FROM (VALUES ('abcdef')) AS TPC_H_Values (StringField);
