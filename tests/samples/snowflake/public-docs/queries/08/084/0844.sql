-- see https://docs.snowflake.com/en/sql-reference/functions/soundex

SELECT * 
    FROM sounding_board AS board, sounding_bored AS bored 
    WHERE bored.v = board.v;