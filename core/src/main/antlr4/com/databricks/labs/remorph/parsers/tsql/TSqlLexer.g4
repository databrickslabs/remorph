/*
T-SQL (Transact-SQL, MSSQL) grammar.
The MIT License (MIT).
Copyright (c) 2017, Mark Adams (madams51703@gmail.com)
Copyright (c) 2015-2017, Ivan Kochurkin (kvanttt@gmail.com), Positive Technologies.
Copyright (c) 2016, Scott Ure (scott@redstormsoftware.com).
Copyright (c) 2016, Rui Zhang (ruizhang.ccs@gmail.com).
Copyright (c) 2016, Marcus Henriksson (kuseman80@gmail.com).
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
*/

// =================================================================================
// Please reformat the grammr file before a change commit. See remorph/core/README.md
// For formatting, see: https://github.com/mike-lischke/antlr-format/blob/main/doc/formatting.md

// $antlr-format alignTrailingComments true
// $antlr-format columnLimit 150
// $antlr-format maxEmptyLinesToKeep 1
// $antlr-format reflowComments false
// $antlr-format useTab false
// $antlr-format allowShortRulesOnASingleLine true
// $antlr-format allowShortBlocksOnASingleLine true
// $antlr-format minEmptyLines 0
// $antlr-format alignSemicolons ownLine
// $antlr-format alignColons trailing
// $antlr-format singleLineOverrulesHangingColon true
// $antlr-format alignLexerCommands true
// $antlr-format alignLabels true
// $antlr-format alignTrailers true
// =================================================================================
lexer grammar TSqlLexer;

import commonlex;

options {
    caseInsensitive = true;
}

@members {
    private static int TSQL_DIALECT = 1;
    private static int SNOWFLAKE_DIALECT = 2;
    private static int dialect = SNOWFLAKE_DIALECT;
}

// Specials for graph nodes
NODEID: '$NODE_ID';

DOLLAR_ACTION: '$ACTION';

// Functions starting with double at signs
AAPSEUDO: '@@' ID;

STRING options {
    caseInsensitive = false;
}: 'N'? '\'' ('\\' . | '\'\'' | ~['])* '\'';

HEX   : '0X' HexDigit*;
INT   : [0-9]+;
FLOAT : DEC_DOT_DEC;
REAL  : (INT | DEC_DOT_DEC) ('E' [+-]? [0-9]+);
MONEY : '$' (INT | FLOAT);

EQ         : '=';
GT         : '>';
LT         : '<';
BANG       : '!';
PE         : '+=';
ME         : '-=';
SE         : '*=';
DE         : '/=';
MEA        : '%=';
AND_ASSIGN : '&=';
XOR_ASSIGN : '^=';
OR_ASSIGN  : '|=';

DOUBLE_BAR   : '||';
DOT          : '.';
AT           : '@';
DOLLAR       : '$';
LPAREN       : '(';
RPAREN       : ')';
COMMA        : ',';
SEMI         : ';';
COLON        : ':';
DOUBLE_COLON : '::';
STAR         : '*';
DIV          : '/';
MOD          : '%';
PLUS         : '+';
MINUS        : '-';
BIT_NOT      : '~';
BIT_OR       : '|';
BIT_AND      : '&';
BIT_XOR      : '^';

PLACEHOLDER: '?';

// TSQL specific
SQUARE_BRACKET_ID : '[' (~']' | ']' ']')* ']';
TEMP_ID           : '#' ([A-Z_$@#0-9] | FullWidthLetter)*;
LOCAL_ID          : '@' ([A-Z_$@#0-9] | FullWidthLetter)*;