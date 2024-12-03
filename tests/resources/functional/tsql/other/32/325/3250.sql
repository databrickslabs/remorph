--Query type: TCL
BEGIN TRAN;
SELECT APPLOCK_MODE('public', 'Form1', 'Transaction');
EXEC sp_getapplock @DbPrincipal = 'public', @Resource = 'Form1', @LockMode = 'Shared', @LockOwner = 'Transaction';
