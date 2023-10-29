-- see https://docs.snowflake.com/en/sql-reference/constructs/with

select musician_id, musician_name from view_musicians_in_bands where band_name = 'Santana'
intersect
select musician_id, musician_name from view_musicians_in_bands where band_name = 'Journey'
order by musician_ID;