-- tsql sql:
SELECT *
INTO customer_address
FROM (
    SELECT *
    FROM (
        VALUES (
            1,
            'address1',
            'street1',
            'number1',
            'suffix1',
            'type1',
            'suite1',
            'city1',
            'county1',
            'state1',
            'zip1',
            'country1',
            1.00,
            'type1'
        )
    ) AS x (
        ca_address_sk,
        ca_address_id,
        ca_street_name,
        ca_street_number,
        ca_street_number_suffix,
        ca_street_type,
        ca_suite_number,
        ca_city,
        ca_county,
        ca_state,
        ca_zip,
        ca_country,
        ca_gmt_offset,
        ca_location_type
    )
) AS temp_result;
-- REMORPH CLEANUP: DROP TABLE customer_address;
SELECT *
FROM customer_address;
