--Query type: DDL
WITH PersonCTE AS ( SELECT * FROM ( VALUES (1, 'John'), (2, 'Jane') ) AS Person(id, name) ) SELECT * FROM PersonCTE;
