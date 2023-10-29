-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-external-data-source-transact-sql?view=sql-server-ver16

ALTER EXTERNAL DATA SOURCE hadoop_eds SET
     LOCATION = 'hdfs://10.10.10.10:8020',
     RESOURCE_MANAGER_LOCATION = '10.10.10.10:8032'
    ;