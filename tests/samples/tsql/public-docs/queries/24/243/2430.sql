-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/base64-encode-transact-sql?view=azuresqldb-current

SELECT Base64_Encode(0xA9) as "Encoded &copy; symbol";