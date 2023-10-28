SELECT tleft.c1   
FROM tleft   
RIGHT JOIN tright   
ON tleft.c1 = tright.c1   
WHERE tright.c1 <> 2 ;