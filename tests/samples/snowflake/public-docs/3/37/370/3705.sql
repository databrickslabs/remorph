SELECT TABLE_SCHEMA,SUM(BYTES)
    FROM mydatabase.information_schema.tables
    GROUP BY TABLE_SCHEMA;