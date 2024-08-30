-- snowflake sql:
SELECT
  tt.col:id AS tax_transaction_id,
  CAST(tt.col:responseBody:isMpfState AS BOOLEAN) AS is_mpf_state,
  REGEXP_REPLACE(tt.col:requestBody:deliveryLocation:city, '""', '') AS delivery_city,
  REGEXP_REPLACE(tt.col:requestBody:store:storeAddress:zipCode, '""', '') AS store_zipcode
FROM (
  SELECT
    OBJECT_CONSTRUCT(
      'id', 1,
      'responseBody', OBJECT_CONSTRUCT('isMpfState', TRUE),
      'requestBody', OBJECT_CONSTRUCT(
        'deliveryLocation', OBJECT_CONSTRUCT('city', 'New""York'),
        'store', OBJECT_CONSTRUCT('storeAddress', OBJECT_CONSTRUCT('zipCode', '100""01'))
      )
    ) AS col
) AS tt;


-- databricks sql:
SELECT
  tt.col.id AS tax_transaction_id,
  CAST(tt.col.responseBody.isMpfState AS BOOLEAN) AS is_mpf_state,
  REGEXP_REPLACE(tt.col.requestBody.deliveryLocation.city, '""', '') AS delivery_city,
  REGEXP_REPLACE(tt.col.requestBody.store.storeAddress.zipCode, '""', '') AS store_zipcode
FROM (
  SELECT
  STRUCT(
    1 AS id,
      STRUCT(TRUE AS isMpfState) AS responseBody,
      STRUCT(
        STRUCT('New""York' AS city) AS deliveryLocation,
        STRUCT(
          STRUCT('100""01' AS zipCode) AS storeAddress
        ) AS store
      ) AS requestBody

  ) AS col
) AS tt;