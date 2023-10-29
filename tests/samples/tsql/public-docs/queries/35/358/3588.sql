-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/text-and-image-functions-textvalid-transact-sql?view=sql-server-ver16

USE pubs;  
GO  
SELECT pub_id, 'Valid (if 1) Text data'   
   = TEXTVALID ('pub_info.logo', TEXTPTR(logo))   
FROM pub_info  
ORDER BY pub_id;  
GO