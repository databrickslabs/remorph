-- tsql sql:
DECLARE @x XML;
DECLARE @f BIT;
SET @x = (SELECT x FROM (VALUES (CAST('<Someotherdate>2003-02-02Z</Someotherdate>' AS XML))) AS v(x));
SET @f = @x.exist('/Someotherdate[(text()[1] cast as xs:date ?) = xs:date("2003-02-02Z") ]');
SELECT @f;
