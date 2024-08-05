with tmp as (select
recon_table_id,
inserted_ts,
explode(data) as schema_data
from IDENTIFIER(:catalog || '.' || :schema || '.details' )
where recon_type='schema'
)
select
main.recon_id,
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
schema_data['source_column'] as source_column,
schema_data['source_datatype'] as source_datatype,
schema_data['databricks_column'] as databricks_column,
schema_data['databricks_datatype'] as databricks_datatype,
schema_data['is_valid'] as is_valid
from
IDENTIFIER(:catalog || '.' || :schema || '.main' ) main
inner join
tmp
on main.recon_table_id = tmp.recon_table_id
order by tmp.inserted_ts desc, main.recon_id, main.target_table
