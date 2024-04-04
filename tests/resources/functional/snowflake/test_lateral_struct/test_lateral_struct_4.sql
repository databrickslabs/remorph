
-- snowflake sql:
SELECT
                                   tt.id AS tax_transaction_id,
                                   cast(tt.response_body:"isMpfState" AS BOOLEAN) AS is_mpf_state,
                                   REGEXP_REPLACE(tt.request_body:"deliveryLocation":"city", '""', '') AS delivery_city,
                                   REGEXP_REPLACE(tt.request_body:"store":"storeAddress":"zipCode", '""', '') AS
                                   store_zipcode
                                   FROM tax_table  tt
                              ;

-- databricks sql:
SELECT tt.id AS tax_transaction_id,
                      CAST(tt.response_body.isMpfState AS BOOLEAN) AS is_mpf_state,
                      REGEXP_REPLACE(tt.request_body.deliveryLocation.city, '""', '') AS delivery_city,
                      REGEXP_REPLACE(tt.request_body.store.storeAddress.zipCode, '""', '') AS store_zipcode
               FROM tax_table AS tt;
