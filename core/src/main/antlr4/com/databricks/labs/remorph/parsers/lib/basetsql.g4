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
lexer grammar basetsql;

// TOOD: Replace usage with genericOption(s)
REQUIRED_SYNCHRONIZED_SECONDARIES_TO_COMMIT: 'REQUIRED_SYNCHRONIZED_SECONDARIES_TO_COMMIT';

// Specials for graph nodes
NODEID: '$NODE_ID';

DOLLAR_ACTION: '$ACTION';

// Functions starting with double at signs
AAPSEUDO: '@@' ID;

SPACE:
    [ \t\r\n\u000c\u0085\u00a0\u1680\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200a\u202f\u205f\u3000]+ -> skip
;
COMMENT      : '/*' (COMMENT | .)*? '*/' -> channel(HIDDEN);
LINE_COMMENT : '--' ~[\r\n]*             -> channel(HIDDEN);

// TODO: ID can be not only Latin.
DOUBLE_QUOTE_ID   : '"' ('""' | ~[\r\n"])* '"';
SQUARE_BRACKET_ID : '[' (~']' | ']' ']')* ']';
LOCAL_ID          : '@' ([A-Z_$@#0-9] | FullWidthLetter)*;
TEMP_ID           : '#' ([A-Z_$@#0-9] | FullWidthLetter)*;

ID: ( [A-Z_#] | FullWidthLetter) ( [A-Z_#$@0-9] | FullWidthLetter)*;
STRING options {
    caseInsensitive = false;
}: 'N'? '\'' ('\\' . | '\'\'' | ~['])* '\'';

INT   : DEC_DIGIT+;
HEX   : '0' 'X' HEX_DIGIT*;
FLOAT : DEC_DOT_DEC;
REAL  : (INT | DEC_DOT_DEC) ('E' [+-]? DEC_DIGIT+);
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

// If the lexer choses this rule it has discovered a character that it cannot match
// and this is an error. But lexer errors mean nothing to users, so we pass it up to the
// parser as a token, which will raise a syntx error.
BADCHAR: .;

fragment LETTER      : [A-Z_];
fragment DEC_DOT_DEC : (DEC_DIGIT+ '.' DEC_DIGIT+ | DEC_DIGIT+ '.' | '.' DEC_DIGIT+);
fragment HEX_DIGIT   : [0-9A-F];
fragment DEC_DIGIT   : [0-9];

fragment FullWidthLetter options {
    caseInsensitive = false;
}:
    '\u00c0' ..'\u00d6'
    | '\u00d8' ..'\u00f6'
    | '\u00f8' ..'\u00ff'
    | '\u0100' ..'\u1fff'
    | '\u2c00' ..'\u2fff'
    | '\u3040' ..'\u318f'
    | '\u3300' ..'\u337f'
    | '\u3400' ..'\u3fff'
    | '\u4e00' ..'\u9fff'
    | '\ua000' ..'\ud7ff'
    | '\uf900' ..'\ufaff'
    | '\uff00' ..'\ufff0'
; // | '\u20000'..'\u2FA1F'