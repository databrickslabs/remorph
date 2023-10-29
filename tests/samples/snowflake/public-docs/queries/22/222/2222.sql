-- see https://docs.snowflake.com/en/sql-reference/collation

select col1 = col2,
       COLLATE(col1, 'lower') = COLLATE(col2, 'lower'),
       COLLATE(col1, 'upper') = COLLATE(col2, 'upper')
    from test_table;