-- see https://docs.snowflake.com/en/sql-reference/functions/warehouse_metering_history

select *
from table(information_schema.warehouse_metering_history('2017-10-23', '2017-10-23', 'testingwh'));