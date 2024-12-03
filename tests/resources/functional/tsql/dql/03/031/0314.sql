--Query type: DQL
SELECT VAR(DISTINCT TotalPrice) AS Distinct_Values, VAR(TotalPrice) AS All_Values FROM (VALUES (100.0), (200.0), (300.0), (400.0), (500.0)) AS TempResult(TotalPrice);
