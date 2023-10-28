select t1.c1
    from t1, t2, t3
    where t1.c1 = t2.c2 (+)
      and t2.c2 = t3.c3 (+);