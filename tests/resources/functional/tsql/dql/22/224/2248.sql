-- tsql sql:
WITH MyCTE AS ( SELECT * FROM ( VALUES ('ExpenseQueue') ) AS T (MyQueue) ) SELECT * FROM MyCTE;
