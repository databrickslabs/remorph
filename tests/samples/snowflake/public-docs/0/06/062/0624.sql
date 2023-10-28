SET var_2 = 'value_2';
SELECT 
    GETVARIABLE('var_2'),
    GETVARIABLE('VAR_2'),
    SESSION_CONTEXT('var_2'),
    SESSION_CONTEXT('VAR_2'),
    $var_2,
    $VAR_2;