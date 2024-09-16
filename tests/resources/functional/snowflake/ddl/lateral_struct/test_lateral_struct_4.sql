-- snowflake sql:
SELECT
  tt.col:id AS tax_transaction_id,
  CAST(tt.col:responseBody.isMpfState AS BOOLEAN) AS is_mpf_state,
  REGEXP_REPLACE(tt.col:requestBody.deliveryLocation.city, '-', '') AS delivery_city,
  REGEXP_REPLACE(tt.col:requestBody.store.storeAddress.zipCode, '=', '') AS store_zipcode
FROM (
  SELECT
    PARSE_JSON('{
      "id": 1,
      "responseBody": {
        "isMpfState": true
      },
      "requestBody": {
        "deliveryLocation": {
          "city": "New-York"
        },
        "store": {
          "storeAddress": {
            "zipCode": "100=01"
          }
        }
      }
    }') AS col
) AS tt;

-- databricks sql:
SELECT
  tt.col:id AS tax_transaction_id,
  CAST(tt.col:responseBody.isMpfState AS BOOLEAN) AS is_mpf_state,
  REGEXP_REPLACE(tt.col:requestBody.deliveryLocation.city, '-', '') AS delivery_city,
  REGEXP_REPLACE(tt.col:requestBody.store.storeAddress.zipCode, '=', '') AS store_zipcode
FROM (
  SELECT
    PARSE_JSON(
      '{\n      "id": 1,\n      "responseBody": {\n        "isMpfState": true\n      },\n      "requestBody": {\n        "deliveryLocation": {\n          "city": "New-York"\n        },\n        "store": {\n          "storeAddress": {\n            "zipCode": "100=01"\n          }\n        }\n      }\n    }'
    ) AS col
) AS tt