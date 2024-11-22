// =================================================================================
// Please reformat the grammr file before a change commit. See remorph/core/README.md
// For formatting, see: https://github.com/mike-lischke/antlr-format/blob/main/doc/formatting.md

// $antlr-format alignColons hanging
// $antlr-format columnLimit 150
// $antlr-format alignSemicolons hanging
// $antlr-format alignTrailingComments true
// =================================================================================

lexer grammar DBTPreprocessorLexer;

tokens {
    STRING
}

options {
    caseInsensitive = true;
}

@members {
    /**
    * Defines the configuration for the preprocessor, such as Jinja templating delimiters and
    * any DBT parameters that are relevant to us.
    */
    public class Config {
        private String exprStart;
        private String exprEnd;
        private String statStart;
        private String statEnd;
        private String commentStart;
        private String commentEnd;
        private String lineStatStart;

        // Standard defaults for Jinja templating
        public Config() {
            this("{{", "}}", "{%", "%}", "{#", "#}", "#");
        }

        public Config(String exprStart, String exprEnd, String statStart, String statEnd, String commentStart, String commentEnd, String lineStatStart) {
            this.exprStart = exprStart;
            this.exprEnd = exprEnd;
            this.statStart = statStart;
            this.statEnd = statEnd;
            this.commentStart = commentStart;
            this.commentEnd = commentEnd;
            this.lineStatStart = lineStatStart;
        }

        // Getters
        public String exprStart() {
            return exprStart;
        }

        public String exprEnd() {
            return exprEnd;
        }

        public String statStart() {
            return statStart;
        }

        public String statEnd() {
            return statEnd;
        }

        public String commentStart() {
            return commentStart;
        }

        public String commentEnd() {
            return commentEnd;
        }

        public String lineStatStart() {
            return lineStatStart;
        }
    }

    public Config config = new Config();

    /**
     * Our template lexer rules only consume a single character, even when the sequence is longer than
     * one character. So we we need to advance the input past the matched sequence.
     */
    private void scanPast(String str) {
        int index = _input.index();

        // If there was a preceding hyphen such as -%}, we need to move past that as well
        if (_input.LA(-1) == '-') {
            index++;
        }
        _input.seek(index + str.length() - 1);

        // If there is a trailing hyphen suchas {%- then we need to scan past that as well
        if (_input.LA(1) == '-') {
            _input.consume();
        }
    }

    /**
     * Called when a single character is matched to see if it and the next sequence of characters
     * match the current configured chracters that start a Ninja statement templage
     */
    private boolean matchAndConsume(String str) {
        // Check if the first character matches otherwise we would accidentally accept anything for
        // a single character marker such as LineStatStart
        if (str.charAt(0) != _input.LA(-1)) {
            return false;
        }
        for (int i = 1; i < str.length(); i++) {
            if (str.charAt(i) != _input.LA(1)) {
                return false;
            }
            // Move to next character
            _input.consume();
        }

        // All characters matched, return true
        return true;
    }

    private boolean isStatement() {
        if( matchAndConsume(config.statStart())) {
            // There may be a trailing hyphen that is part of the statement start
            if (_input.LA(1) == '-') {
                _input.consume();
            }
            return true;
        }
        return false;
    }

    private boolean isExpression() {
        if (matchAndConsume(config.exprStart())) {
           // There may be a trailing hyphen that is part of the expression start
            if (_input.LA(1) == '-') {
                _input.consume();
            }
            return true;
        }
        return false;
    }

    private boolean isComment() {
        return matchAndConsume(config.commentStart());
    }

    // Note that this is not qute correct yet as we must check that this is the
    // the first non-whitespace character on the line as well.
    private boolean isLineStat() {
        return matchAndConsume(config.lineStatStart());
    }

    private boolean isStatementEnd() {
        // There may be a preceding hyphen that is part of the statement end
        int index = _input.index();
        if (_input.LA(-1) == '-') {
            _input.consume();
        }
        if (matchAndConsume(config.statEnd())) {
            return true;
        }
        // Return to the start of the statement, any hyphen wwas just that and
        // not part of the token
        _input.seek(index);
        return false;
    }

    private boolean isExpresionEnd() {
        // There may be a preceding hyphen that is part of the expression end
        int index = _input.index();
        if (_input.LA(-1) == '-') {
            _input.consume();
        }
        if (matchAndConsume(config.exprEnd())) {
            return true;
        }
        // Return to the start of the expression, any hyphen wwas just that and
        // not part of the token
        _input.seek(index);
        return false;
    }

    private boolean isCommentEnd() {
        return matchAndConsume(config.commentEnd());
    }
}

STATEMENT: . { scanPast(config.statStart); } { isStatement() }? -> pushMode(statementMode )
    ;
EXPRESSION: . { scanPast(config.exprStart); } { isExpression() }? -> pushMode(expressionMode )
    ;
COMMENT: . { scanPast(config.commentStart); } { isComment() }? -> pushMode(commentMode )
    ;
LINESTAT: . { scanPast(config.lineStatStart); } { isLineStat() }? -> pushMode(lineStatMode )
    ;

// We track whitespace as it can influence how a template following or not following
// whitespace is replaced in the processed output. Similarly, we want to know if whitespace
// followed the template reference or not
WS: [ \t]+
    ;

C: .
    ;

mode statementMode;

STATEMENT_STRING: '\'' ('\\' . | ~["\n])* '\'' -> type(STRING)
    ;
STATEMENT_END: . { scanPast(config.statEnd); } { isStatementEnd() }? -> popMode
    ;
STATMENT_BIT: . -> type(C)
    ;

mode expressionMode;

EXPRESSION_STRING: '\'' ('\\' . | ~['\n])* '\'' -> type(STRING)
    ;
EXPRESSION_END: . { scanPast(config.exprEnd); } { isExpresionEnd() }? -> popMode
    ;
EXPRESSION_BIT: . -> type(C)
    ;

mode commentMode;
COMMENT_STRING: '\'' ('\\' . | ~['\n])* '\'' -> type(STRING)
    ;
COMMENT_END: . { scanPast(config.commentEnd); } { isCommentEnd() }? -> popMode
    ;
COMMENT_BIT: . -> type(C)
    ;

mode lineStatMode;
LINESTAT_STRING: '\'' ('\\' . | ~['\n])* '\'' -> type(STRING)
    ;
LINESTAT_END: '\r'? '\n' -> popMode
    ;
LINESTAT_BIT: . -> type(C)
    ;