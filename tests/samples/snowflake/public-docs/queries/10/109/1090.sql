-- see https://docs.snowflake.com/en/sql-reference/name-resolution

SELECT CURRENT_DATABASE();


CREATE DATABASE db1;


SELECT CURRENT_DATABASE();


USE DATABASE testdb;


SELECT current_database();
