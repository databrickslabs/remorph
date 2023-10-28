ALTER VIEW [ IF EXISTS ] <name> RENAME TO <new_name>

ALTER VIEW [ IF EXISTS ] <name> SET COMMENT = '<string_literal>'

ALTER VIEW [ IF EXISTS ] <name> UNSET COMMENT

ALTER VIEW <name> SET SECURE

ALTER VIEW <name> SET CHANGE_TRACKING =  { TRUE | FALSE }

ALTER VIEW <name> UNSET SECURE

ALTER VIEW [ IF EXISTS ] <name> SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER VIEW [ IF EXISTS ] <name> UNSET TAG <tag_name> [ , <tag_name> ... ]

ALTER VIEW [ IF EXISTS ] <name>
  ADD ROW ACCESS POLICY <policy_name> ON (<col_name> [ , ... ])

ALTER VIEW [ IF EXISTS ] <name>
  DROP ROW ACCESS POLICY <policy_name>

ALTER VIEW [ IF EXISTS ] <name>
  DROP ROW ACCESS POLICY <policy_name>
  , ADD ROW ACCESS POLICY <policy_name> ON (<col_name> [ , ... ])

ALTER VIEW [ IF EXISTS ] <name> DROP ALL ROW ACCESS POLICIES

ALTER VIEW <name> { ALTER | MODIFY } [ COLUMN ] <col_name> SET MASKING POLICY <policy_name> [ USING ( <col_name> , cond_col_1 , ... ) ]
                                                                                            [ FORCE ]

ALTER VIEW <name> { ALTER | MODIFY } [ COLUMN ] <col_name> UNSET MASKING POLICY

ALTER VIEW <name> { ALTER | MODIFY } [ COLUMN ] <col_name> SET TAG <tag_name> = '<string_literal>' [ , <tag_name> = '<string_literal>' ... ]

ALTER VIEW <name> { ALTER | MODIFY } COLUMN <col_name> UNSET TAG <tag_name> [ , <tag_name> ... ]