-- tsql sql:
SELECT CONVERT(DATETIME2(0), o_orderdate, 126) AT TIME ZONE 'Central European Standard Time' FROM (VALUES ('1996-01-02')) AS o(o_orderdate);
