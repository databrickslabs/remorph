create or replace temporary table vartab (ID INTEGER, v VARCHAR);

insert into vartab (id, v) VALUES 
    (1, '[-1, 12, 289, 2188, false,]'), 
    (2, '{ "x" : "abc", "y" : false, "z": 10} '),
    (3, '{ "bad" : "json", "missing" : true, "close_brace": 10 ');