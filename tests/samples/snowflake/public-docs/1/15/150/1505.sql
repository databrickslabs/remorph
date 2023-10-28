select *
from table(information_schema.replication_group_refresh_progress('rg1'));