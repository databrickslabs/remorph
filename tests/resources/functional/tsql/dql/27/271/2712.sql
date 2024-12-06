-- tsql sql:
SELECT p_productkey, p_name, p_comment
FROM (
    VALUES (1, 'Product1', 'Comment1'),
           (2, 'Product2', 'Comment2'),
           (3, 'Product3', 'Comment3')
) AS p (p_productkey, p_name, p_comment)
JOIN STRING_SPLIT('1,2,3', ',') AS s
    ON s.value = p.p_productkey
