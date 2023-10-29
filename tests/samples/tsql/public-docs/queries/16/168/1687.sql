-- see https://learn.microsoft.com/en-us/sql/t-sql/spatial-geography/mindbcompatibilitylevel-geography-data-type?view=sql-server-ver16

DECLARE @g geometry = 'CIRCULARSTRING(-120.533 46.566, -118.283 46.1, -122.3 47.45)';  
IF @g.MinDbCompatibilityLevel() <= 110  
BEGIN  
    SELECT @g.ToString();  
END