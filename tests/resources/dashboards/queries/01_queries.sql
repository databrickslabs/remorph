SELECT
main.recon_id,
main.source_type,
main.report_type,
main.source_table.`catalog` as source_catalog,
main.source_table.`schema` as source_schema,
main.source_table.table_name as source_table_name
FROM remorph.reconcile.main main
