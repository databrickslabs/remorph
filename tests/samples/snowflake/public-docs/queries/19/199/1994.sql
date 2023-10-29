-- see https://docs.snowflake.com/en/sql-reference/collation

create or replace table demo (
    no_explicit_collation VARCHAR,
    en_ci VARCHAR COLLATE 'en-ci',
    en VARCHAR COLLATE 'en',
    utf_8 VARCHAR collate 'utf8');
insert into demo (no_explicit_collation) values
    ('-'),
    ('+');
update demo SET
    en_ci = no_explicit_collation,
    en = no_explicit_collation,
    utf_8 = no_explicit_collation;