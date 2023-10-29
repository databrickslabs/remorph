-- see https://docs.snowflake.com/en/sql-reference/name-resolution

select current_schemas();


use database mytestdb;

select current_schemas();


create schema private;

select current_schemas();
