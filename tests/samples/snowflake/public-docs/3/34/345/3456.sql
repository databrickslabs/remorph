MATCH_RECOGNIZE (
    [ PARTITION BY <expr> [, ... ] ]
    [ ORDER BY <expr> [, ... ] ]
    [ MEASURES <expr> [AS] <alias> [, ... ] ]
    [ ONE ROW PER MATCH |
      ALL ROWS PER MATCH [ { SHOW EMPTY MATCHES | OMIT EMPTY MATCHES | WITH UNMATCHED ROWS } ]
      ]
    [ AFTER MATCH SKIP
          {
          PAST LAST ROW   |
          TO NEXT ROW   |
          TO [ { FIRST | LAST} ] <symbol>
          }
      ]
    PATTERN ( <pattern> )
    DEFINE <symbol> AS <expr> [, ... ]
)