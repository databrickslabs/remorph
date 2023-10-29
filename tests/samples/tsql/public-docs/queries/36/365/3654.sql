-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/select-over-clause-transact-sql?view=sql-server-ver16

select 
      object_id
    , [min]    = min(object_id) over()
    , [max]    = max(object_id) over()
from sys.objects