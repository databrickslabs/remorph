select 
     object_id, type
   , [min]    = min(object_id) over(partition by type)
   , [max]    = max(object_id) over(partition by type)
from sys.objects