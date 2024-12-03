--Query type: DDL
CREATE SEQUENCE Test.NewSequence;
SELECT NEXT VALUE FOR Test.NewSequence AS FirstValue;
-- REMORPH CLEANUP: DROP SEQUENCE Test.NewSequence;
