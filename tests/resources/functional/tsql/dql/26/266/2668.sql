-- tsql sql:
SELECT LTRIM(orders.o_comment) AS trimmed_comment FROM (VALUES ('     Five spaces are at the beginning of this string.')) AS orders(o_comment);
