searchOptimizationAction ::=
  {
     ADD SEARCH OPTIMIZATION [
       ON <search_method_with_target> [ , <search_method_with_target> ... ]
     ]

   | DROP SEARCH OPTIMIZATION [
       ON { <search_method_with_target> | <column_name> | <expression_id> }
          [ , ... ]
     ]

  }