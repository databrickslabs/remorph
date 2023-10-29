-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/select-over-clause-transact-sql?view=sql-server-ver16

select 
     object_id, type
   , [min]    = min(object_id) over(partition by type)
   , [max]    = max(object_id) over(partition by type)
from sys.objects