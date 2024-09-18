package com.databricks.labs.remorph.discovery

object Constants {
  val tableDefinitionQuery: String = s"""SELECT
                                |    sft.TABLE_CATALOG,
                                |    sft.TABLE_SCHEMA,
                                |    sft.TABLE_NAME,
                                |    t.Schema as derivedSchema,
                                |    sft.BYTES,
                                |    sft.TABLE_TYPE
                                |FROM (
                                |    SELECT
                                |        TABLE_CATALOG,
                                |        TABLE_SCHEMA,
                                |        TABLE_NAME,
                                |        LISTAGG(column_name || ':' ||
                                |            CASE
                                |                WHEN numeric_precision IS NOT NULL AND numeric_scale IS NOT NULL
                                |                THEN
                                |                    CONCAT(data_type, '(', numeric_precision, ',' , numeric_scale, ')')
                                |                WHEN LOWER(data_type) = 'text'
                                |                THEN
                                |                    CONCAT('varchar', '(', CHARACTER_MAXIMUM_LENGTH, ')')
                                |                ELSE data_type
                                |             END|| ':' || TO_BOOLEAN(CASE WHEN IS_NULLABLE = 'YES' THEN 'true' ELSE 'false' END),
                                |        '~') WITHIN GROUP (ORDER BY ordinal_position) AS Schema
                                |    FROM
                                |        SNOWFLAKE.INFORMATION_SCHEMA.COLUMNS
                                |    GROUP BY
                                |        TABLE_CATALOG, TABLE_SCHEMA, TABLE_NAME
                                |) t
                                |JOIN SNOWFLAKE.INFORMATION_SCHEMA.TABLES sft
                                |    ON t.TABLE_CATALOG = sft.TABLE_CATALOG
                                |    AND t.TABLE_SCHEMA = sft.TABLE_SCHEMA
                                |    AND t.TABLE_NAME = sft.TABLE_NAME
                                |ORDER BY
                                |    sft.TABLE_CATALOG, sft.TABLE_SCHEMA, sft.TABLE_NAME;""".stripMargin

}
