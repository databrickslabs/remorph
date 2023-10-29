-- see https://docs.snowflake.com/en/sql-reference/functions/to_decimal

select column1,
       to_decimal(column1, '99.9') as D0,
       to_decimal(column1, '99.9', 9, 5) as D5,
       to_decimal(column1, 'TM9', 9, 5) as TD5
from values ('1.0'), ('-12.3'), ('0.0'), ('  - 0.1   ');
