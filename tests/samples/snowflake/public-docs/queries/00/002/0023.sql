-- see https://docs.snowflake.com/en/sql-reference/functions/rlike

-- Escape the backslash character (\) in \w and \d

SELECT RLIKE('800-456-7891','[2-9]\\d{2}-\\d{3}-\\d{4}') AS matches_phone_number;


SELECT RLIKE('jsmith@email.com','\\w+@[a-zA-Z_]+?\\.[a-zA-Z]{2,3}') AS matches_email_address;


-- Alternatively, rewrite the statements and avoid sequences that rely on the backslash character

SELECT RLIKE('800-456-7891','[2-9][0-9]{2}-[0-9]{3}-[0-9]{4}') AS matches_phone_number;


SELECT RLIKE('jsmith@email.com','[a-zA-Z_]+@[a-zA-Z_]+?\\.[a-zA-Z]{2,3}') AS matches_email_address;
