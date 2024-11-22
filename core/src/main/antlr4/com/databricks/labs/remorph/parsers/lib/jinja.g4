// =================================================================================
// Please reformat the grammr file before a change commit. See remorph/core/README.md
// For formatting, see: https://github.com/mike-lischke/antlr-format/blob/main/doc/formatting.md

// $antlr-format alignColons hanging
// $antlr-format columnLimit 150
// $antlr-format alignSemicolons hanging
// $antlr-format alignTrailingComments true
// =================================================================================

parser grammar jinja;

// Jinja template elements can occur anywhere in the text and so this rule can be used strategically to allow
// what otherwise would be a syntax error to be parsed as a Jinja template. As it is essentially one
// token, ANTLR alts will predict easilly. For isntance on lists of expressions, we need to allow
// JINJA templates without separating COMMAs etc.
jinjaTemplate: JINJA_REF+
    ;