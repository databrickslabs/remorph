INSERT INTO objects_1 (id, object1, variant1) 
  SELECT
    1,
    OBJECT_CONSTRUCT('a', 1, 'b', 2, 'c', 3),
    TO_VARIANT(OBJECT_CONSTRUCT('a', 1, 'b', 2, 'c', 3))
    ;