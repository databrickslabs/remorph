-- tsql sql:
SELECT *
FROM (
    VALUES ('Assets', 'Cash'),
           ('Assets', 'Bank'),
           ('Assets', 'Investments'),
           ('Assets', 'Accounts Receivable'),
           ('Assets', 'Inventory')
) AS Account (AccountType, AccountName)
WHERE AccountType = 'Assets';
