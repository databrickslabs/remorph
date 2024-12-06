-- tsql sql:
WITH customer_info AS (
    SELECT
        c_custkey,
        c_name,
        c_address,
        CAST(DECOMPRESS(c_comment) AS NVARCHAR(MAX)) AS c_comment
    FROM
    (
        VALUES
            (1, 'Customer1', 'Address1', COMPRESS('Comment1')),
            (2, 'Customer2', 'Address2', COMPRESS('Comment2')),
            (3, 'Customer3', 'Address3', COMPRESS('Comment3'))
    ) AS customer (c_custkey, c_name, c_address, c_comment)
)
SELECT
    c_custkey,
    c_name,
    c_address,
    c_comment
FROM
    customer_info;
