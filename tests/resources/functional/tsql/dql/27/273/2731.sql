--Query type: DQL
SELECT RIGHT(v.string, 2) AS last_two_chars FROM (VALUES ('abcdefghij')) AS v(string);
