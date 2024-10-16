--Query type: DDL
CREATE EXTERNAL DATA SOURCE external_data_source_name_node
WITH (
    LOCATION = 'hdfs://10.10.10.10:8020'
);

CREATE EXTERNAL DATA SOURCE external_data_source_resource_manager
WITH (
    LOCATION = 'hdfs://10.10.10.10:8032'
);

SELECT *
FROM sys.external_data_sources;

-- REMORPH CLEANUP: DROP EXTERNAL DATA SOURCE external_data_source_name_node;
-- REMORPH CLEANUP: DROP EXTERNAL DATA SOURCE external_data_source_resource_manager;