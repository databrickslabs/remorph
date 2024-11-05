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
lexer grammar basesnowflake;

tokens {
    STRING_CONTENT
}

// TODO: Revisit these tokens
RETURN_N_ROWS : 'RETURN_' DEC_DIGIT+ '_ROWS';
SKIP_FILE_N   : 'SKIP_FILE_' DEC_DIGIT+;

// TODO: Replace these long options with genericOption as per TSQL - many others in commonlex also.
CLIENT_ENABLE_LOG_INFO_STATEMENT_PARAMETERS   : 'CLIENT_ENABLE_LOG_INFO_STATEMENT_PARAMETERS';
CLIENT_ENCRYPTION_KEY_SIZE                    : 'CLIENT_ENCRYPTION_KEY_SIZE';
CLIENT_MEMORY_LIMIT                           : 'CLIENT_MEMORY_LIMIT';
CLIENT_METADATA_REQUEST_USE_CONNECTION_CTX    : 'CLIENT_METADATA_REQUEST_USE_CONNECTION_CTX';
CLIENT_METADATA_USE_SESSION_DATABASE          : 'CLIENT_METADATA_USE_SESSION_DATABASE';
CLIENT_PREFETCH_THREADS                       : 'CLIENT_PREFETCH_THREADS';
CLIENT_RESULT_CHUNK_SIZE                      : 'CLIENT_RESULT_CHUNK_SIZE';
CLIENT_RESULT_COLUMN_CASE_INSENSITIVE         : 'CLIENT_RESULT_COLUMN_CASE_INSENSITIVE';
CLIENT_SESSION_KEEP_ALIVE                     : 'CLIENT_SESSION_KEEP_ALIVE';
CLIENT_SESSION_KEEP_ALIVE_HEARTBEAT_FREQUENCY : 'CLIENT_SESSION_KEEP_ALIVE_HEARTBEAT_FREQUENCY';
CLIENT_TIMESTAMP_TYPE_MAPPING                 : 'CLIENT_TIMESTAMP_TYPE_MAPPING';
EXTERNAL_OAUTH                                : 'EXTERNAL_OAUTH';
EXTERNAL_OAUTH_ADD_PRIVILEGED_ROLES_TO_BLOCKED_LIST:
    'EXTERNAL_OAUTH_ADD_PRIVILEGED_ROLES_TO_BLOCKED_LIST'
;
EXTERNAL_OAUTH_ALLOWED_ROLES_LIST : 'EXTERNAL_OAUTH_ALLOWED_ROLES_LIST';
EXTERNAL_OAUTH_ANY_ROLE_MODE      : 'EXTERNAL_OAUTH_ANY_ROLE_MODE';
EXTERNAL_OAUTH_AUDIENCE_LIST      : 'EXTERNAL_OAUTH_AUDIENCE_LIST';
EXTERNAL_OAUTH_BLOCKED_ROLES_LIST : 'EXTERNAL_OAUTH_BLOCKED_ROLES_LIST';
EXTERNAL_OAUTH_ISSUER             : 'EXTERNAL_OAUTH_ISSUER';
EXTERNAL_OAUTH_JWS_KEYS_URL       : 'EXTERNAL_OAUTH_JWS_KEYS_URL';
EXTERNAL_OAUTH_RSA_PUBLIC_KEY     : 'EXTERNAL_OAUTH_RSA_PUBLIC_KEY';
EXTERNAL_OAUTH_RSA_PUBLIC_KEY_2   : 'EXTERNAL_OAUTH_RSA_PUBLIC_KEY_2';
EXTERNAL_OAUTH_SCOPE_DELIMITER    : 'EXTERNAL_OAUTH_SCOPE_DELIMITER';
EXTERNAL_OAUTH_SNOWFLAKE_USER_MAPPING_ATTRIBUTE:
    'EXTERNAL_OAUTH_SNOWFLAKE_USER_MAPPING_ATTRIBUTE'
;
EXTERNAL_OAUTH_TOKEN_USER_MAPPING_CLAIM        : 'EXTERNAL_OAUTH_TOKEN_USER_MAPPING_CLAIM';
EXTERNAL_OAUTH_TYPE                            : 'EXTERNAL_OAUTH_TYPE';
EXTERNAL_STAGE                                 : 'EXTERNAL_STAGE';
REQUIRE_STORAGE_INTEGRATION_FOR_STAGE_CREATION : 'REQUIRE_STORAGE_INTEGRATION_FOR_STAGE_CREATION';
REQUIRE_STORAGE_INTEGRATION_FOR_STAGE_OPERATION:
    'REQUIRE_STORAGE_INTEGRATION_FOR_STAGE_OPERATION'
;

DUMMY:
    'DUMMY'
; //Dummy is not a keyword but rules reference it in unfinished grammar - need to get rid

fragment SPACE:
    [ \t\r\n\u000c\u0085\u00a0\u1680\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200a\u202f\u205f\u3000]+
;

WS: SPACE -> channel(HIDDEN);

SQL_COMMENT    : '/*' (SQL_COMMENT | .)*? '*/' -> channel(HIDDEN);
LINE_COMMENT   : '--' ~[\r\n]*                 -> channel(HIDDEN);
LINE_COMMENT_2 : '//' ~[\r\n]*                 -> channel(HIDDEN);

// TODO: ID can be not only Latin.
DOUBLE_QUOTE_ID    : '"' ('""' | ~[\r\n"])* '"';
DOUBLE_QUOTE_BLANK : '""';

ID       : [A-Z_] [A-Z0-9_@$]*;
LOCAL_ID : DOLLAR [A-Z_] [A-Z0-9_]*;

INT   : DEC_DIGIT+;
FLOAT : DEC_DOT_DEC;
REAL  : (INT | DEC_DOT_DEC) 'E' [+-]? DEC_DIGIT+;

fragment HexDigit  : [0-9a-f];
fragment HexString : [A-Z0-9|.] [A-Z0-9+\-|.]*;

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

fragment DEC_DOT_DEC : DEC_DIGIT+ DOT DEC_DIGIT+ | DEC_DIGIT+ DOT | DOT DEC_DIGIT+;
fragment DEC_DIGIT   : [0-9];

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

STRING_START: '\'' -> pushMode(stringMode);

// This lexer rule is needed so that any unknown character in the lexicon does not
// cause an incomprehensible error message from teh lexer. This rule will allow the parser to issue
// something more meaningful and perform error recovery as the lexer CANNOT raise an error - it
// will alwys match at least one character using this catch-all rule.
//
// !IMPORTANT! - Always leave this as the last lexer rule, before the mode definitions
BADCHAR: .;

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