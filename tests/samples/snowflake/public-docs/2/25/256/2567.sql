SELECT OBJECT_INSERT(OBJECT_INSERT(OBJECT_CONSTRUCT(),'k1', 100),'k1','string-value', TRUE) AS obj;

------------------------+
          OBJ           |
------------------------+
 {                      |
   "k1": "string-value" |
 }                      |
------------------------+