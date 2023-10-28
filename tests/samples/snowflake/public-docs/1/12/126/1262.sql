SELECT * FROM strings;

---------+
    S    |
---------+
 coffee  |
 ice tea |
 latte   |
 tea     |
 [NULL]  |
---------+

SELECT * FROM strings WHERE ENDSWITH(s, 'te');

-------+
   S   |
-------+
 latte |
-------+