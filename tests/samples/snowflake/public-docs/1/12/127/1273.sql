SELECT s, t, EDITDISTANCE(s, t), EDITDISTANCE(t, s), EDITDISTANCE(s, t, 3), EDITDISTANCE(s, t, -1) FROM ed;

----------------+-----------------+--------------------+--------------------+-----------------------+------------------------+
      S         |        T        | EDITDISTANCE(S, T) | EDITDISTANCE(T, S) | EDITDISTANCE(S, T, 3) | EDITDISTANCE(S, T, -1) |
----------------+-----------------+--------------------+--------------------+-----------------------+------------------------|
                |                 | 0                  | 0                  | 0                     | 0                      |
 Gute nacht     | Ich weis nicht  | 8                  | 8                  | 3                     | 0                      |
 Ich weiß nicht | Ich wei? nicht  | 1                  | 1                  | 1                     | 0                      |
 Ich weiß nicht | Ich weiss nicht | 2                  | 2                  | 2                     | 0                      |
 Ich weiß nicht | [NULL]          | [NULL]             | [NULL]             | [NULL]                | [NULL]                 |
 Snowflake      | Oracle          | 7                  | 7                  | 3                     | 0                      |
 święta         | swieta          | 2                  | 2                  | 2                     | 0                      |
 [NULL]         |                 | [NULL]             | [NULL]             | [NULL]                | [NULL]                 |
 [NULL]         | [NULL]          | [NULL]             | [NULL]             | [NULL]                | [NULL]                 |
----------------+-----------------+--------------------+--------------------+-----------------------+------------------------+