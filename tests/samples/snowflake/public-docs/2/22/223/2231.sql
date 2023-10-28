NTH_VALUE( <expr> , <n> ) [ FROM { FIRST | LAST } ] [ { IGNORE | RESPECT } NULLS ]
                        OVER ( [ PARTITION BY <expr1> ] ORDER BY <expr2> [ { ASC | DESC } ] [ <window_frame> ] )