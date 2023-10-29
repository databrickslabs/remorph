-- see https://docs.snowflake.com/en/sql-reference/functions/result_scan

SELECT c2 FROM TABLE(RESULT_SCAN('ce6687a4-331b-4a57-a061-02b2b0f0c17c'));