--Query type: DCL
CREATE CERTIFICATE NewCertificate
WITH SUBJECT = 'NewCertificate',
    EXPIRY_DATE = '2025-01-01';

CREATE TABLE #Temp
(
    CertificateName sysname,
    CertificateSubject nvarchar(100)
);

INSERT INTO #Temp
VALUES ('NewCertificate', 'NewCertificate');

SELECT *
FROM #Temp;

-- REMORPH CLEANUP: DROP TABLE #Temp;
-- REMORPH CLEANUP: DROP CERTIFICATE NewCertificate;