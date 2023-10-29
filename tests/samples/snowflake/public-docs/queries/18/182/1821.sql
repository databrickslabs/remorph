-- see https://docs.snowflake.com/en/sql-reference/functions/parse_json

SELECT varchar1, PARSE_JSON(varchar1), variant1,  TO_JSON(variant1),
                 PARSE_JSON(varchar1) = variant1, TO_JSON(variant1) = varchar1
    FROM jdemo2;