/* --height 6 --width 6 */
WITH tmp AS (
    SELECT
        recon_table_id,
        inserted_ts,
        recon_type,
        explode(data) AS data,
        row_number() OVER (PARTITION BY recon_table_id, recon_type ORDER BY recon_table_id) AS rn
    FROM
        remorph.reconcile.details
    WHERE
        recon_type != 'schema'
)
SELECT
    main.recon_id,
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
    recon_type,
    key,
    value,
    rn
FROM tmp
         INNER JOIN remorph.reconcile.main main
                    ON main.recon_table_id = tmp.recon_table_id
    LATERAL VIEW explode(data) exploded_data AS key, value
