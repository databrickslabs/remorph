-- Find a friend
   SELECT Person2.name AS FriendName
   FROM Person Person1, friend, Person Person2
   WHERE MATCH(Person1-(friend)->Person2);
   
-- The pattern can also be expressed as below

   SELECT Person2.name AS FriendName
   FROM Person Person1, friend, Person Person2 
   WHERE MATCH(Person2<-(friend)-Person1);


-- Find 2 people who are both friends with same person
   SELECT Person1.name AS Friend1, Person2.name AS Friend2
   FROM Person Person1, friend friend1, Person Person2, 
        friend friend2, Person Person0
   WHERE MATCH(Person1-(friend1)->Person0<-(friend2)-Person2);
   
-- this pattern can also be expressed as below

   SELECT Person1.name AS Friend1, Person2.name AS Friend2
   FROM Person Person1, friend friend1, Person Person2, 
        friend friend2, Person Person0
   WHERE MATCH(Person1-(friend1)->Person0 AND Person2-(friend2)->Person0);