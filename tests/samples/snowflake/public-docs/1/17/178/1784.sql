select *
from t1
    join t2 on t1.a = t2.a
    join t3 on t1.b = t3.b
    join t4 on t1.c = t4.c
;