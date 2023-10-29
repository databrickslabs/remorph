-- see https://docs.snowflake.com/en/sql-reference/functions/array_size

CREATE OR replace TABLE colors (v variant);

INSERT INTO
   colors
   SELECT
      parse_json(column1) AS v
   FROM
   VALUES
     ('[{r:255,g:12,b:0},{r:0,g:255,b:0},{r:0,g:0,b:255}]'),
     ('[{r:255,g:128,b:0},{r:128,g:255,b:0},{r:0,g:255,b:128},{r:0,g:128,b:255},{r:128,g:0,b:255},{r:255,g:0,b:128}]')
    v;