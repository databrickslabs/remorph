-- tsql sql:
CREATE SEQUENCE dbo.my_sequence;
GRANT ALTER ON OBJECT::dbo.my_sequence TO admin;
-- REMORPH CLEANUP: DROP SEQUENCE dbo.my_sequence;
