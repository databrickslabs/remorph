# Syntax

```
SELECT [ ALL | DISTINCT ]  
[ TOP ( expression ) [ PERCENT ] [ WITH TIES ] ]   
<select_list>   
<select_list> ::=   
    {   
      *   
      | { table_name | view_name | table_alias }.*   
      | {  
          [ { table_name | view_name | table_alias }. ]  
               { column_name | $IDENTITY | $ROWGUID }   
          | udt_column_name [ { . | :: } { { property_name | field_name }   
            | method_name ( argument [ ,...n] ) } ]  
          | expression  
         }  
        [ [ AS ] column_alias ]   
      | column_alias = expression   
    } [ ,...n ]
```

## Select For

```
[ FOR { BROWSE | <XML> | <JSON>} ]  
  
<XML> ::=  
XML   
{   
    { RAW [ ( 'ElementName' ) ] | AUTO }   
    [   
        <CommonDirectivesForXML>   
        [ , { XMLDATA | XMLSCHEMA [ ( 'TargetNameSpaceURI' ) ] } ]   
        [ , ELEMENTS [ XSINIL | ABSENT ]   
    ]  
  | EXPLICIT   
    [   
        <CommonDirectivesForXML>   
        [ , XMLDATA ]   
    ]  
  | PATH [ ( 'ElementName' ) ]   
    [  
        <CommonDirectivesForXML>   
        [ , ELEMENTS [ XSINIL | ABSENT ] ]  
    ]  
}   
  
<CommonDirectivesForXML> ::=   
[ , BINARY BASE64 ]  
[ , TYPE ]  
[ , ROOT [ ( 'RootName' ) ] ]  
  
<JSON> ::=  
JSON   
{   
    { AUTO | PATH }   
    [   
        [ , ROOT [ ( 'RootName' ) ] ]  
        [ , INCLUDE_NULL_VALUES ]  
        [ , WITHOUT_ARRAY_WRAPPER ]  
    ]  
  
}
```

## Group by

```
-- Syntax for SQL Server and Azure SQL Database   
-- ISO-Compliant Syntax  
  
GROUP BY {
      column-expression  
    | ROLLUP ( <group_by_expression> [ ,...n ] )  
    | CUBE ( <group_by_expression> [ ,...n ] )  
    | GROUPING SETS ( <grouping_set> [ ,...n ]  )  
    | () --calculates the grand total 
} [ ,...n ] 
 
<group_by_expression> ::=  
      column-expression  
    | ( column-expression [ ,...n ] )    
   
<grouping_set> ::=  
      () --calculates the grand total  
    | <grouping_set_item>  
    | ( <grouping_set_item> [ ,...n ] )  
  
<grouping_set_item> ::=  
      <group_by_expression>  
    | ROLLUP ( <group_by_expression> [ ,...n ] )  
    | CUBE ( <group_by_expression> [ ,...n ] )  
  

-- For backward compatibility only.
-- Non-ISO-Compliant Syntax for SQL Server and Azure SQL Database 
  
GROUP BY {
       ALL column-expression [ ,...n ] 
    | column-expression [ ,...n ]  WITH { CUBE | ROLLUP }    
       }

-- Syntax for Azure Synapse Analytics 
  
GROUP BY {
      column-name [ WITH (DISTRIBUTED_AGG) ]  
    | column-expression
    | ROLLUP ( <group_by_expression> [ ,...n ] ) 
} [ ,...n ]

-- Syntax for Parallel Data Warehouse  
  
GROUP BY {
      column-name [ WITH (DISTRIBUTED_AGG) ]  
    | column-expression
} [ ,...n ]
```

# Window

```
WINDOW window_name AS (
       [ reference_window_name ]   
       [ <PARTITION BY clause> ]  
       [ <ORDER BY clause> ]   
       [ <ROW or RANGE clause> ]  
      )  
  
<PARTITION BY clause> ::=  
PARTITION BY value_expression , ... [ n ]  
  
<ORDER BY clause> ::=  
ORDER BY order_by_expression  
    [ COLLATE collation_name ]   
    [ ASC | DESC ]   
    [ ,...n ]  
  
<ROW or RANGE clause> ::=  
{ ROWS | RANGE } <window frame extent>
```

