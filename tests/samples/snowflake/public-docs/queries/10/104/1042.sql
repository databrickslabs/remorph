-- see https://docs.snowflake.com/en/sql-reference/functions/case

SELECT CASE COLLATE('m', 'upper')
    WHEN 'M' THEN TRUE
    ELSE FALSE
END;
SELECT CASE 'm'
    WHEN COLLATE('M', 'lower') THEN TRUE
    ELSE FALSE
END;