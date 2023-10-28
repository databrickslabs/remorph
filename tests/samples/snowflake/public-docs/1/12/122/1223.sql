select * from strings;

---------+
    S    |
---------+
 coffee  |
 ice tea |
 latte   |
 tea     |
 [NULL]  |
---------+

select * from strings where startswith(s, 'te');

-----+
  S  |
-----+
 tea |
-----+