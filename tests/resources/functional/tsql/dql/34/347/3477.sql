--Query type: DQL
SELECT xml_schema_namespace(namespace_name, schema_name) FROM (VALUES ('production', 'AdventureWorks.ProductDescriptionSchemaCollection')) AS temp_result(namespace_name, schema_name);
