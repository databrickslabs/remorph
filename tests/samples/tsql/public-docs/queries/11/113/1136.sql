-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-table-transact-sql?view=sql-server-ver16

CREATE SCHEMA [AccessControl];
GO
CREATE TABLE [AccessControl].[KeyCardEvents]
(
    EmployeeID INT NOT NULL,
    AccessOperationDescription NVARCHAR (MAX) NOT NULL,
    [Timestamp] Datetime2 NOT NULL,
    StartTransactionId BIGINT GENERATED ALWAYS AS TRANSACTION_ID START HIDDEN NOT NULL,
    StartSequenceNumber BIGINT GENERATED ALWAYS AS SEQUENCE_NUMBER START HIDDEN NOT NULL
)
WITH (
    LEDGER = ON (
        LEDGER_VIEW = [AccessControl].[KeyCardEventsLedger] (
            TRANSACTION_ID_COLUMN_NAME = TransactionId,
            SEQUENCE_NUMBER_COLUMN_NAME = SequenceNumber,
            OPERATION_TYPE_COLUMN_NAME = OperationId,
            OPERATION_TYPE_DESC_COLUMN_NAME = OperationTypeDescription
        ),
        APPEND_ONLY = ON
    )
);
GO