-- see https://docs.snowflake.com/en/sql-reference/info-schema/class_instance_functions

SELECT function_name,
       function_instance_name AS instance_name,
       argument_signature,
       data_type AS return_value_data_type
    FROM mydatabase.INFORMATION_SCHEMA.CLASS_INSTANCE_FUNCTIONS;