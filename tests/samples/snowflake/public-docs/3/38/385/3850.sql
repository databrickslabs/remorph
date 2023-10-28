WITH RECURSIVE cte_name (X, Y) AS
(
  SELECT related_to_X, related_to_Y FROM table1
  UNION ALL
  SELECT also_related_to_X, also_related_to_Y
    FROM table1 JOIN cte_name ON <join_condition>
)
SELECT ... FROM ...