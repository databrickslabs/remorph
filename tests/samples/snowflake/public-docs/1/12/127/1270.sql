SELECT * from strings;

---------+
    S    |
---------+
 coffee  |
 ice tea |
 latte   |
 tea     |
 [NULL]  |
---------+

SELECT * FROM strings WHERE CONTAINS(s, 'te');

---------+
    S    |
---------+
 ice tea |
 latte   |
 tea     |
---------+