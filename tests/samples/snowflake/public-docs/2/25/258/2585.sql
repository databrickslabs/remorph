SELECT object_agg(k, v) FROM objectagg_example GROUP BY g;

-------------------+
 OBJECT_AGG(K, V)  |
-------------------+
 {                 |
   "name": "Sue",  |
   "zip": 94401    |
 }                 |
 {                 |
   "age": 21,      |
   "name": "Joe"   |
 }                 |
-------------------+