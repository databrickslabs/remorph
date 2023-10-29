-- see https://docs.snowflake.com/en/sql-reference/collation

select max(no_explicit_collation), max(en_ci), max(en), max(utf_8)
    from demo;