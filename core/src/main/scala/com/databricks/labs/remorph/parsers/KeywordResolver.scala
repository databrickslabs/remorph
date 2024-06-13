package com.databricks.labs.remorph.parsers

// TODO: Valentin some dialects will be loaded via external jars - sealed traits could be an issue?
sealed trait KeywordType
case object Reserved extends KeywordType
case object NonReserved extends KeywordType

sealed trait KeywordClass
case object OptionKeyword extends KeywordClass
case object FunctionKeyword extends KeywordClass
case object XMLOption extends KeywordClass
// etc...

sealed trait OptionType

/**
 * An option that is ON if present
 */
case object BooleanOption extends OptionType

/**
 * An option that requires some value to be present. Note that the value will be accepted from an expression. The actual
 * value could be checked to see that it yields the correct type, but in this transpiler we assume valid input in the
 * first place.
 */
case object ExpressionOption extends OptionType

/**
 * The type of the value that the option takes. This is useful for validation and transformation.
 */
sealed trait OptionValueType

/**
 * The option takes a string value only
 */
case object StringOption extends OptionValueType

/**
 * An option that takes an integer value only
 */
case object IntegerOption extends OptionValueType
// etc ...

// TODO: Maybe the use of Option is not the best choice here, as it is a Scala type and could be confusing?

case class Keyword(
    keywordType: KeywordType, // Whether the keyword is reserved or non-reserved (can be useful for transformation)
    keywordClass: KeywordClass, // The class of the keyword (e.g. OPTION, XMLOPTION and so on )
    optionType: OptionType, // The type of the option if the keyword is an option
    optionValueType: OptionValueType // The type of the value that the option takes
) {}

/**
 * <p> This class is used to resolve keywords in the SQL dialects. Keywords that are merely options specifications are
 * not tracked in the lexer and parser as it just involves a lot of clutter and creates huge NFAs and DFAs for no good
 * reason. <p> This type of resolution is useful for the following:
 *   - validation of option names and values
 *   - error reporting - e.g. "OPTION 'foo' is not valid here", "'foo' is not a valid value for 'bar'"
 * <p> NOTE: This implementation is just a place holder so we do not lose track of the myriad keywords in the dialects
 * but the actual implementation is TBD.
 */
abstract class KeywordResolver {

  protected val commonKeywordsPf: PartialFunction[String, Keyword] = {
    case "TIME" => Keyword(NonReserved, OptionKeyword, ExpressionOption, IntegerOption)
    case "DELAY" => Keyword(NonReserved, OptionKeyword, ExpressionOption, IntegerOption)
    case "TIMEOUT" => Keyword(NonReserved, OptionKeyword, ExpressionOption, IntegerOption)

    // etc...
  }

  def resolveKeyword(keyword: String): Option[Keyword] = {
    commonKeywordsPf.lift(keyword.toUpperCase())
  }
}
