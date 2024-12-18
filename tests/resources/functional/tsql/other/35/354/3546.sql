-- tsql sql:
CREATE TABLE Certificates
(
    CertificateName nvarchar(50),
    CertificateValue nvarchar(50)
);

INSERT INTO Certificates
(
    CertificateName,
    CertificateValue
)
VALUES
(
    'Customer01',
    'Certificate01'
);

WITH CertificateCTE AS
(
    SELECT CertificateName, CertificateValue
    FROM Certificates
)
SELECT *
FROM CertificateCTE;

SELECT *
FROM
(
    VALUES
    (
        'Customer01',
        'Certificate01'
    )
) AS Certificates
(
    CertificateName,
    CertificateValue
);

DELETE FROM Certificates
WHERE CertificateName = 'Customer01';

SELECT *
FROM Certificates;

-- REMORPH CLEANUP: DROP TABLE Certificates;
