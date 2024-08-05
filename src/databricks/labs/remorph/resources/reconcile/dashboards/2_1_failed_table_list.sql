select
main.recon_id,
main.source_type,
main.report_type,
main.source_table.`catalog` as source_catalog,
main.source_table.`schema` as source_schema,
main.source_table.table_name as source_table_name,
CASE
        WHEN COALESCE(MAIN.SOURCE_TABLE.CATALOG, '') <> '' THEN CONCAT(MAIN.SOURCE_TABLE.CATALOG, '.', MAIN.SOURCE_TABLE.SCHEMA, '.', MAIN.SOURCE_TABLE.TABLE_NAME)
        ELSE CONCAT(MAIN.SOURCE_TABLE.SCHEMA, '.', MAIN.SOURCE_TABLE.TABLE_NAME)
    END AS source_table,
main.target_table.`catalog` as target_catalog,
main.target_table.`schema` as target_schema,
main.target_table.table_name as target_table_name,
CONCAT(MAIN.TARGET_TABLE.CATALOG, '.', MAIN.TARGET_TABLE.SCHEMA, '.', MAIN.TARGET_TABLE.TABLE_NAME) AS target_table,
metrics.run_metrics.status as status,
metrics.run_metrics.run_by_user as executed_by,
main.start_ts as start_ts,
main.end_ts as end_ts,
date(main.start_ts) as start_date
from IDENTIFIER(:catalog || '.' || :schema || '.main' ) main
inner join
IDENTIFIER(:catalog || '.' || :schema || '.metrics' ) metrics
on main.recon_table_id = metrics.recon_table_id
where metrics.run_metrics.status = false
order by metrics.inserted_ts desc, main.recon_id, main.target_table.table_name