-- Query the INFER_SCHEMA function.
SELECT *
  FROM TABLE(
    INFER_SCHEMA(
      LOCATION=>'@mystage/geography/cities.parquet'
      , FILE_FORMAT=>'my_parquet_format'
      )
    );
