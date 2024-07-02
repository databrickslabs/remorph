package com.databricks.labs.remorph.generators.sqlgen

import com.databricks.labs.remorph.generators.GeneratorContext
import com.databricks.labs.remorph.parsers.intermediate.{BinaryOperator, Expression}

import scala.util.matching.Regex

object SqlExpressions {
  private[df2sql] def exprsSql(ctx: GeneratorContext, exprs: Seq[Expression]): String =
    smartDelimiters(ctx, exprs.map(x => exprSql(ctx, x)))

  // TODO: make private
  def smartDelimiters(ctx: GeneratorContext, seq: Seq[String]): String = {
    val default = seq.mkString(", ")
    if (default.length < ctx.maxLineWidth) default else seq.mkString(s",\n${ctx.ws}")
  }

  private def withParenthesesIfBinary(ctx: GeneratorContext, expr: Expression): String =
    expr match {
      case b: BinaryOperator =>
        s"(${binaryOperatorCode(ctx, b)})"
      case _ =>
        exprSql(ctx, expr)
    }

  private def binaryOperatorCode(ctx: GeneratorContext, b: BinaryOperator): String = {
    val symbol = b.sqlOperator
    val left = withParenthesesIfBinary(ctx, b.left)
    val oneLine = s"$left $symbol ${withParenthesesIfBinary(ctx.withRawLiteral, b.right)}"
    if (oneLine.length < ctx.maxLineWidth) {
      oneLine
    } else {
      val nest = ctx.nest
      val right = withParenthesesIfBinary(nest, b.right)
      s"$left $symbol\n${nest.ws}$right"
    }
  }

  private def caseWhenSql(ctx: GeneratorContext,
                          branches: Seq[(Expression, Expression)],
                          elseValue: Option[Expression]): String = {
    val subContext = ctx.nest
    "CASE" + branches.map(whenThenSql(subContext)).mkString + (if (elseValue.isDefined) {
      s"\n${subContext.ws}ELSE ${exprSql(subContext, elseValue.get)}"
    } else "") + s"\n${ctx.ws}END" // END should get the whitespace of parent context
  }

  private def whenThenSql(ctx: GeneratorContext
                         ): PartialFunction[(Expression, Expression), String] = {
    case (left, right) =>
      val leftSql = exprSql(ctx, left)
      val rightSql = exprSql(ctx, right)
      val oneline = s"\n${ctx.ws}WHEN $leftSql THEN $rightSql"
      if (oneline.length < ctx.maxLineWidth) {
        oneline
      } else {
        // do some reformatting because of maximum line width
        val nest = ctx.nest
        s"\n${ctx.ws}WHEN $leftSql\n${nest.ws}THEN ${exprSql(nest, right)})"
      }
  }

  private val pattern: Regex = "((?<![\\\\])['\"`])".r

  /** Sugar for quoting strings */
  private def q(value: String) =
    if (pattern.findAllIn(value).toList.isEmpty) value
    else catalyst.util.quoteIdentifier(value)

