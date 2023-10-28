COUNT( [ DISTINCT ] <expr1> [ , <expr2> ... ] ) OVER (
                                                     [ PARTITION BY <expr3> ]
                                                     [ ORDER BY <expr4> [ ASC | DESC ] [ <window_frame> ] ]
                                                     )