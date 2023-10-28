[ WITH [ RECURSIVE ]
       <cte_name1> ( <cte_column_list> ) AS ( anchorClause UNION ALL recursiveClause )
   [ , <cte_name2> ( <cte_column_list> ) AS ( anchorClause UNION ALL recursiveClause ) ]
   [ , <cte_nameN> ( <cte_column_list> ) AS ( anchorClause UNION ALL recursiveClause ) ]
]
SELECT ...