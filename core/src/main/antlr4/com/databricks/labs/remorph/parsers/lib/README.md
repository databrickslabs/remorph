# ANTLR Grammar Library

This directory contains ANTLR grammar files that are common to more than one SQL dialect. Such as the grammar that covers stored procedures, which all
dialects of SQL support in some form, and for which we have a universal grammar.

ANTLR processes included grammars as pure text, in the same way that say the C pre-processor processes `#include` directives. 
This means that you must be careful to ensure that:
 - if you define new tokens in an included grammar, that they do not clash with tokens in the including grammar.
 - if you define new rules in an included grammar, that they do not clash with rules in the including grammar.
   In particular, you must avoid creating ambiguities in rule/token prediction, where ANTLR will try to create
   a parser anyway, but generate code that performs extremely long token lookahead, and is therefore very slow.

In other words, you cannot just arbitrarily throw together some common Lexer and Parser rules and expect them
to just work.
