/* --filter start_date */
SELECT
  main.recon_id,
  main.source_type,
  main.report_type,
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
  CONCAT(
    main.target_table.catalog,
    '.',
    main.target_table.schema,
    '.',
    main.target_table.table_name
  ) AS target_table,
  metrics.run_metrics.status AS status,
  metrics.run_metrics.run_by_user AS executed_by,
  main.start_ts AS start_ts,
  main.end_ts AS end_ts,
  CAST(main.start_ts AS DATE) AS start_date
FROM
  remorph_catalog.remorph_schema.main AS main
  INNER JOIN remorph_catalog.remorph_schema.metrics AS metrics ON main.recon_table_id = metrics.recon_table_id
WHERE
  metrics.run_metrics.status = TRUE
ORDER BY
  metrics.inserted_ts DESC,
  main.recon_id,
  main.target_table.table_name