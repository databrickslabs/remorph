CREATE OR REPLACE TABLE array_demo (ID INTEGER, array1 ARRAY, array2 ARRAY, tip VARCHAR);

INSERT INTO array_demo (ID, array1, array2, tip)
    SELECT 1, ARRAY_CONSTRUCT(1, 2), ARRAY_CONSTRUCT(3, 4), 'non-overlapping';
INSERT INTO array_demo (ID, array1, array2, tip)
    SELECT 2, ARRAY_CONSTRUCT(1, 2, 3), ARRAY_CONSTRUCT(3, 4, 5), 'value 3 overlaps';
INSERT INTO array_demo (ID, array1, array2, tip)
    SELECT 3, ARRAY_CONSTRUCT(1, 2, 3, 4), ARRAY_CONSTRUCT(3, 4, 5), 'values 3 and 4 overlap';
INSERT INTO array_demo (ID, array1, array2, tip)
    SELECT 4, ARRAY_CONSTRUCT(NULL, 102, NULL), ARRAY_CONSTRUCT(NULL, NULL, 103), 'NULLs overlap';
INSERT INTO array_demo (ID, array1, array2, tip)
    SELECT 5, array_construct(object_construct('a',1,'b',2), 1, 2),
              array_construct(object_construct('a',1,'b',2), 3, 4), 
              'the objects in the array match';
INSERT INTO array_demo (ID, array1, array2, tip)
    SELECT 6, array_construct(object_construct('a',1,'b',2), 1, 2),
              array_construct(object_construct('b',2,'c',3), 3, 4), 
              'neither the objects nor any other values match';
INSERT INTO array_demo (ID, array1, array2, tip)
    SELECT 7, array_construct(object_construct('a',1, 'b',2, 'c',3)),
              array_construct(object_construct('c',3, 'b',2, 'a',1)), 
              'the objects contain the same values, but in different order';