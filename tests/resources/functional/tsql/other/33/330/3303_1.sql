--Query type: DDL
CREATE TABLE #auditOrderData
(
    audit_log_id UNIQUEIDENTIFIER DEFAULT (NEWID()),
    audit_log_type CHAR(3),
    audit_order_id INT,
    audit_order_total DECIMAL(10, 2),
    audit_order_date DATE,
    audit_user SYSNAME DEFAULT (SUSER_SNAME()),
    audit_changed DATETIME DEFAULT (GETDATE())
);

INSERT INTO #auditOrderData
(
    audit_log_type,
    audit_order_id,
    audit_order_total,
    audit_order_date
)
SELECT
    audit_log_type,
    audit_order_id,
    audit_order_total,
    audit_order_date
FROM
(
    VALUES
    (
        'ORD',
        1,
        100.00,
        CAST(GETDATE() AS DATE)
    )
) AS auditOrderData
(
    audit_log_type,
    audit_order_id,
    audit_order_total,
    audit_order_date
);

SELECT * FROM #auditOrderData;
-- REMORPH CLEANUP: DROP TABLE #auditOrderData;
