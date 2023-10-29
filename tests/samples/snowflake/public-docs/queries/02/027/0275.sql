-- see https://docs.snowflake.com/en/sql-reference/functions/result_scan

CREATE OR REPLACE PROCEDURE return_JSON()
    RETURNS VARCHAR
    LANGUAGE JavaScript
    AS
    $$
        return '{"keyA": "ValueA", "keyB": "ValueB"}';
    $$
    ;