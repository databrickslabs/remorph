-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/get-bit-transact-sql?view=sql-server-ver16

SELECT GET_BIT ( 0xabcdef, 2 ) as Get_2nd_Bit,
GET_BIT ( 0xabcdef, 4 ) as Get_4th_Bit;