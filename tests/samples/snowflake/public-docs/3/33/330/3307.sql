inlineConstraint ::=
  [ CONSTRAINT <constraint_name> ]
  { UNIQUE
    | PRIMARY KEY
    | [ FOREIGN KEY ] REFERENCES <ref_table_name> [ ( <ref_col_name> ) ]
  }
  [ <constraint_properties> ]