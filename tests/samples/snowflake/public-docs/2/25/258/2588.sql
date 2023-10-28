SELECT ARRAYS_OVERLAP(array_construct('hello', 'aloha'), 
                      array_construct('hello', 'hi', 'hey'))
  AS Overlap;
SELECT ARRAYS_OVERLAP(array_construct('hello', 'aloha'), 
                      array_construct('hola', 'bonjour', 'ciao'))
  AS Overlap;
SELECT ARRAYS_OVERLAP(array_construct(object_construct('a',1,'b',2), 1, 2), 
                      array_construct(object_construct('b',2,'c',3), 3, 4))
  AS Overlap;
SELECT ARRAYS_OVERLAP(array_construct(object_construct('a',1,'b',2), 1, 2), 
                      array_construct(object_construct('a',1,'b',2), 3, 4))
  AS Overlap;