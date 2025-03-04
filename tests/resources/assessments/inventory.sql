select DB_ID(name) as db_id,
       name,
       collation_name,
       create_date,
       SYSDATETIME() as extract_ts
from SYS.DATABASES
