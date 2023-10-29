-- see https://docs.snowflake.com/en/sql-reference/name-resolution

SELECT current_schema();


CREATE DATABASE db1;


SELECT current_schema();


CREATE SCHEMA sch1;


SELECT current_schema();


USE SCHEMA public;


SELECT current_schema();
