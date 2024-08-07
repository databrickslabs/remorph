/* --filter start_date */
WITH tmp AS (
  SELECT
    recon_table_id,
    inserted_ts,
    recon_type,
    EXPLODE(data) AS data,
    ROW_NUMBER() OVER (
      PARTITION BY recon_table_id,
      recon_type
      ORDER BY
        recon_table_id
    ) AS rn
  FROM
    remorph_catalog.remorph_schema.details
  WHERE
    recon_type <> 'SCHEMA'
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
  recon_type,
  key,
  value,
  rn
FROM
  tmp
  INNER JOIN remorph_catalog.remorph_schema.main AS main ON main.recon_table_id = tmp.recon_table_id LATERAL VIEW EXPLODE(data) EXPLODED_DATA AS key,
  value