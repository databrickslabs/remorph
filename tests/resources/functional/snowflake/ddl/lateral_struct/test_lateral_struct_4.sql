-- snowflake sql:
SELECT
  tt.col:id AS tax_transaction_id,
  CAST(tt.col:responseBody.isMpfState AS BOOLEAN) AS is_mpf_state,
  REGEXP_REPLACE(tt.col:requestBody.deliveryLocation.city, '-', '') AS delivery_city,
  REGEXP_REPLACE(tt.col:requestBody.store.storeAddress.zipCode, '=', '') AS store_zipcode
FROM (
  SELECT
    PARSE_JSON('{"id": 1, "responseBody": { "isMpfState": true }, "requestBody": { "deliveryLocation": { "city": "New-York" }, "store": {"storeAddress": {"zipCode": "100=01"}}}}')
    AS col
) AS tt;

-- databricks sql:
SELECT
  tt.col:id AS tax_transaction_id,
  CAST(tt.col:responseBody.isMpfState AS BOOLEAN) AS is_mpf_state,
  REGEXP_REPLACE(tt.col:requestBody.deliveryLocation.city, '-', '') AS delivery_city,
  REGEXP_REPLACE(tt.col:requestBody.store.storeAddress.zipCode, '=', '') AS store_zipcode
FROM (
  SELECT
    PARSE_JSON('{"id": 1, "responseBody": { "isMpfState": true }, "requestBody": { "deliveryLocation": { "city": "New-York" }, "store": {"storeAddress": {"zipCode": "100=01"}}}}')
    AS col
) AS tt;
