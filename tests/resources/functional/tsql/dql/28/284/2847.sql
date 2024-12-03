--Query type: DQL
SELECT YEAR(o_orderdate) FROM (VALUES ('1996-01-02')) AS T(o_orderdate);
