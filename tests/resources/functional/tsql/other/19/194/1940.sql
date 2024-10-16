--Query type: DML
DELETE t FROM Table1 t WHERE t.id IN ( SELECT id FROM ( VALUES (1, 'data1'), (2, 'data2') ) AS derivedTable(id, data) WHERE derivedTable.id = t.id );