-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-fulltext-stoplist-transact-sql?view=sql-server-ver16

ALTER FULLTEXT STOPLIST CombinedFunctionWordList ADD 'en' LANGUAGE 'Spanish';  
ALTER FULLTEXT STOPLIST CombinedFunctionWordList ADD 'en' LANGUAGE 'French';