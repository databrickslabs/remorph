--Query type: DQL
SELECT comments FROM (VALUES ('vital safety components'), ('other comments')) AS orders (comments) WHERE comments LIKE '%vital safety components%';
