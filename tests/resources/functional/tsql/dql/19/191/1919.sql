-- tsql sql:
DECLARE @customer_xml XML;
SET @customer_xml = (
    SELECT CAST('<customer><name>' + c_name + '</name></customer>' AS XML)
    FROM (
        VALUES ('John')
    ) AS customer(c_name)
);
SELECT @customer_xml.exist('/customer/name');
