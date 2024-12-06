-- tsql sql:
WITH mycte AS ( SELECT id, name FROM ( VALUES (1, 'John'), (2, 'Jane'), (3, 'Bob') ) AS t (id, name) ) SELECT * FROM mycte WITH (TABLOCK, INDEX (0));
