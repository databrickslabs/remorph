--Query type: DML
WITH LocationCTE AS ( SELECT LocationName, CostRate FROM ( VALUES ('Location1', 0.00), ('Location2', 0.00) ) AS Locations (LocationName, CostRate) ) SELECT LocationName, CostRate FROM LocationCTE;