  private[df2sql] def exprSql(ctx: GeneratorContext, expr: Expression): String = expr match {
    case b: BinaryOperator =>
      binaryOperatorCode(ctx, b)
    case CaseWhen(branches, elseValue) =>
      caseWhenSql(ctx, branches, elseValue)
    case Like(left, right, escapeChar) => escapeChar match {
      case '\\' => s"${exprSql(ctx, left)} LIKE ${exprSql(ctx, right)}"
      case c => s"${exprSql(ctx, left)} LIKE ${exprSql(ctx, right)} ESCAPE '$c'"
    }
    case ref: AttributeReference =>
      if (ref.qualifier.nonEmpty && ctx.hasJoins) {
        s"${ref.qualifier.mkString(".")}.${q(ref.name)}"
      } else q(ref.name)
    case Alias(child, name) =>
      s"${exprSql(ctx, child)} AS $name"
    case GetArrayItem(child, Literal(idx, _ @ IntegerType), _) => s"${exprSql(ctx, child)}[$idx]"
    case GetMapValue(child, key, _) => s"${exprSql(ctx, child)}[${exprSql(ctx, key)}]"

    case Abs(left) => s"ABS(${exprSql(ctx, left)})"
    case Acos(left) => s"ACOS(${exprSql(ctx, left)})"
    case Acosh(left) => s"ACOSH(${exprSql(ctx, left)})"
    case ArrayAggregate(left, right, c, d) => s"AGGREGATE(${exprSql(ctx, left)}, " +
      s"${exprSql(ctx, right)}, ${exprSql(ctx, c)}, ${exprSql(ctx, d)})"
    case CreateArray(left, _) => s"ARRAY(${exprsSql(ctx, left)})"

    // array_sort(expr, func) - Sorts the input array. If func is omitted, sort
    case ArraySort(left, right) => s"ARRAY_SORT(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"

    case Ascii(left) => s"ASCII(${exprSql(ctx, left)})"
    case Asin(left) => s"ASIN(${exprSql(ctx, left)})"
    case Asinh(left) => s"ASINH(${exprSql(ctx, left)})"
    case Atan(left) => s"ATAN(${exprSql(ctx, left)})"
    case Atan2(left, right) => s"ATAN2(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"
    case Atanh(left) => s"ATANH(${exprSql(ctx, left)})"
    case Base64(left) => s"BASE64(${exprSql(ctx, left)})"
    case Bin(left) => s"BIN(${exprSql(ctx, left)})"
    case BitwiseCount(left) => s"BIT_COUNT(${exprSql(ctx, left)})"
    case BitLength(left) => s"BIT_LENGTH(${exprSql(ctx, left)})"
    case BRound(left, right) => s"BROUND(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"

    case Cast(left, right, None) => s"CAST(${exprSql(ctx, left)}, $right)"
    case Cbrt(left) => s"CBRT(${exprSql(ctx, left)})"
    case Ceil(left) => s"CEIL(${exprSql(ctx, left)})"
    case Chr(left) => s"CHAR(${exprSql(ctx, left)})"
    case Length(left) => s"CHAR_LENGTH(${exprSql(ctx, left)})"
    case Coalesce(left) => s"COALESCE(${exprsSql(ctx, left)})"

    // concat_ws(sep[, str | array(str)]+) - Returns the concatenation of
    // the strings separated by `sep`.
    case ConcatWs(left) => s"CONCAT_WS(${exprsSql(ctx, left)})"
    case Conv(left, right, c) => s"CONV(${exprSql(ctx, left)}, " +
      s"${exprSql(ctx, right)}, ${exprSql(ctx, c)})"
    case Cos(left) => s"COS(${exprSql(ctx, left)})"
    case Cosh(left) => s"COSH(${exprSql(ctx, left)})"
    case Cot(left) => s"COT(${exprSql(ctx, left)})"
    case Crc32(left) => s"CRC32(${exprSql(ctx, left)})"
    case Cube(left) => s"CUBE(${exprsSql(ctx, left)})"
    case DayOfMonth(left) => s"DAY(${exprSql(ctx, left)})"
    case Decode(left, right) => s"DECODE(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"
    case ToDegrees(left) => s"DEGREES(${exprSql(ctx, left)})"
    case ElementAt(left, right, _) => s"ELEMENT_AT(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"
    case Elt(left, right) => s"ELT(${exprsSql(ctx, left)}, $right)"
    case Encode(left, right) => s"ENCODE(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"
    case ArrayExists(left, right, _) => s"EXISTS(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"
    case Exp(left) => s"EXP(${exprSql(ctx, left)})"
    case Explode(left) => s"EXPLODE(${exprSql(ctx, left)})"

    // expm1(expr) - Returns exp(`expr`) - 1.
    case Expm1(left) => s"EXPM1(${exprSql(ctx, left)})"

    // extract(field FROM source) - Extracts a part of the date/timestamp or interval source.
    case Extract(left, right, child) => s"EXTRACT(${exprSql(ctx, left)}, " +
      s"${exprSql(ctx, right)}, ${exprSql(ctx, child)})"

    // factorial(expr) - Returns the factorial of `expr`. `expr` is [0..20]. Otherwise, null.
    case Factorial(left) => s"FACTORIAL(${exprSql(ctx, left)})"

    // filter(expr, func) - Filters the input array using the given predicate.
    case ArrayFilter(left, right) => s"FILTER(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"

    case FindInSet(left, right) => s"FIND_IN_SET(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"

    // floor(expr) - Returns the largest integer not greater than `expr`.
    case Floor(left) => s"FLOOR(${exprSql(ctx, left)})"

    // forall(expr, pred) - Tests whether a predicate holds for all elements in the array.
    case ArrayForAll(left, right) => s"FORALL(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"

    case FormatNumber(left, right) =>
      s"FORMAT_NUMBER(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"

    // greatest(expr, ...) - Returns the greatest value of all parameters, skipping null values.
    case Greatest(left) => s"GREATEST(${exprsSql(ctx, left)})"

    case Grouping(left) => s"GROUPING(${exprSql(ctx, left)})"

    case GroupingID(left) => s"GROUPING_ID(${exprsSql(ctx, left)})"

    // hash(expr1, expr2, ...) - Returns a hash value of the arguments.
    case Murmur3Hash(left, right) => s"HASH(${exprsSql(ctx, left)}, $right)"

    // hex(expr) - Converts `expr` to hexadecimal.
    case Hex(left) => s"HEX(${exprSql(ctx, left)})"

    // hypot(expr1, expr2) - Returns sqrt(`expr1`**2 + `expr2`**2).
    case Hypot(left, right) => s"HYPOT(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"

    // ifnull(expr1, expr2) - Returns `expr2` if `expr1` is null, or `expr1` otherwise.
    case IfNull(left, right, _) => s"IFNULL(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"

    // if(expr1, expr2, expr3) - If `expr1` evaluates to true,
    // then returns `expr2`; otherwise returns `expr3`.
    case If(left, right, c) =>
      s"IF(${exprSql(ctx, left)}, ${exprSql(ctx, right)}, ${exprSql(ctx, c)})"

    // expr1 in(expr2, expr3, ...) - Returns true if `expr` equals to any valN.
    case In(left, right) if right.size > 1 => s"IN(${exprSql(ctx, left)}, ${exprsSql(ctx, right)})"

    case In(left, right) if right.isEmpty => s"IN(${exprSql(ctx, left)})"

    case InitCap(left) => s"INITCAP(${exprSql(ctx, left)})"

    // inline(expr) - Explodes an array of structs into a table. Uses column names
    // col1, col2, etc. by default unless specified otherwise.
    case Inline(left) => s"INLINE(${exprSql(ctx, left)})"

    // instr(str, substr) - Returns the (1-based) index of the first
    // occurrence of `substr` in `str`.
    case StringInstr(left, right) => s"INSTR(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"

    // isnan(expr) - Returns true if `expr` is NaN, or false otherwise.
    case IsNaN(left) => s"ISNAN(${exprSql(ctx, left)})"

    // isnotnull(expr) - Returns true if `expr` is not null, or false otherwise.
    case IsNotNull(left) => s"ISNOTNULL(${exprSql(ctx, left)})"

    // isnull(expr) - Returns true if `expr` is null, or false otherwise.
    case IsNull(left) => s"ISNULL(${exprSql(ctx, left)})"

    // java_method(class, method[, arg1[, arg2 ..]]) - Calls a method with reflection.
    case CallMethodViaReflection(left) => s"JAVA_METHOD(${exprsSql(ctx, left)})"

    // least(expr, ...) - Returns the least value of all parameters, skipping null values.
    case Least(left) => s"LEAST(${exprsSql(ctx, left)})"

    // levenshtein(str1, str2) - Returns the Levenshtein distance between the two given strings.
    case Levenshtein(left, right) => s"LEVENSHTEIN(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"

    // ln(expr) - Returns the natural logarithm (base e) of `expr`.
    case Log(left) => s"LN(${exprSql(ctx, left)})"

    case StringLocate(left, right, c) =>
      s"LOCATE(${exprSql(ctx, left)}, ${exprSql(ctx, right)}, ${exprSql(ctx, c)})"

    // log(base, expr) - Returns the logarithm of `expr` with `base`.
    case Logarithm(left, right) => s"LOG(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"

    // log10(expr) - Returns the logarithm of `expr` with base 10.
    case Log10(left) => s"LOG10(${exprSql(ctx, left)})"

    // log1p(expr) - Returns log(1 + `expr`).
    case Log1p(left) => s"LOG1P(${exprSql(ctx, left)})"

    // log2(expr) - Returns the logarithm of `expr` with base 2.
    case Log2(left) => s"LOG2(${exprSql(ctx, left)})"

    // lower(str) - Returns `str` with all characters changed to lowercase.
    case Lower(left) => s"LOWER(${exprSql(ctx, left)})"

    case StringLPad(left, right, c) =>
      s"LPAD(${exprSql(ctx, left)}, ${exprSql(ctx, right)}, ${exprSql(ctx, c)})"

    case StringTrimLeft(left, right) => s"LTRIM(${exprSql(ctx, left)}, $right)"

    // map(key0, value0, key1, value1, ...) - Creates a map with the given key/value pairs.
    case CreateMap(left, _) => s"MAP(${exprsSql(ctx, left)})"

    // map_filter(expr, func) - Filters entries in a map using the function.
    case MapFilter(left, right) => s"MAP_FILTER(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"

    case MapFromArrays(left, right) =>
      s"MAP_FROM_ARRAYS(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"

    case MapZipWith(left, right, c) =>
      s"MAP_ZIP_WITH(${exprSql(ctx, left)}, ${exprSql(ctx, right)}, ${exprSql(ctx, c)})"

    // md5(expr) - Returns an MD5 128-bit checksum as a hex string of `expr`.
    case Md5(left) => s"MD5(${exprSql(ctx, left)})"

    case MonotonicallyIncreasingID() => s"MONOTONICALLY_INCREASING_ID()"

    // named_struct(name1, val1, name2, val2, ...) - Creates a struct with the given
    // field names and values.
    case CreateNamedStruct(left) => s"NAMED_STRUCT(${exprsSql(ctx, left)})"

    // nanvl(expr1, expr2) - Returns `expr1` if it's not NaN, or `expr2` otherwise.
    case NaNvl(left, right) => s"NANVL(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"

    // negative(expr) - Returns the negated value of `expr`.
    case UnaryMinus(left, _) => s"-(${exprSql(ctx, left)})"

    // not expr - Logical not.
    case Not(left) => s"NOT(${exprSql(ctx, left)})"

    // nullif(expr1, expr2) - Returns null if `expr1` equals to `expr2`, or `expr1` otherwise.
    case NullIf(left, right, _) => s"NULLIF(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"

    // octet_length(expr) - Returns the byte length of string data or number of bytes
    // of binary data.
    case OctetLength(left) => s"OCTET_LENGTH(${exprSql(ctx, left)})"

    // overlay(input, replace, pos[, len]) - Replace `input` with `replace` that
    // starts at `pos` and is of length `len`.
    case Overlay(left, right, c, d) => s"OVERLAY(${exprSql(ctx, left)}, " +
        s"${exprSql(ctx, right)}, ${exprSql(ctx, c)}, ${exprSql(ctx, d)})"

    // parse_url(url, partToExtract[, key]) - Extracts a part from a URL.
    case ParseUrl(left, right) => s"PARSE_URL(${exprsSql(ctx, left)}, $right)"

    // posexplode(expr) - Separates the elements of array `expr` into multiple rows with
    // positions, or the elements of map `expr` into multiple rows and columns with positions.
    // Unless specified otherwise, uses the column name `pos` for position, `col` for elements
    // of the array or `key` and `value` for elements of the map.
    case PosExplode(left) => s"POSEXPLODE(${exprSql(ctx, left)})"

    // positive(expr) - Returns the value of `expr`.
    case UnaryPositive(left) => s"POSITIVE(${exprSql(ctx, left)})"

    // pow(expr1, expr2) - Raises `expr1` to the power of `expr2`.
    case Pow(left, right) => s"POW(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"

    // radians(expr) - Converts degrees to radians.
    case ToRadians(left) => s"RADIANS(${exprSql(ctx, left)})"

    // raise_error(expr) - Throws an exception with `expr`.
    case RaiseError(left, right) => s"RAISE_ERROR(${exprSql(ctx, left)}, $right)"

    case RegExpExtract(left, right, c) =>
      s"REGEXP_EXTRACT(${exprSql(ctx, left)}, ${exprSql(ctx, right)}, ${exprSql(ctx, c)})"

    case RegExpExtractAll(left, right, c) =>
      s"REGEXP_EXTRACT_ALL(${exprSql(ctx, left)}, ${exprSql(ctx, right)}, ${exprSql(ctx, c)})"

    // regexp_replace(str, regexp, rep[, position]) - Replaces all substrings of `str`
    // that match `regexp` with `rep`.
    case RegExpReplace(left, right, c, d) =>
      s"REGEXP_REPLACE(${exprSql(ctx, left)}, ${exprSql(ctx, right)},"+
        s" ${exprSql(ctx, c)}, ${exprSql(ctx, d)})"

    // repeat(str, n) - Returns the string which repeats the given string value n times.
    case StringRepeat(left, right) => s"REPEAT(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"

    // replace(str, search[, replace]) - Replaces all occurrences of `search` with `replace`.
    case StringReplace(left, right, c) =>
      s"REPLACE(${exprSql(ctx, left)}, ${exprSql(ctx, right)}, ${exprSql(ctx, c)})"

    // rint(expr) - Returns the double value that is closest in value to the argument and
    // is equal to a mathematical integer.
    case Rint(left) => s"RINT(${exprSql(ctx, left)})"

    // str rlike regexp - Returns true if `str` matches `regexp`, or false otherwise.
    case RLike(left, right) => s"${exprSql(ctx, left)} RLIKE ${exprSql(ctx, right)}"

    case Rollup(left) => s"ROLLUP(${exprsSql(ctx, left)})"

    // round(expr, d) - Returns `expr` rounded to `d` decimal places using HALF_UP rounding mode.
    case Round(left, right) => s"ROUND(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"

    case StringRPad(left, right, c) =>
      s"RPAD(${exprSql(ctx, left)}, ${exprSql(ctx, right)}, ${exprSql(ctx, c)})"

    case StringTrimRight(left, right) => s"RTRIM(${exprSql(ctx, left)}, $right)"

    // schema_of_csv(csv[, options]) - Returns schema in the DDL format of CSV string.
    case SchemaOfCsv(left, right) => s"SCHEMA_OF_CSV(${exprSql(ctx, left)}, $right)"

    // sentences(str[, lang, country]) - Splits `str` into an array of array of words.
    case Sentences(left, right, c) =>
      s"SENTENCES(${exprSql(ctx, left)}, ${exprSql(ctx, right)}, ${exprSql(ctx, c)})"

    // sha(expr) - Returns a sha1 hash value as a hex string of the `expr`.
    case Sha1(left) => s"SHA(${exprSql(ctx, left)})"

    case Sha2(left, right) => s"SHA2(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"

    // shiftleft(base, expr) - Bitwise left shift.
    case ShiftLeft(left, right) => s"SHIFTLEFT(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"

    // shiftright(base, expr) - Bitwise (signed) right shift.
    case ShiftRight(left, right) => s"SHIFTRIGHT(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"

    // shiftrightunsigned(base, expr) - Bitwise unsigned right shift.
    case ShiftRightUnsigned(left, right) =>
      s"SHIFTRIGHTUNSIGNED(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"

    // sign(expr) - Returns -1.0, 0.0 or 1.0 as `expr` is negative, 0 or positive.
    case Signum(left) => s"SIGN(${exprSql(ctx, left)})"

    // sin(expr) - Returns the sine of `expr`, as if computed by `java.lang.Math.sin`.
    case Sin(left) => s"SIN(${exprSql(ctx, left)})"

    case Sinh(left) => s"SINH(${exprSql(ctx, left)})"

    case Size(left, _) => s"SIZE(${exprSql(ctx, left)})"

    // soundex(str) - Returns Soundex code of the string.
    case SoundEx(left) => s"SOUNDEX(${exprSql(ctx, left)})"

    // space(n) - Returns a string consisting of `n` spaces.
    case StringSpace(left) => s"SPACE(${exprSql(ctx, left)})"

    // spark_partition_id() - Returns the current partition id.
    case SparkPartitionID() => s"SPARK_PARTITION_ID()"

    // split(str, regex[, limit]) - Splits `str` around occurrences that match `regex`
    // and returns an array with a length of at most `limit`
    case StringSplit(left, right, c) if c == Literal(-1) =>
      s"SPLIT(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"

    case StringSplit(left, right, c) =>
      s"SPLIT(${exprSql(ctx, left)}, ${exprSql(ctx, right)}, ${exprSql(ctx, c)})"

    // sqrt(expr) - Returns the square root of `expr`.
    case Sqrt(left) => s"SQRT(${exprSql(ctx, left)})"

    // stack(n, expr1, ..., exprk) - Separates `expr1`, ..., `exprk` into `n` rows.
    // Uses column names col0, col1, etc. by default unless specified otherwise.
    case Stack(left) => s"STACK(${exprsSql(ctx, left)})"

    // str_to_map(text[, pairDelim[, keyValueDelim]]) - Creates a map after splitting the text
    // into key/value pairs using delimiters. Default delimiters are ',' for `pairDelim` and ':'
    // for `keyValueDelim`. Both `pairDelim` and `keyValueDelim` are treated as regular expressions.
    case StringToMap(left, right, c) =>
      s"STR_TO_MAP(${exprSql(ctx, left)}, ${exprSql(ctx, right)}, ${exprSql(ctx, c)})"

    case Substring(left, right, c) =>
      s"SUBSTR(${exprSql(ctx, left)}, ${exprSql(ctx, right)}, ${exprSql(ctx, c)})"

    case SubstringIndex(left, right, c) =>
      s"SUBSTRING_INDEX(${exprSql(ctx, left)}, ${exprSql(ctx, right)}, ${exprSql(ctx, c)})"

    case Tan(left) => s"TAN(${exprSql(ctx, left)})"

    case Tanh(left) => s"TANH(${exprSql(ctx, left)})"

    // to_csv(expr[, options]) - Returns a CSV string with a given struct value
    case StructsToCsv(left, right, c) => s"TO_CSV($left, ${exprSql(ctx, right)}, $c)"

    // transform(expr, func) - Transforms elements in an array using the function.
    case ArrayTransform(left, right) => s"TRANSFORM(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"

    // transform_keys(expr, func) - Transforms elements in a map using the function.
    case TransformKeys(left, right) =>
      s"TRANSFORM_KEYS(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"

    // transform_values(expr, func) - Transforms values in the map using the function.
    case TransformValues(left, right) =>
      s"TRANSFORM_VALUES(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"

    // translate(input, from, to) - Translates the `input` string by replacing the characters
    // present in the `from` string with the corresponding characters in the `to` string.
    case StringTranslate(left, right, c) =>
      s"TRANSLATE(${exprSql(ctx, left)}, ${exprSql(ctx, right)}, ${exprSql(ctx, c)})"

    case StringTrim(left, right) => s"TRIM(${exprSql(ctx, left)}, $right)"

    // typeof(expr) - Return DDL-formatted type string for the data type of the input.
    case TypeOf(left) => s"TYPEOF(${exprSql(ctx, left)})"

    // unbase64(str) - Converts the argument from a base 64 string `str` to a binary.
    case UnBase64(left) => s"UNBASE64(${exprSql(ctx, left)})"

    // unhex(expr) - Converts hexadecimal `expr` to binary.
    case Unhex(left) => s"UNHEX(${exprSql(ctx, left)})"

    // upper(str) - Returns `str` with all characters changed to uppercase.
    case Upper(left) => s"UPPER(${exprSql(ctx, left)})"

    // uuid() - Returns an universally unique identifier (UUID) string.
    // The value is returned as a canonical UUID 36-character string.
    case Uuid(_) => s"UUID()"

    case WidthBucket(left, right, c, d) =>
      s"WIDTH_BUCKET(${exprSql(ctx, left)}, ${exprSql(ctx, right)}," +
        s" ${exprSql(ctx, c)}, ${exprSql(ctx, d)})"

    // zip_with(left, right, func) - Merges the two given arrays, element-wise,
    // into a single array using function. If one array is shorter, nulls are
    // appended at the end to match the length of the longer array, before applying function.
    case ZipWith(left, right, c) =>
      s"ZIP_WITH(${exprSql(ctx, left)}, ${exprSql(ctx, right)}, ${exprSql(ctx, c)})"

    case ApproximatePercentile(left, right, c, d, e) =>
      s"APPROX_PERCENTILE(${exprSql(ctx, left)}, " +
        s"${exprSql(ctx, right)}, ${exprSql(ctx, c)}, $d, $e)"

    // avg(expr) - Returns the mean calculated from values of a group.
    case Average(left) => s"AVG(${exprSql(ctx, left)})"

    // bit_and(expr) - Returns the bitwise AND of all non-null input values, or null if none.
    case BitAndAgg(left) => s"BIT_AND(${exprSql(ctx, left)})"

    // bit_or(expr) - Returns the bitwise OR of all non-null input values, or null if none.
    case BitOrAgg(left) => s"BIT_OR(${exprSql(ctx, left)})"

    // bit_xor(expr) - Returns the bitwise XOR of all non-null input values, or null if none.
    case BitXorAgg(left) => s"BIT_XOR(${exprSql(ctx, left)})"

    // collect_list(expr) - Collects and returns a list of non-unique elements.
    case CollectList(left, _, _) => s"COLLECT_LIST(${exprSql(ctx, left)})"

    // collect_set(expr) - Collects and returns a set of unique elements.
    case CollectSet(left, _, _) => s"COLLECT_SET(${exprSql(ctx, left)})"

    // corr(expr1, expr2) - Returns Pearson coefficient
    // of correlation between a set of number pairs.
    case Corr(left, right, _) => s"CORR(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"

    case Count(left) => s"COUNT(${exprsSql(ctx, left)})"

    case CountIf(left) => s"COUNT_IF(${exprSql(ctx, left)})"

    // every(expr) - Returns true if all values of `expr` are true.
    case BoolAnd(left) => s"EVERY(${exprSql(ctx, left)})"

    case First(left, _) => s"FIRST(${exprSql(ctx, left)})"

    // kurtosis(expr) - Returns the kurtosis value calculated from values of a group.
    case Kurtosis(left, _) => s"KURTOSIS(${exprSql(ctx, left)})"

    case Last(left, _) => s"LAST(${exprSql(ctx, left)})"

    // max(expr) - Returns the maximum value of `expr`.
    case Max(left) => s"MAX(${exprSql(ctx, left)})"

    // max_by(x, y) - Returns the value of `x` associated with the maximum value of `y`.
    case MaxBy(left, right) => s"MAX_BY(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"

    // min(expr) - Returns the minimum value of `expr`.
    case Min(left) => s"MIN(${exprSql(ctx, left)})"

    // min_by(x, y) - Returns the value of `x` associated with the minimum value of `y`.
    case MinBy(left, right) => s"MIN_BY(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"

    // skewness(expr) - Returns the skewness value calculated from values of a group.
    case Skewness(left, _) => s"SKEWNESS(${exprSql(ctx, left)})"

    // some(expr) - Returns true if at least one value of `expr` is true.
    case BoolOr(left) => s"SOME(${exprSql(ctx, left)})"

    // std(expr) - Returns the sample standard deviation calculated from values of a group.
    case StddevSamp(left, _) => s"STD(${exprSql(ctx, left)})"

    // stddev_pop(expr) - Returns the population standard deviation calculated from values of a group.
    case StddevPop(left, _) => s"STDDEV_POP(${exprSql(ctx, left)})"

    // sum(expr) - Returns the sum calculated from values of a group.
    case Sum(left) => s"SUM(${exprSql(ctx, left)})"

    // array_contains(array, value) - Returns true if the array contains the value.
    case ArrayContains(left, right) =>
      s"ARRAY_CONTAINS(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"

    // array_distinct(array) - Removes duplicate values from the array.
    case ArrayDistinct(left) => s"ARRAY_DISTINCT(${exprSql(ctx, left)})"

    case ArrayExcept(left, right) => s"ARRAY_EXCEPT(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"

    case ArrayIntersect(left, right) =>
      s"ARRAY_INTERSECT(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"

    case ArrayJoin(left, right, _) => s"ARRAY_JOIN(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"

    // array_max(array) - Returns the maximum value in the array. NULL elements are skipped.
    case ArrayMax(left) => s"ARRAY_MAX(${exprSql(ctx, left)})"

    // array_min(array) - Returns the minimum value in the array. NULL elements are skipped.
    case ArrayMin(left) => s"ARRAY_MIN(${exprSql(ctx, left)})"

    case ArrayPosition(left, right) =>
      s"ARRAY_POSITION(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"

    // array_remove(array, element) - Remove all elements that equal to element from array.
    case ArrayRemove(left, right) => s"ARRAY_REMOVE(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"

    // array_repeat(element, count) - Returns the array containing element count times.
    case ArrayRepeat(left, right) => s"ARRAY_REPEAT(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"

    case ArrayUnion(left, right) => s"ARRAY_UNION(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"

    // arrays_overlap(a1, a2) - Returns true if a1 contains at least a non-null element
    // present also in a2. If the arrays have no common element and they are both non-empty
    // and either of them contains a null element null is returned, false otherwise.
    case ArraysOverlap(left, right) =>
      s"ARRAYS_OVERLAP(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"

    case ArraysZip(left) => s"ARRAYS_ZIP(${exprsSql(ctx, left)})"

    // concat(col1, col2, ..., colN) - Returns the concatenation of col1, col2, ..., colN.
    case Concat(left) => s"CONCAT(${exprsSql(ctx, left)})"

    // flatten(arrayOfArrays) - Transforms an array of arrays into a single array.
    case Flatten(left) => s"FLATTEN(${exprSql(ctx, left)})"

    // reverse(array) - Returns a reversed string or an array with reverse order of elements.
    case Reverse(left) => s"REVERSE(${exprSql(ctx, left)})"

    // shuffle(array) - Returns a random permutation of the given array.
    case Shuffle(left, _) => s"SHUFFLE(${exprSql(ctx, left)})"

    // slice(x, start, length) - Subsets array x starting from index start
    // (array indices start at 1, or starting from the end if start is negative)
    // with the specified length.
    case Slice(left, right, c) =>
      s"SLICE(${exprSql(ctx, left)}, ${exprSql(ctx, right)}, ${exprSql(ctx, c)})"

    case SortArray(left, right) => s"SORT_ARRAY(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"

    // add_months(start_date, num_months) -
    // Returns the date that is `num_months` after `start_date`.
    case AddMonths(left, right) => s"ADD_MONTHS(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"

    case CurrentDate(_) => s"CURRENT_DATE()"

    case CurrentTimestamp() => s"CURRENT_TIMESTAMP()"

    // current_timezone() - Returns the current session local timezone.
    case CurrentTimeZone() => s"CURRENT_TIMEZONE()"

    // date_add(start_date, num_days) - Returns the date that is `num_days` after `start_date`.
    case DateAdd(left, right) => s"DATE_ADD(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"

    // date_format(timestamp, fmt) - Converts `timestamp` to a value of string
    // in the format specified by the date format `fmt`.
    case DateFormatClass(left, right, _) =>
      s"DATE_FORMAT(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"

    // date_from_unix_date(days) - Create date from the number of days since 1970-01-01.
    case DateFromUnixDate(left) => s"DATE_FROM_UNIX_DATE(${exprSql(ctx, left)})"

    // date_sub(start_date, num_days) - Returns the date that is `num_days` before `start_date`.
    case DateSub(left, right) => s"DATE_SUB(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"

    case TruncTimestamp(left, right, _) =>
      s"DATE_TRUNC(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"

    // datediff(endDate, startDate) - Returns the number of days from `startDate` to `endDate`.
    case DateDiff(left, right) => s"DATEDIFF(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"

    // dayofweek(date) - Returns the day of the week for date/timestamp
    // (1 = Sunday, 2 = Monday, ..., 7 = Saturday).
    case DayOfWeek(left) => s"DAYOFWEEK(${exprSql(ctx, left)})"

    // dayofyear(date) - Returns the day of year of the date/timestamp.
    case DayOfYear(left) => s"DAYOFYEAR(${exprSql(ctx, left)})"

    // next_day(start_date, day_of_week) - Returns the first date which is later
    // than `start_date` and named as indicated.
    case NextDay(left, right) => s"NEXT_DAY(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"

    // quarter(date) - Returns the quarter of the year for date, in the range 1 to 4.
    case Quarter(left) => s"QUARTER(${exprSql(ctx, left)})"

    // second(timestamp) - Returns the second component of the string/timestamp.
    case Second(left, right) => s"SECOND(${exprSql(ctx, left)}, $right)"

    // get_json_object(json_txt, path) - Extracts a json object from `path`.
    case GetJsonObject(left, right) =>
      s"GET_JSON_OBJECT(${exprSql(ctx, left)}, ${exprSql(ctx, right)})"

    // json_array_length(jsonArray) - Returns the number of elements in the outmost JSON array.
    case LengthOfJsonArray(left) => s"JSON_ARRAY_LENGTH(${exprSql(ctx, left)})"

    // json_object_keys(json_object) - Returns all the keys of the outmost JSON object as an array.
    case JsonObjectKeys(left) => s"JSON_OBJECT_KEYS(${exprSql(ctx, left)})"

    // json_tuple(jsonStr, p1, p2, ..., pn) - Returns a tuple like the function get_json_object,
    // but it takes multiple names. All the input parameters and output column types are string.
    case JsonTuple(left) => s"JSON_TUPLE(${exprsSql(ctx, left)})"

    // map_concat(map, ...) - Returns the union of all the given maps
    case MapConcat(left) => s"MAP_CONCAT(${exprsSql(ctx, left)})"

    // map_entries(map) - Returns an unordered array of all entries in the given map.
    case MapEntries(left) => s"MAP_ENTRIES(${exprSql(ctx, left)})"

    // map_from_entries(arrayOfEntries) - Returns a map created from the given array of entries.
    case MapFromEntries(left) => s"MAP_FROM_ENTRIES(${exprSql(ctx, left)})"

    // map_keys(map) - Returns an unordered array containing the keys of the map.
    case MapKeys(left) => s"MAP_KEYS(${exprSql(ctx, left)})"

    // map_values(map) - Returns an unordered array containing the values of the map.
    case MapValues(left) => s"MAP_VALUES(${exprSql(ctx, left)})"

    // giving up and resorting to almost pretty SQL.
    // Generated function calls are all uppercase.
    case _ => expr.sql
  }
}
