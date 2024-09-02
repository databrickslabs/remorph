--Query type: DML
INSERT INTO inventory33 (description)
SELECT description
FROM (
    VALUES ('Red pen'), ('Blue pen'), ('Green pen'), ('Black pen'), ('Yellow pen')
) AS temp (description);