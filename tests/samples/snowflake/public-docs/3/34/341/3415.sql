-- Uses the 'fr' collation because the precedence for col2_fr is higher than
-- the precendence for col1.
... WHERE col1 = col2_fr ...

-- Uses the 'en' collation, because it is explicitly specified in the statement,
-- which takes precedence over the collation for col2_fr.
... WHERE col1 COLLATE 'en' = col2_fr ...

-- Returns an error because the expressions have different collations at the same
-- precedence level.
... WHERE col2_fr = col3_de ...

-- Uses the 'de' collation because collation for col2_fr has been removed.
... WHERE col2_fr COLLATE '' = col3_de ...

-- Returns an error because the expressions have different collations at the same
-- precedence level.
... WHERE col2_fr COLLATE 'en' = col3_de COLLATE 'de' ...