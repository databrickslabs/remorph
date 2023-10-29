-- see https://docs.snowflake.com/en/sql-reference/functions/regexp_substr

-- Prepare example
create or replace table message(body varchar(255));

insert into message values
('Hellooo World'),
('How are you doing today?'),
('the quick brown fox jumps over the lazy dog'),
('PACK MY BOX WITH FIVE DOZEN LIQUOR JUGS');