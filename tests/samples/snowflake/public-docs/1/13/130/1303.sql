SELECT * FROM persons;

------+---------------------+
 NAME |      CHILDREN       |
------+---------------------+
 Mark | Marky,Mark Jr,Maria |
 John | Johnny,Jane         |
------+---------------------+

SELECT name, C.value::string AS childName
FROM persons,
     LATERAL FLATTEN(input=>split(children, ',')) C;

------+-----------+
 NAME | CHILDNAME |
------+-----------+
 John | Johnny    |
 John | Jane      |
 Mark | Marky     |
 Mark | Mark Jr   |
 Mark | Maria     |
------+-----------+