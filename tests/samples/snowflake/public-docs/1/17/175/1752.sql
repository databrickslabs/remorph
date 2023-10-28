select body, regexp_instr(body, '\\S*(o)\\S*\\b', 1, 1, 0, 'ie') as result from message;

---------------------------------------------+--------------------------------------------------+
                    body                     | result                                           |
---------------------------------------------+--------------------------------------------------+
 Hellooo World                               | 7                                                |
 How are you doing today?                    | 2                                                |
 the quick brown fox jumps over the lazy dog | 13                                               |
 PACK MY BOX WITH FIVE DOZEN LIQUOR JUGS     | 10                                               |
---------------------------------------------+--------------------------------------------------+