-- snowflake sql:
SELECT
  tt.value:id AS tax_transaction_id,
  CAST(tt.value:responseBody:isMpfState AS BOOLEAN) AS is_mpf_state,
  REGEXP_REPLACE(tt.value:requestBody:deliveryLocation:city, '""', '') AS delivery_city,
  REGEXP_REPLACE(tt.value:requestBody:store:storeAddress:zipCode, '""', '') AS store_zipcode
FROM (
  SELECT
    OBJECT_CONSTRUCT(
      'id', 1,
      'responseBody', OBJECT_CONSTRUCT('isMpfState', TRUE),
      'requestBody', OBJECT_CONSTRUCT(
        'deliveryLocation', OBJECT_CONSTRUCT('city', 'New""York'),
        'store', OBJECT_CONSTRUCT('storeAddress', OBJECT_CONSTRUCT('zipCode', '100""01'))
      )
    ) AS value
) AS tt;


-- databricks sql:
SELECT
  tt.col1 AS tax_transaction_id,
  CAST(tt.col2.responseBody.isMpfState AS BOOLEAN) AS is_mpf_state,
  REGEXP_REPLACE(tt.col2.requestBody.deliveryLocation.city, '""', '') AS delivery_city,
  REGEXP_REPLACE(tt.col2.requestBody.store.storeAddress.zipCode, '""', '') AS store_zipcode
FROM VALUES(
  STRUCT(
    1 AS id,
    STRUCT(
      STRUCT(TRUE AS isMpfState) AS responseBody,
      STRUCT(
        STRUCT('New""York' AS city) AS deliveryLocation,
        STRUCT(
          STRUCT('100""01' AS zipCode) AS storeAddress
        ) AS store
      ) AS requestBody
    )
  )
) AS tt(col1,col2);