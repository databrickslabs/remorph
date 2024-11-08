// =================================================================================
// Please reformat the grammr file before a change commit. See remorph/core/README.md
// For formatting, see: https://github.com/mike-lischke/antlr-format/blob/main/doc/formatting.md

// $antlr-format alignColons hanging
// $antlr-format columnLimit 150
// $antlr-format alignSemicolons hanging
// $antlr-format alignTrailingComments true
// =================================================================================

lexer grammar Preprocessor;

tokens {
   STRING,
   CHAR
}

options {
    caseInsensitive = true;
}

@members {
    /**
    * Defines the configuration for the preprocessor, such as Jinga templating delimiters and
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

        // Standard defaults for Jinga templating
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
     * Called when a single character is matched to see if it and the next sequence of characters
     * match the current configured chracters that start a Ninja statement templage
     */
    private boolean matchAndConsume(String str) {
        int m = _input.mark();
        try {

            int index = _input.index();
            for (int i = 1; i < str.length(); i++) {
                if (str.charAt(i) != _input.LA(1)) {
                    _input.seek(index);
                    return false;
                }
                // Move to next character
                _input.consume();
            }

            // All characters matched, return true
            return true;

        } finally {
            _input.release(m);
        }
    }

    private boolean isStatement() {
        return matchAndConsume(config.statStart());
    }

    private boolean isExpression() {
        return matchAndConsume(config.exprStart());
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
        return matchAndConsume(config.statEnd());
    }

    private boolean isExpresionEnd() {
        return matchAndConsume(config.exprEnd());
    }

    private boolean isCommentEnd() {
        return matchAndConsume(config.commentEnd());
    }
}

STATEMENT: .  { isStatement() }? -> pushMode(statementMode );
EXPRESSION: . { isExpression() }? -> pushMode(expressionMode );
COMMENT: .    { isComment() }? -> pushMode(commentMode );
LINESTAT: .  { isLineStat() }? -> pushMode(lineStatMode );

C: .;

mode statementMode;

STATEMENT_STRING: '"' ('\\' . | ~["\n])* '"' -> type(STRING);
STATEMENT_END: . { isStatementEnd() }? -> popMode;
STATMENT_BIT: . -> type(CHAR);

mode expressionMode;

EXPRESSION_STRING: '"' ('\\' . | ~["\n])* '"' -> type(STRING);
EXPRESSION_END: . { isExpresionEnd() }? -> popMode;
EXPRESSION_BIT: . -> type(CHAR);

mode commentMode;
COMMENT_STRING: '"' ('\\' . | ~["\n])* '"' -> type(STRING);
COMMENT_END: . { isCommentEnd() }? -> popMode;
COMMENT_BIT: . -> type(CHAR);

mode lineStatMode;
LINESTAT_STRING: '"' ('\\' . | ~["\n])* '"' -> type(STRING);
LINESTAT_END: ( '\r\n' | '\n') -> popMode;
LINESTAT_BIT: . -> type(CHAR);
