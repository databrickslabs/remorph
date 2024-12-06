-- tsql sql:
WITH ExpenseCTE AS ( SELECT 'Expense1' AS ExpenseName, 100.00 AS ExpenseAmount UNION ALL SELECT 'Expense2', 200.00 UNION ALL SELECT 'Expense3', 300.00 ) SELECT * FROM ExpenseCTE;