## order by

```
-- Syntax for SQL Server and Azure SQL Database  
  
ORDER BY order_by_expression  
    [ COLLATE collation_name ]   
    [ ASC | DESC ]   
    [ ,...n ]   
[ <offset_fetch> ]  
  
<offset_fetch> ::=  
{   
    OFFSET { integer_constant | offset_row_count_expression } { ROW | ROWS }  
    [  
      FETCH { FIRST | NEXT } {integer_constant | fetch_row_count_expression } { ROW | ROWS } ONLY  
    ]  
}
```

## over

```
-- Syntax for SQL Server, Azure SQL Database, and Azure Synapse Analytics  
  
OVER (   
       [ <PARTITION BY clause> ]  
       [ <ORDER BY clause> ]   
       [ <ROW or RANGE clause> ]  
      )  
  
<PARTITION BY clause> ::=  
PARTITION BY value_expression , ... [ n ]  
  
<ORDER BY clause> ::=  
ORDER BY order_by_expression  
    [ COLLATE collation_name ]   
    [ ASC | DESC ]   
    [ ,...n ]  
  
<ROW or RANGE clause> ::=  
{ ROWS | RANGE } <window frame extent>  
  
<window frame extent> ::=   
{   <window frame preceding>  
  | <window frame between>  
}  
<window frame between> ::=   
  BETWEEN <window frame bound> AND <window frame bound>  
  
<window frame bound> ::=   
{   <window frame preceding>  
  | <window frame following>  
}  
  
<window frame preceding> ::=   
{  
    UNBOUNDED PRECEDING  
  | <unsigned_value_specification> PRECEDING  
  | CURRENT ROW  
}  
  
<window frame following> ::=   
{  
    UNBOUNDED FOLLOWING  
  | <unsigned_value_specification> FOLLOWING  
  | CURRENT ROW  
}  
  
<unsigned value specification> ::=   
{  <unsigned integer literal> }
```

## Pivot

