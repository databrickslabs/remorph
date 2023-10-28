SELECT SYSTEM$TYPEOF('something') FROM (values(1)) v;

----------------------------+
 SYSTEM$TYPEOF('SOMETHING') |
----------------------------+
 VARCHAR(9)[LOB]            |
----------------------------+