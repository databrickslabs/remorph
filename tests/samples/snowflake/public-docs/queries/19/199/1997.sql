-- see https://docs.snowflake.com/en/sql-reference/functions/to_decimal

create or replace table number_conv(expr varchar);
insert into number_conv values ('12.3456'), ('98.76546');

select expr, to_number(expr),  to_number(expr, 10, 1), to_number(expr, 10, 8) from number_conv;


select expr, to_number(expr, 10, 9) from number_conv;

100039 (22003): Numeric value '12.3456' is out of range