```
[ FROM { <table_source> } [ , ...n ] ]
<table_source> ::=
{
    table_or_view_name [ FOR SYSTEM_TIME <system_time> ] [ [ AS ] table_alias ]
        [ <tablesample_clause> ]
        [ WITH ( < table_hint > [ [ , ] ...n ] ) ]
    | rowset_function [ [ AS ] table_alias ]
        [ ( bulk_column_alias [ , ...n ] ) ]
    | user_defined_function [ [ AS ] table_alias ]
    | OPENXML <openxml_clause>
    | derived_table [ [ AS ] table_alias ] [ ( column_alias [ , ...n ] ) ]
    | <joined_table>
    | <pivoted_table>
    | <unpivoted_table>
    | @variable [ [ AS ] table_alias ]
    | @variable.function_call ( expression [ , ...n ] )
        [ [ AS ] table_alias ] [ (column_alias [ , ...n ] ) ]
}
<tablesample_clause> ::=
    TABLESAMPLE [ SYSTEM ] ( sample_number [ PERCENT | ROWS ] )
        [ REPEATABLE ( repeat_seed ) ]

<joined_table> ::=
{
    <table_source> <join_type> <table_source> ON <search_condition>
    | <table_source> CROSS JOIN <table_source>
    | left_table_source { CROSS | OUTER } APPLY right_table_source
    | [ ( ] <joined_table> [ ) ]
}
<join_type> ::=
    [ { INNER | { { LEFT | RIGHT | FULL } [ OUTER ] } } [ <join_hint> ] ]
    JOIN

<pivoted_table> ::=
    table_source PIVOT <pivot_clause> [ [ AS ] table_alias ]

<pivot_clause> ::=
        ( aggregate_function ( value_column [ [ , ] ...n ] )
        FOR pivot_column
        IN ( <column_list> )
    )

<unpivoted_table> ::=
    table_source UNPIVOT <unpivot_clause> [ [ AS ] table_alias ]

<unpivot_clause> ::=
    ( value_column FOR pivot_column IN ( <column_list> ) )

<column_list> ::=
    column_name [ , ...n ]

<system_time> ::=
{
      AS OF <date_time>
    | FROM <start_date_time> TO <end_date_time>
    | BETWEEN <start_date_time> AND <end_date_time>
    | CONTAINED IN (<start_date_time> , <end_date_time>)
    | ALL
}

    <date_time>::=
        <date_time_literal> | @date_time_variable

    <start_date_time>::=
        <date_time_literal> | @date_time_variable

    <end_date_time>::=
        <date_time_literal> | @date_time_variable

FROM { <table_source> [ , ...n ] }

<table_source> ::=
{
    [ database_name . [ schema_name ] . | schema_name . ] table_or_view_name [ AS ] table_or_view_alias
    [ <tablesample_clause> ]
    | derived_table [ AS ] table_alias [ ( column_alias [ , ...n ] ) ]
    | <joined_table>
}

<tablesample_clause> ::=
    TABLESAMPLE ( sample_number [ PERCENT ] ) -- Azure Synapse Analytics Dedicated SQL pool only

<joined_table> ::=
{
    <table_source> <join_type> <table_source> ON search_condition
    | <table_source> CROSS JOIN <table_source>
    | left_table_source { CROSS | OUTER } APPLY right_table_source
    | [ ( ] <joined_table> [ ) ]
}

<join_type> ::=
    [ INNER ] [ <join hint> ] JOIN
    | LEFT  [ OUTER ] JOIN
    | RIGHT [ OUTER ] JOIN
    | FULL  [ OUTER ] JOIN

<join_hint> ::=
    REDUCE
    | REPLICATE
    | REDISTRIBUTE
```

## match

```
MATCH (<graph_search_pattern>)

<graph_search_pattern>::=
  {  
      <simple_match_pattern> 
    | <arbitrary_length_match_pattern>  
    | <arbitrary_length_match_last_node_predicate> 
  }

<simple_match_pattern>::=
  {
      LAST_NODE(<node_alias>) | <node_alias>   { 
          { <-( <edge_alias> )- } 
        | { -( <edge_alias> )-> }
        <node_alias> | LAST_NODE(<node_alias>)
        } 
  }
  [ { AND } { ( <simple_match_pattern> ) } ]
  [ ,...n ]

<node_alias> ::=
  node_table_name | node_table_alias 

<edge_alias> ::=
  edge_table_name | edge_table_alias


<arbitrary_length_match_pattern>  ::=
  { 
    SHORTEST_PATH( 
      <arbitrary_length_pattern> 
      [ { AND } { <arbitrary_length_pattern> } ] 
      [ ,…n] 
    )
  } 

<arbitrary_length_match_last_node_predicate> ::=
  {  LAST_NODE( <node_alias> ) = LAST_NODE( <node_alias> ) }


<arbitrary_length_pattern> ::=
	{  LAST_NODE( <node_alias> )   | <node_alias>
     ( <edge_first_al_pattern> [<edge_first_al_pattern>…,n] )
     <al_pattern_quantifier> 
  }
 	|  ( {<node_first_al_pattern> [<node_first_al_pattern> …,n] )
  	  	<al_pattern_quantifier> 
        LAST_NODE( <node_alias> ) | <node_alias> 
 }
	
<edge_first_al_pattern> ::=
  { (  
        { -( <edge_alias> )->   } 
      | { <-( <edge_alias> )- } 
      <node_alias>
	  ) 
  } 

<node_first_al_pattern> ::=
  { ( 
      <node_alias> 
        { <-( <edge_alias> )- } 
      | { -( <edge_alias> )-> }
 	  ) 
  } 


<al_pattern_quantifier> ::=
  {
	    +
	  | { 1 , n }
  }

n -  positive integer only.
```