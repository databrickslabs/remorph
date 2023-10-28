select 
      object_id
    , [min]    = min(object_id) over()
    , [max]    = max(object_id) over()
from sys.objects