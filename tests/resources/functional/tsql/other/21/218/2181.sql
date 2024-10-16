--Query type: DML
SELECT Time, dbo.TimeDelay_hh_mm_ss(Time) AS Delay FROM (VALUES ('00:00:10'), ('00:00:20'), ('00:00:30')) AS TimeDelays(Time);