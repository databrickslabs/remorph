-- tsql sql:
CREATE TABLE CustomerDemographics (CD_DEMO_SK INTEGER NOT NULL, CD_GENDER VARCHAR(1) NULL);
INSERT INTO CustomerDemographics (CD_DEMO_SK, CD_GENDER) VALUES (1, 'M'), (2, 'F'), (3, 'M');
SELECT * FROM CustomerDemographics;
-- REMORPH CLEANUP: DROP TABLE CustomerDemographics;
