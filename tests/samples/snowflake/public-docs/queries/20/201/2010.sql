-- see https://docs.snowflake.com/en/sql-reference/functions/as

create or replace table vartab (n number(2), v variant);

insert into vartab
    select column1 as n, parse_json(column2) as v
    from values (1, 'null'), 
                (2, null), 
                (3, 'true'),
                (4, '-17'), 
                (5, '123.12'), 
                (6, '1.912e2'),
                (7, '"Om ara pa ca na dhih"  '), 
                (8, '[-1, 12, 289, 2188, false,]'), 
                (9, '{ "x" : "abc", "y" : false, "z": 10} ') 
       AS vals;