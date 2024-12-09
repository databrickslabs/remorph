/*
Snowflake Database grammar.
The MIT License (MIT).

Copyright (c) 2022, Michał Lorek.

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
lexer grammar SnowflakeLexer;

import commonlex;

tokens {
    STRING_CONTENT
}

options {
    caseInsensitive = true;
}

@members {
    private static int TSQL_DIALECT = 1;
    private static int SNOWFLAKE_DIALECT = 2;
    private static int dialect = SNOWFLAKE_DIALECT;
}

INT   : [0-9]+;
FLOAT : DEC_DOT_DEC;
REAL  : (INT | DEC_DOT_DEC) 'E' [+-]? [0-9]+;

BANG  : '!';
ARROW : '->';
ASSOC : '=>';

NE   : '!=';
LTGT : '<>';
EQ   : '=';
GT   : '>';
GE   : '>=';
LT   : '<';
LE   : '<=';

PIPE_PIPE   : '||';
DOT         : '.';
AT          : '@';
DOLLAR      : '$';
LPAREN      : '(';
RPAREN      : ')';
LSB         : '[';
RSB         : ']';
LCB         : '{';
RCB         : '}';
COMMA       : ',';
SEMI        : ';';
COLON       : ':';
COLON_COLON : '::';
STAR        : '*';
DIVIDE      : '/';
MODULE      : '%';
PLUS        : '+';
MINUS       : '-';
TILDA       : '~';
AMP         : '&';

// A question mark can be used as a placeholder for a prepared statement that will use binding.
PARAM: '?';

SQLCOMMAND:
    '!' SPACE? (
        'abort'
        | 'connect'
        | 'define'
        | 'edit'
        | 'exit'
        | 'help'
        | 'options'
        | 'pause'
        | 'print'
        | 'queries'
        | 'quit'
        | 'rehash'
        | 'result'
        | 'set'
        | 'source'
        | 'spool'
        | 'system'
        | 'variables'
    ) ~[\r\n]*
;

// Parameters
LOCAL_ID: DOLLAR ID;

STRING_START: '\'' -> pushMode(stringMode);

// ================================================================================================
// LEXICAL MODES
//
// Lexical modes are used to allow the lexer to return different token types than the main lexer
// and are triggered by a main lexer rule matching a specific token. The mode is ended by matching
// a specific lexical sequence in the input stream. Note that this is a lexical trigger only and is
// not influenced by the parser state as the paresr does NOT direct the lexer:
//
// 1) The lexer runs against the entire input sequence and returns tokens to the parser.
// 2) THEN the parser uses the tokens to build the parse tree - it cannot therefore influence the
//    lexer in any way.

// In string mode we are separating out normal string literals from defined variable
// references, so that they can be translated from Snowflakey syntax to Databricks SQL syntax.
// This mode is trigered when we hit a single quote in the lexer and ends when we hit the
// terminating single quote minus the usual escape character processing.
mode stringMode;

// An element that is a variable reference can be &{variable} or just &variable. They are
// separated out in case there is any difference needed in translation/generation. A single
// & is placed in a string by using &&.

// We exit the stringMode when we see the terminating single quote.
//
STRING_END: '\'' -> popMode;

STRING_AMP    : '&' -> type(STRING_CONTENT);
STRING_AMPAMP : '&&';

// Note that snowflake also allows $var, and :var
// if they are allowed in literal strings// then they can be added here.
//
VAR_SIMPLE  : '&' [A-Z_] [A-Z0-9_]*;
VAR_COMPLEX : '&{' [A-Z_] [A-Z0-9_]* '}';

// TODO: Do we also need \xHH hex and \999 octal escapes?
STRING_UNICODE : '\\' 'u' HexDigit HexDigit HexDigit HexDigit;
STRING_ESCAPE  : '\\' .;
STRING_SQUOTE  : '\'\'';

// Anything that is not a variable reference is just a normal piece of text.
STRING_BIT: ~['\\&]+ -> type(STRING_CONTENT);