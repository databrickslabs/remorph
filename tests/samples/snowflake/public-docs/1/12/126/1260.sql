SELECT s, t, JAROWINKLER_SIMILARITY(s, t), JAROWINKLER_SIMILARITY(t, s) FROM ed;

----------------+-----------------+------------------------------+------------------------------+
      S         |        T        | JAROWINKLER_SIMILARITY(S, T) | JAROWINKLER_SIMILARITY(T, S) |
----------------+-----------------+------------------------------+------------------------------+
                |                 | 0                            | 0                            |
 Gute nacht     | Ich weis nicht  | 56                           | 56                           |
 Ich weiß nicht | Ich wei? nicht  | 98                           | 98                           |
 Ich weiß nicht | Ich weiss nicht | 97                           | 97                           |
 Ich weiß nicht | [NULL]          | [NULL]                       | [NULL]                       |
 Snowflake      | Oracle          | 61                           | 61                           |
 święta         | swieta          | 77                           | 77                           |
 [NULL]         |                 | [NULL]                       | [NULL]                       |
 [NULL]         | [NULL]          | [NULL]                       | [NULL]                       |
----------------+-----------------+------------------------------+------------------------------+