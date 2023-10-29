-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-table-transact-sql?view=sql-server-ver16

[ledger_start_transaction_id] BIGINT GENERATED ALWAYS AS TRANSACTION_ID START HIDDEN NOT NULL
[ledger_end_transaction_id] BIGINT GENERATED ALWAYS AS TRANSACTION_ID END HIDDEN NULL
[ledger_start_sequence_number] BIGINT GENERATED ALWAYS AS SEQUENCE_NUMBER START HIDDEN NOT NULL
[ledger_end_sequence_number] BIGINT GENERATED ALWAYS AS SEQUENCE_NUMBER END HIDDEN NULL