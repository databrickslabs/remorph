-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/openxml-transact-sql?view=sql-server-ver16

DECLARE @idoc INT, @doc VARCHAR(1000);

SET @doc = '
<ROOT>
<Customer CustomerID="VINET" ContactName="Paul Henriot">
   <Order OrderID="10248" CustomerID="VINET" EmployeeID="5"
           OrderDate="1996-07-04T00:00:00">
      <OrderDetail ProductID="11" Quantity="12"/>
      <OrderDetail ProductID="42" Quantity="10"/>
   </Order>
</Customer>
<Customer CustomerID="LILAS" ContactName="Carlos Gonzlez">v
   <Order OrderID="10283" CustomerID="LILAS" EmployeeID="3"
           OrderDate="1996-08-16T00:00:00">
      <OrderDetail ProductID="72" Quantity="3"/>
   </Order>
</Customer>
</ROOT>';

--Create an internal representation of the XML document.
EXEC sp_xml_preparedocument @idoc OUTPUT, @doc;

-- SELECT stmt using OPENXML rowset provider
SELECT *
FROM OPENXML(@idoc, '/ROOT/Customer/Order/OrderDetail', 2) WITH (
        OrderID INT '../@OrderID',
        CustomerID VARCHAR(10) '../@CustomerID',
        OrderDate DATETIME '../@OrderDate',
        ProdID INT '@ProductID',
        Qty INT '@Quantity'
    );