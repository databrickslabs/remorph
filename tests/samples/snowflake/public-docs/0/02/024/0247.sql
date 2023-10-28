-- Create a file format that sets the file type as Parquet.
CREATE FILE FORMAT my_parquet_format
  TYPE = parquet;

-- Query the GENERATE_COLUMN_DESCRIPTION function.
SELECT GENERATE_COLUMN_DESCRIPTION(ARRAY_AGG(OBJECT_CONSTRUCT(*)), 'table') AS COLUMNS
  FROM TABLE (
    INFER_SCHEMA(
      LOCATION=>'@mystage',
      FILE_FORMAT=>'my_parquet_format'
    )
  );


-- The function output can be used to define the columns in a table.
CREATE TABLE mytable ("country" VARIANT, "continent" TEXT);