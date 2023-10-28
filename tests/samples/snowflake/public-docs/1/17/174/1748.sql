select body, regexp_instr(body, '\\b\\S*o\\S*\\b', 3, 3) as result from message;

---------------------------------------------+-----------------------------------------+
                    body                     | result                                  |
---------------------------------------------+-----------------------------------------+
 Hellooo World                               | 0                                       |
 How are you doing today?                    | 19                                      |
 the quick brown fox jumps over the lazy dog | 27                                      |
 PACK MY BOX WITH FIVE DOZEN LIQUOR JUGS     | 0                                       |
---------------------------------------------+-----------------------------------------+