with tmp as (select recon_table_id, inserted_ts ,recon_type, explode(data) as data,
row_number() over(partition by recon_table_id,recon_type order by recon_table_id) as rn
from IDENTIFIER(:catalog || '.' || :schema || '.details' )
where recon_type != 'schema')
select main.recon_id,
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
recon_type, key, value, rn
from tmp
inner join
IDENTIFIER(:catalog || '.' || :schema || '.main' ) main
on main.recon_table_id = tmp.recon_table_id
lateral view explode(data) exploded_data AS key, value
