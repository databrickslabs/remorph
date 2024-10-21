--Query type: DDL
CREATE TABLE #LineItem
(
    OrderKey INT
);

INSERT INTO #LineItem
VALUES
(
    1
);

CREATE NONCLUSTERED INDEX IX_LineItem_OrderKey
ON #LineItem
(
    OrderKey
)
WITH
(
    FILLFACTOR = 80,
    PAD_INDEX = ON
);