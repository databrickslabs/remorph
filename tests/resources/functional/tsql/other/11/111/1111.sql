--Query type: DDL
DECLARE @PoolName nvarchar(128) = 'PoolMarketing';
DECLARE @MinCPUPercent int = 20;
DECLARE @MaxCPUPercent int = 30;
DECLARE @CapCPUPercent int = 40;
DECLARE @MinMemoryPercent int = 10;
DECLARE @MaxMemoryPercent int = 20;

SELECT @PoolName AS PoolName, @MinCPUPercent AS MinCPUPercent, @MaxCPUPercent AS MaxCPUPercent, @CapCPUPercent AS CapCPUPercent, @MinMemoryPercent AS MinMemoryPercent, @MaxMemoryPercent AS MaxMemoryPercent;