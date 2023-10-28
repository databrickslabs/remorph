SELECT
  OBJECT_INSERT(OBJECT_INSERT(OBJECT_INSERT(OBJECT_CONSTRUCT(), 'Key_One', PARSE_JSON('NULL')), 'Key_Two', NULL), 'Key_Three', 'null')
  AS obj;

-----------------------+
          OBJ          |
-----------------------+
 {                     |
   "Key_One": null,    |
   "Key_Three": "null" |
 }                     |
-----------------------+