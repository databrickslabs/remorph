/* --title 'Number of Distinct Recon IDs per Target Table Failed' --width 6 */
SELECT
    main.recon_id,
    main.source_type,
    main.report_type,
    main.source_table.`catalog` AS source_catalog,
    main.source_table.`schema` AS source_schema,
    main.source_table.table_name AS source_table_name,
    CASE
        WHEN COALESCE(main.source_table.catalog, '') <> '' THEN CONCAT(main.source_table.catalog, '.', main.source_table.schema, '.', main.source_table.table_name)
        ELSE CONCAT(main.source_table.schema, '.', main.source_table.table_name)
        END AS source_table,
    main.target_table.`catalog` AS target_catalog,
    main.target_table.`schema` AS target_schema,
    main.target_table.table_name AS target_table_name,
    CONCAT(main.target_table.catalog, '.', main.target_table.schema, '.', main.target_table.table_name) AS target_table,
    metrics.run_metrics.status AS status,
    metrics.run_metrics.run_by_user AS executed_by,
    main.start_ts AS start_ts,
    main.end_ts AS end_ts,
    DATE(main.start_ts) AS start_date
FROM
    remorph.reconcile.main main
    INNER JOIN remorph.reconcile.metrics metrics
ON main.recon_table_id = metrics.recon_table_id
WHERE
    metrics.run_metrics.status = FALSE
ORDER BY
    metrics.inserted_ts DESC,
    main.recon_id,
    main.target_table.table_name
