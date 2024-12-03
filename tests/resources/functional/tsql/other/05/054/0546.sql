--Query type: DML
DECLARE @sql nvarchar(max) = 'ALTER DATABASE MyDatabase SET AUTOMATIC_TUNING ( FORCE_LAST_GOOD_PLAN = ON)';
EXECUTE sp_executesql @sql;
