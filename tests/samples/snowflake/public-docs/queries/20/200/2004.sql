-- see https://docs.snowflake.com/en/sql-reference/data-type-conversion

create or replace table tmp (
    varchar1 varchar, 
    float1 float, 
    variant1 variant
    );

insert into tmp select '5.000', 5.000, parse_json('{"Loan Number": 5.000}');