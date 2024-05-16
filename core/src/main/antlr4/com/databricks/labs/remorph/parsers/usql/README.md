# TSQL Replacement Grammar

The grammar we are currently using for TSQL is in poor shape. It is not complete and does parses
many things incorrectly. This grammar and lexer, along with their associated includes are complete for
TSQL 2008R2 (tested exhaustively).

At worst, we can just replace the TSQL grammar with the USQL grammar, and tweak the existing visitors to
accommodate the small changes in rule names. However, in an ideal world, we can add to this grammar such
that it supports Snowflake, and other variants of SQL. 

It may be possible to have a universal visitor, though this is not a requirement.
