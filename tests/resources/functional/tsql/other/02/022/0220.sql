--Query type: DML
CREATE TABLE budget_notification (id INT, email VARCHAR(255), notification_email VARCHAR(255));
INSERT INTO budget_notification (id, email, notification_email)
VALUES (1, 'budgets_notification', 'costadmin@domain.com, budgetadmin@domain.com');
UPDATE budget_notification
SET email = 'budgets_notification', notification_email = 'costadmin@domain.com, budgetadmin@domain.com';
SELECT *
FROM budget_notification;
-- REMORPH CLEANUP: DROP TABLE budget_notification;
