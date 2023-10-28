SELECT procedure_name,
       procedure_instance_name,
       argument_signature,
       data_type AS return_value_data_type
    FROM mydatabase.INFORMATION_SCHEMA.CLASS_INSTANCE_PROCEDURES;