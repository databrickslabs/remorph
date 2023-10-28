objectReference ::=
   {
      [<namespace>.]<object_name>
           [ AT | BEFORE ( <object_state> ) ]
           [ CHANGES ( <change_tracking_type> ) ]
           [ MATCH_RECOGNIZE ]
           [ PIVOT | UNPIVOT ]
           [ [ AS ] <alias_name> ]
           [ SAMPLE ]
     | <table_function>
           [ PIVOT | UNPIVOT ]
           [ [ AS ] <alias_name> ]
           [ SAMPLE ]
     | ( VALUES (...) )
           [ SAMPLE ]
     | [ LATERAL ] ( <subquery> )
           [ [ AS ] <alias_name> ]
     | @[<namespace>.]<stage_name>[/<path>]
           [ ( FILE_FORMAT => <format_name>, PATTERN => '<regex_pattern>' ) ]
           [ [AS] <alias_name> ]
     | DIRECTORY( @<stage_name> )
   }