-- see https://docs.snowflake.com/en/sql-reference/functions/bitxor

INSERT INTO bits (ID, bit1, bit2) VALUES 
    (   11,    1,     1),    -- Bits are all the same.
    (   24,    2,     4),    -- Bits are all different.
    (   42,    4,     2),    -- Bits are all different.
    ( 1624,   16,    24),    -- Bits overlap.
    (65504,    0, 65504),    -- Lots of bits (all but the low 6 bits)
    (    0, NULL,  NULL)     -- No bits
    ;