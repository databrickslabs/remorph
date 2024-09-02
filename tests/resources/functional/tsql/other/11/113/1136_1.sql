--Query type: DDL
CREATE TABLE Promotions
(
    PromotionID INT,
    ProductID INT,
    Discount DECIMAL(10, 2),
    StartDate DATE,
    EndDate DATE,
    StartTransactionId BIGINT GENERATED ALWAYS AS TRANSACTION_ID START HIDDEN NOT NULL,
    StartSequenceNumber BIGINT GENERATED ALWAYS AS SEQUENCE_NUMBER START HIDDEN NOT NULL
)
WITH (
    LEDGER = ON (
        LEDGER_VIEW = dbo.PromotionsLedger (
            TRANSACTION_ID_COLUMN_NAME = TransactionId,
            SEQUENCE_NUMBER_COLUMN_NAME = SequenceNumber,
            OPERATION_TYPE_COLUMN_NAME = OperationId,
            OPERATION_TYPE_DESC_COLUMN_NAME = OperationTypeDescription
        ),
        APPEND_ONLY = ON
    )
);

INSERT INTO Promotions (PromotionID, ProductID, Discount, StartDate, EndDate)
SELECT PromotionID, ProductID, Discount, StartDate, EndDate
FROM (
    VALUES (1, 10, 0.10, '2022-01-01', '2022-12-31')
) AS PromotionsCTE (PromotionID, ProductID, Discount, StartDate, EndDate);

SELECT * FROM Promotions;
-- REMORPH CLEANUP: DROP TABLE Promotions;