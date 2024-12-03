--Query type: DDL
WITH Region AS ( SELECT * FROM ( VALUES (1, 'North'), (2, 'South'), (3, 'East'), (4, 'West') ) AS Region ( RegionKey, RegionName ) ), Nation AS ( SELECT * FROM ( VALUES (1, 'USA'), (2, 'Canada'), (3, 'Mexico') ) AS Nation ( NationKey, NationName ) ) SELECT * FROM Region; SELECT * FROM Nation;
