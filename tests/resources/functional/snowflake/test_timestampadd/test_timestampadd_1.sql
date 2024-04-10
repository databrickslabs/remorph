
-- snowflake sql:
SELECT timestampadd('hour', -1, bp.ts) AND timestampadd('day', 2, bp.ts)
                FROM base_prep AS bp;

-- databricks sql:
SELECT DATEADD(hour, -1, bp.ts) AND DATEADD(day, 2, bp.ts) FROM base_prep AS bp;
