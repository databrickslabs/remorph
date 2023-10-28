select 
      object_id, type
    , [min]    = min(object_id) over(partition by type order by object_id)
    , [max]    = max(object_id) over(partition by type order by object_id)
from sys.objects