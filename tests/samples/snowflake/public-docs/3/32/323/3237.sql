constraintAction ::=
  {
     ADD outoflineConstraint
   | RENAME CONSTRAINT <constraint_name> TO <new_constraint_name>
   | { ALTER | MODIFY } { CONSTRAINT <constraint_name> | PRIMARY KEY | UNIQUE | FOREIGN KEY } ( <col_name> [ , ... ] )
                         [ [ NOT ] ENFORCED ] [ VALIDATE | NOVALIDATE ] [ RELY | NORELY ]
   | DROP { CONSTRAINT <constraint_name> | PRIMARY KEY | UNIQUE | FOREIGN KEY } ( <col_name> [ , ... ] )
                         [ CASCADE | RESTRICT ]
  }

  outoflineConstraint ::=
    [ CONSTRAINT <constraint_name> ]
    {
       UNIQUE [ ( <col_name> [ , <col_name> , ... ] ) ]
     | PRIMARY KEY [ ( <col_name> [ , <col_name> , ... ] ) ]
     | [ FOREIGN KEY ] [ ( <col_name> [ , <col_name> , ... ] ) ]
                          REFERENCES <ref_table_name> [ ( <ref_col_name> [ , <ref_col_name> , ... ] ) ]
    }
    [ <constraint_properties> ]