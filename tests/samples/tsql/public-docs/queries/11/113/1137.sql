-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-table-transact-sql?view=sql-server-ver16

CREATE SCHEMA [HR];
GO
CREATE TABLE [HR].[Employees]
(
    EmployeeID INT NOT NULL PRIMARY KEY,
    Salary Money NOT NULL,
    StartTransactionId BIGINT GENERATED ALWAYS AS TRANSACTION_ID START HIDDEN NOT NULL,
    EndTransactionId BIGINT GENERATED ALWAYS AS TRANSACTION_ID END HIDDEN NULL,
    StartSequenceNumber BIGINT GENERATED ALWAYS AS SEQUENCE_NUMBER START HIDDEN NOT NULL,
    EndSequenceNumber BIGINT GENERATED ALWAYS AS SEQUENCE_NUMBER END HIDDEN NULL,
    ValidFrom DATETIME2 GENERATED ALWAYS AS ROW START HIDDEN NOT NULL,
    ValidTo DATETIME2 GENERATED ALWAYS AS ROW END HIDDEN NOT NULL,
    PERIOD FOR SYSTEM_TIME (ValidFrom, ValidTo)
)
WITH (
    SYSTEM_VERSIONING = ON (HISTORY_TABLE = [HR].[EmployeesHistory]),
    LEDGER = ON (
        LEDGER_VIEW = [HR].[EmployeesLedger] (
            TRANSACTION_ID_COLUMN_NAME = TransactionId,
            SEQUENCE_NUMBER_COLUMN_NAME = SequenceNumber,
            OPERATION_TYPE_COLUMN_NAME = OperationId,
            OPERATION_TYPE_DESC_COLUMN_NAME = OperationTypeDescription
        )
    )
);
GO