select  1, split_part('user@snowflake.com', '',  1) UNION
select -1, split_part('user@snowflake.com', '', -1) UNION
select  2, split_part('user@snowflake.com', '',  2) UNION
select -2, split_part('user@snowflake.com', '', -2);