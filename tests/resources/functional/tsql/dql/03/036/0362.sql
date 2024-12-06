-- tsql sql:
SELECT SOUNDEX(name) AS PhoneticSound, name FROM (VALUES ('Johnson'), ('Jonsen'), ('Jenson')) AS Names(name);
