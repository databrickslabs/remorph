--Query type: DDL
WITH customerDemographics AS (
    SELECT *
    FROM (
        VALUES
            (1, 'address1', 'phone1'),
            (2, 'address2', 'phone2')
    ) AS temp (custKey, address, phone)
)
SELECT *
FROM customerDemographics;
