WITH
    l AS (
         SELECT 'a' AS userid
         ),
    r AS (
         SELECT 'b' AS userid
         )
  SELECT *
    FROM l LEFT JOIN r USING(userid)
;