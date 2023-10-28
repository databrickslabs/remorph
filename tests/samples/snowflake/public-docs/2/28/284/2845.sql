CASE ( <expression_to_match> )
    WHEN <expression> THEN
        <statement>;
        [ <statement>; ... ]
    [ WHEN ... ]
    [ ELSE
        <statement>;
        [ <statement>; ... ]
    ]
END [ CASE ] ;