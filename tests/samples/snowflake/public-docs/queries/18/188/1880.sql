-- see https://docs.snowflake.com/en/sql-reference/name-resolution

SHOW PARAMETERS LIKE 'search_path';


SELECT current_schemas();


CREATE DATABASE db1;


USE SCHEMA public;


SELECT current_schemas();


ALTER SESSION SET search_path='$current, $public, testdb.public';


SHOW PARAMETERS LIKE 'search_path';


SELECT current_schemas();
