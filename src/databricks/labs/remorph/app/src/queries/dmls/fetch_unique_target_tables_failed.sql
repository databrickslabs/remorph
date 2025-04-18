SELECT CONCAT_WS('.', main.target_table.catalog, main.target_table.schema, main.target_table.table_name) AS t_table,
       CAST(main.start_ts AS DATE)                                                                       AS start_date
FROM {REMORPH_METADATA_SCHEMA}.main AS main
INNER JOIN {REMORPH_METADATA_SCHEMA}.metrics AS metrics
ON main.recon_table_id = metrics.recon_table_id
WHERE
    metrics.run_metrics.status = FALSE