-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/openxml-transact-sql?view=sql-server-ver16

DECLARE @idoc INT, @doc VARCHAR(1000);

SET @doc = '
<ROOT>
<Customers CustomerID="VINET" ContactName="Paul Henriot">
   <Orders CustomerID="VINET" EmployeeID="5" OrderDate=
           "1996-07-04T00:00:00">
      <Order_x0020_Details OrderID="10248" ProductID="11" Quantity="12"/>
      <Order_x0020_Details OrderID="10248" ProductID="42" Quantity="10"/>
   </Orders>
</Customers>
<Customers CustomerID="LILAS" ContactName="Carlos Gonzlez">
   <Orders CustomerID="LILAS" EmployeeID="3" OrderDate=
           "1996-08-16T00:00:00">
      <Order_x0020_Details OrderID="10283" ProductID="72" Quantity="3"/>
   </Orders>
</Customers>
</ROOT>';

--Create an internal representation of the XML document.
EXEC sp_xml_preparedocument @idoc OUTPUT, @doc;

-- SELECT statement that uses the OPENXML rowset provider.
SELECT * FROM OPENXML(@idoc, '/ROOT/Customers')

EXEC sp_xml_removedocument @idoc;