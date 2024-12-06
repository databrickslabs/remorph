-- tsql sql:
SELECT o_orderpriority, CASE WHEN o_orderpriority = '1-URGENT' THEN 'High Priority' WHEN o_orderpriority = '2-HIGH' THEN 'Medium Priority' END AS priority FROM (VALUES ('1-URGENT'), ('2-HIGH'), ('3-MEDIUM')) o (o_orderpriority);
