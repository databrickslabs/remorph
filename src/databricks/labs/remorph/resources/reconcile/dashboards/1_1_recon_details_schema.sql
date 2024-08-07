/* --filter recon_id target_table_name source_table_name */
WITH tmp AS (
  SELECT
    recon_table_id,
    inserted_ts,
    EXPLODE(data) AS schema_data
  FROM
    remorph_catalog.remorph_schema.details
  WHERE
    recon_type = 'SCHEMA'
)
SELECT
  main.recon_id,
  main.source_table.`CATALOG` AS source_catalog,
  main.source_table.`SCHEMA` AS source_schema,
  main.source_table.table_name AS source_table_name,
  CASE
    WHEN COALESCE(main.source_table.catalog, '') <> '' THEN CONCAT(
      main.source_table.catalog,
      '.',
      main.source_table.schema,
      '.',
      main.source_table.table_name
    )
    ELSE CONCAT(
      main.source_table.schema,
      '.',
      main.source_table.table_name
    )
  END AS source_table,
  main.target_table.`CATALOG` AS target_catalog,
  main.target_table.`SCHEMA` AS target_schema,
  main.target_table.table_name AS target_table_name,
  CONCAT(
    main.target_table.catalog,
    '.',
    main.target_table.schema,
    '.',
    main.target_table.table_name
  ) AS target_table,
  schema_data ['SOURCE_COLUMN'] AS source_column,
  schema_data ['SOURCE_DATATYPE'] AS source_datatype,
  schema_data ['DATABRICKS_COLUMN'] AS databricks_column,
  schema_data ['DATABRICKS_DATATYPE'] AS databricks_datatype,
  schema_data ['IS_VALID'] AS is_valid
FROM
  remorph_catalog.remorph_schema.main AS main
  INNER JOIN tmp ON main.recon_table_id = tmp.recon_table_id
ORDER BY
  tmp.inserted_ts DESC,
  main.recon_id,
  main.target_table