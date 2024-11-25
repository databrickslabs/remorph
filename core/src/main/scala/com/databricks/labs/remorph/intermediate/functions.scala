package com.databricks.labs.remorph.intermediate

import com.databricks.labs.remorph.transpilers.TranspileException

import java.util.Locale

trait Fn extends Expression {
  def prettyName: String
}

case class CallFunction(function_name: String, arguments: Seq[Expression]) extends Expression with Fn {
  override def children: Seq[Expression] = arguments
  override def dataType: DataType = UnresolvedType
  override def prettyName: String = function_name.toUpperCase(Locale.getDefault)
}

class CallMapper extends Rule[LogicalPlan] with IRHelpers {

  override final def apply(plan: LogicalPlan): LogicalPlan = {
    plan transformAllExpressions { case fn: Fn =>
      try {
        convert(fn)
      } catch {
        case e: IndexOutOfBoundsException =>
          throw TranspileException(WrongNumberOfArguments(fn.prettyName, fn.children.size, e.getMessage))

      }
    }
  }

  /** This function is supposed to be overridden by dialects */
  def convert(call: Fn): Expression = withNormalizedName(call) match {
    case CallFunction("ABS", args) => Abs(args.head)
    case CallFunction("ACOS", args) => Acos(args.head)
    case CallFunction("ACOSH", args) => Acosh(args.head)
    case CallFunction("ADD_MONTHS", args) => AddMonths(args.head, args(1))
    case CallFunction("AGGREGATE", args) => ArrayAggregate(args.head, args(1), args(2), args(3))
    case CallFunction("ANY", args) => BoolOr(args.head)
    case CallFunction("APPROX_COUNT_DISTINCT", args) => HyperLogLogPlusPlus(args.head, args(1))
    case CallFunction("ARRAYS_OVERLAP", args) => ArraysOverlap(args.head, args(1))
    case CallFunction("ARRAYS_ZIP", args) => ArraysZip(args)
    case CallFunction("ARRAY_CONTAINS", args) => ArrayContains(args.head, args(1))
    case CallFunction("ARRAY_DISTINCT", args) => ArrayDistinct(args.head)
    case CallFunction("ARRAY_EXCEPT", args) => ArrayExcept(args.head, args(1))
    case CallFunction("ARRAY_INTERSECT", args) => ArrayIntersect(args.head, args(1))
    case CallFunction("ARRAY_JOIN", args) =>
      val delim = if (args.size >= 3) Some(args(2)) else None
      ArrayJoin(args.head, args(1), delim)
    case CallFunction("ARRAY_MAX", args) => ArrayMax(args.head)
    case CallFunction("ARRAY_MIN", args) => ArrayMin(args.head)
    case CallFunction("ARRAY_POSITION", args) => ArrayPosition(args.head, args(1))
    case CallFunction("ARRAY_REMOVE", args) => ArrayRemove(args.head, args(1))
    case CallFunction("ARRAY_REPEAT", args) => ArrayRepeat(args.head, args(1))
    case CallFunction("ARRAY_SORT", args) => ArraySort(args.head, args(1))
    case CallFunction("ARRAY_UNION", args) => ArrayUnion(args.head, args(1))
    case CallFunction("ASCII", args) => Ascii(args.head)
    case CallFunction("ASIN", args) => Asin(args.head)
    case CallFunction("ASINH", args) => Asinh(args.head)
    case CallFunction("ASSERT_TRUE", args) => AssertTrue(args.head, args(1))
    case CallFunction("ATAN", args) => Atan(args.head)
    case CallFunction("ATAN2", args) => Atan2(args.head, args(1))
    case CallFunction("ATANH", args) => Atanh(args.head)
    case CallFunction("AVG", args) => Average(args.head)
    case CallFunction("BASE64", args) => Base64(args.head)
    case CallFunction("BIN", args) => Bin(args.head)
    case CallFunction("BIT_AND", args) => BitAndAgg(args.head)
    case CallFunction("BIT_COUNT", args) => BitwiseCount(args.head)
    case CallFunction("BIT_GET", args) => BitwiseGet(args.head, args(1))
    case CallFunction("GETBIT", args) => BitwiseGet(args.head, args(1)) // Synonym for BIT_GET
    case CallFunction("BIT_LENGTH", args) => BitLength(args.head)
    case CallFunction("BIT_OR", args) => BitOrAgg(args.head)
    case CallFunction("BIT_XOR", args) => BitXorAgg(args.head)
    case CallFunction("BOOL_AND", args) => BoolAnd(args.head)
    case CallFunction("BROUND", args) => BRound(args.head, args(1))
    case CallFunction("CBRT", args) => Cbrt(args.head)
    case CallFunction("CEIL", args) => Ceil(args.head)
    case CallFunction("CHAR", args) => Chr(args.head)
    case CallFunction("COALESCE", args) => Coalesce(args)
    case CallFunction("COLLECT_LIST", args) => CollectList(args.head, args.tail.headOption)
    case CallFunction("COLLECT_SET", args) => CollectSet(args.head)
    case CallFunction("CONCAT", args) => Concat(args)
    case CallFunction("CONCAT_WS", args) => ConcatWs(args)
    case CallFunction("CONV", args) => Conv(args.head, args(1), args(2))
    case CallFunction("CORR", args) => Corr(args.head, args(1))
    case CallFunction("COS", args) => Cos(args.head)
    case CallFunction("COSH", args) => Cosh(args.head)
    case CallFunction("COT", args) => Cot(args.head)
    case CallFunction("COUNT", args) => Count(args)
    case CallFunction("COUNT_IF", args) => CountIf(args.head)
    case CallFunction("COUNT_MIN_SKETCH", args) =>
      CountMinSketchAgg(args.head, args(1), args(2), args(3))
    case CallFunction("COVAR_POP", args) => CovPopulation(args.head, args(1))
    case CallFunction("COVAR_SAMP", args) => CovSample(args.head, args(1))
    case CallFunction("CRC32", args) => Crc32(args.head)
    case CallFunction("CUBE", args) => Cube(args)
    case CallFunction("CUME_DIST", _) => CumeDist()
    case CallFunction("CURRENT_CATALOG", _) => CurrentCatalog()
    case CallFunction("CURRENT_DATABASE", _) => CurrentDatabase()
    case CallFunction("CURRENT_DATE", _) => CurrentDate()
    case CallFunction("CURRENT_TIMESTAMP", _) => CurrentTimestamp()
    case CallFunction("CURRENT_TIMEZONE", _) => CurrentTimeZone()
    case CallFunction("DATEDIFF", args) => DateDiff(args.head, args(1))
    case CallFunction("DATE_ADD", args) => DateAdd(args.head, args(1))
    case CallFunction("DATE_FORMAT", args) => DateFormatClass(args.head, args(1))
    case CallFunction("DATE_FROM_UNIX_DATE", args) => DateFromUnixDate(args.head)
    case CallFunction("DATE_PART", args) => DatePart(args.head, args(1))
    case CallFunction("DATE_SUB", args) => DateSub(args.head, args(1))
    case CallFunction("DATE_TRUNC", args) => TruncTimestamp(args.head, args(1))
    case CallFunction("DAYOFMONTH", args) => DayOfMonth(args.head)
    case CallFunction("DAYOFWEEK", args) => DayOfWeek(args.head)
    case CallFunction("DAYOFYEAR", args) => DayOfYear(args.head)
    case CallFunction("DECODE", args) => Decode(args.head, args(1))
    case CallFunction("DEGREES", args) => ToDegrees(args.head)
    case CallFunction("DENSE_RANK", args) => DenseRank(args)
    case CallFunction("DIV", args) => IntegralDivide(args.head, args(1))
    case CallFunction("E", _) => EulerNumber()
    case CallFunction("ELEMENT_AT", args) => ElementAt(args.head, args(1))
    case CallFunction("ELT", args) => Elt(args)
    case CallFunction("ENCODE", args) => Encode(args.head, args(1))
    case CallFunction("EXISTS", args) => ArrayExists(args.head, args(1))
    case CallFunction("EXP", args) => Exp(args.head)
    case CallFunction("EXPLODE", args) => Explode(args.head)
    case CallFunction("EXPM1", args) => Expm1(args.head)
    case CallFunction("EXTRACT", args) => Extract(args.head, args(1))
    case CallFunction("FACTORIAL", args) => Factorial(args.head)
    case CallFunction("FILTER", args) => ArrayFilter(args.head, args(1))
    case CallFunction("FIND_IN_SET", args) => FindInSet(args.head, args(1))
    case CallFunction("FIRST", args) => First(args.head, args.lift(1))
    case CallFunction("FLATTEN", args) => Flatten(args.head)
    case CallFunction("FLOOR", args) => Floor(args.head)
    case CallFunction("FORALL", args) => ArrayForAll(args.head, args(1))
    case CallFunction("FORMAT_NUMBER", args) => FormatNumber(args.head, args(1))
    case CallFunction("FORMAT_STRING", args) => FormatString(args)
    case CallFunction("FROM_CSV", args) => CsvToStructs(args.head, args(1), args(2))
    case CallFunction("FROM_JSON", args) => JsonToStructs(args.head, args(1), args.lift(2))
    case CallFunction("FROM_UNIXTIME", args) => FromUnixTime(args.head, args(1))
    case CallFunction("FROM_UTC_TIMESTAMP", args) => FromUTCTimestamp(args.head, args(1))
    case CallFunction("GET_JSON_OBJECT", args) => GetJsonObject(args.head, args(1))
    case CallFunction("GREATEST", args) => Greatest(args)
    case CallFunction("GROUPING", args) => Grouping(args.head)
    case CallFunction("GROUPING_ID", args) => GroupingID(args)
    case CallFunction("HASH", args) => Murmur3Hash(args)
    case CallFunction("HEX", args) => Hex(args.head)
    case CallFunction("HOUR", args) => Hour(args.head)
    case CallFunction("HYPOT", args) => Hypot(args.head, args(1))
    case CallFunction("IF", args) => If(args.head, args(1), args(2))
    case CallFunction("IFNULL", args) => IfNull(args.head, args(1))
    case CallFunction("IN", args) => In(args.head, args.tail) // TODO: not a function
    case CallFunction("INITCAP", args) => InitCap(args.head)
    case CallFunction("INLINE", args) => Inline(args.head)
    case CallFunction("INPUT_FILE_BLOCK_LENGTH", _) => InputFileBlockLength()
    case CallFunction("INPUT_FILE_BLOCK_START", _) => InputFileBlockStart()
    case CallFunction("INPUT_FILE_NAME", _) => InputFileName()
    case CallFunction("INSTR", args) => StringInstr(args.head, args(1))
    case CallFunction("ISNAN", args) => IsNaN(args.head)
    case CallFunction("JAVA_METHOD", args) => CallMethodViaReflection(args)
    case CallFunction("JSON_ARRAY_LENGTH", args) => LengthOfJsonArray(args.head)
    case CallFunction("JSON_OBJECT_KEYS", args) => JsonObjectKeys(args.head)
    case CallFunction("JSON_TUPLE", args) => JsonTuple(args)
    case CallFunction("KURTOSIS", args) => Kurtosis(args.head)
    case CallFunction("LAG", args) => Lag(args.head, args.lift(1), args.lift(2))
    case CallFunction("LAST", args) => Last(args.head, args.lift(1))
    case CallFunction("LAST_DAY", args) => LastDay(args.head)
    case CallFunction("LEAD", args) => Lead(args.head, args.lift(1), args.lift(2))
    case CallFunction("LEAST", args) => Least(args)
    case CallFunction("LEFT", args) => Left(args.head, args(1))
    case CallFunction("LENGTH", args) => Length(args.head)
    case CallFunction("LEVENSHTEIN", args) => Levenshtein(args.head, args(1), args.lift(2))
    case CallFunction("LN", args) => Log(args.head)
    case CallFunction("LOG", args) => Logarithm(args.head, args(1))
    case CallFunction("LOG10", args) => Log10(args.head)
    case CallFunction("LOG1P", args) => Log1p(args.head)
    case CallFunction("LOG2", args) => Log2(args.head)
    case CallFunction("LOWER", args) => Lower(args.head)
    case CallFunction("LPAD", args) =>
      StringLPad(args.head, args(1), args.lastOption.getOrElse(Literal(" ")))
    case CallFunction("LTRIM", args) => StringTrimLeft(args.head, args.lift(1))
    case CallFunction("MAKE_DATE", args) => MakeDate(args.head, args(1), args(2))
    case CallFunction("MAKE_INTERVAL", args) =>
      MakeInterval(args.head, args(1), args(2), args(3), args(4), args(5))
    case CallFunction("MAKE_TIMESTAMP", args) =>
      MakeTimestamp(args.head, args(1), args(2), args(3), args(4), args(5), Some(args(6)))
    case CallFunction("MAP", args) => CreateMap(args, useStringTypeWhenEmpty = false)
    case CallFunction("MAP_CONCAT", args) => MapConcat(args)
    case CallFunction("MAP_ENTRIES", args) => MapEntries(args.head)
    case CallFunction("MAP_FILTER", args) => MapFilter(args.head, args(1))
    case CallFunction("MAP_FROM_ARRAYS", args) => MapFromArrays(args.head, args(1))
    case CallFunction("MAP_FROM_ENTRIES", args) => MapFromEntries(args.head)
    case CallFunction("MAP_KEYS", args) => MapKeys(args.head)
    case CallFunction("MAP_VALUES", args) => MapValues(args.head)
    case CallFunction("MAP_ZIP_WITH", args) => MapZipWith(args.head, args(1), args(2))
    case CallFunction("MAX", args) => Max(args.head)
    case CallFunction("MAX_BY", args) => MaxBy(args.head, args(1))
    case CallFunction("MD5", args) => Md5(args.head)
    case CallFunction("MIN", args) => Min(args.head)
    case CallFunction("MINUTE", args) => Minute(args.head)
    case CallFunction("MIN_BY", args) => MinBy(args.head, args(1))
    case CallFunction("MOD", args) => Remainder(args.head, args(1))
    case CallFunction("MONOTONICALLY_INCREASING_ID", _) => MonotonicallyIncreasingID()
    case CallFunction("MONTH", args) => Month(args.head)
    case CallFunction("MONTHS_BETWEEN", args) => MonthsBetween(args.head, args(1), args(2))
    case CallFunction("NAMED_STRUCT", args) => CreateNamedStruct(args)
    case CallFunction("NANVL", args) => NaNvl(args.head, args(1))
    case CallFunction("NEGATIVE", args) => UnaryMinus(args.head)
    case CallFunction("NEXT_DAY", args) => NextDay(args.head, args(1))
    case CallFunction("NOW", _) => Now()
    case CallFunction("NTH_VALUE", args) => NthValue(args.head, args(1), args.lift(2))
    case CallFunction("NTILE", args) => NTile(args.head)
    case CallFunction("NULLIF", args) => NullIf(args.head, args(1))
    case CallFunction("NVL", args) => Nvl(args.head, args(1))
    case CallFunction("NVL2", args) => Nvl2(args.head, args(1), args(2))
    case CallFunction("OCTET_LENGTH", args) => OctetLength(args.head)
    case CallFunction("OVERLAY", args) => Overlay(args.head, args(1), args(2), args(3))
    case CallFunction("PARSE_URL", args) => ParseUrl(args)
    case CallFunction("PERCENTILE", args) => Percentile(args.head, args(1), args(2))
    case CallFunction("PERCENTILE_APPROX", args) => ApproximatePercentile(args.head, args(1), args(2))
    case CallFunction("PERCENT_RANK", args) => PercentRank(args)
    case CallFunction("PI", _) => Pi()
    case CallFunction("PMOD", args) => Pmod(args.head, args(1))
    case CallFunction("POSEXPLODE", args) => PosExplode(args.head)
    case CallFunction("POSITION", args) =>
      StringLocate(args.head, args(1), args.lastOption.getOrElse(Literal(1)))
    case CallFunction("POSITIVE", args) => UnaryPositive(args.head)
    case CallFunction("POW", args) => Pow(args.head, args(1))
    case CallFunction("POWER", args) => Pow(args.head, args(1))
    case CallFunction("QUARTER", args) => Quarter(args.head)
    case CallFunction("RADIANS", args) => ToRadians(args.head)
    case CallFunction("RAISE_ERROR", args) => RaiseError(args.head)
    case CallFunction("RAND", args) => Rand(args.head)
    case CallFunction("RANDN", args) => Randn(args.head)
    case CallFunction("RANK", args) => Rank(args)
    case CallFunction("REGEXP_EXTRACT", args) => RegExpExtract(args.head, args(1), args(2))
    case CallFunction("REGEXP_EXTRACT_ALL", args) => RegExpExtractAll(args.head, args(1), args(2))
    case CallFunction("REGEXP_REPLACE", args) => RegExpReplace(args.head, args(1), args(2), args.lift(3))
    case CallFunction("REPEAT", args) => StringRepeat(args.head, args(1))
    case CallFunction("REPLACE", args) => StringReplace(args.head, args(1), args(2))
    case CallFunction("REVERSE", args) => Reverse(args.head)
    case CallFunction("RIGHT", args) => Right(args.head, args(1))
    case CallFunction("RINT", args) => Rint(args.head)
    case CallFunction("RLIKE", args) => RLike(args.head, args(1))
    case CallFunction("ROLLUP", args) => Rollup(args)
    case CallFunction("ROUND", args) => Round(args.head, args.lift(1))
    case CallFunction("ROW_NUMBER", _) => RowNumber()
    case CallFunction("RPAD", args) => StringRPad(args.head, args(1), args(2))
    case CallFunction("RTRIM", args) => StringTrimRight(args.head, args.lift(1))
    case CallFunction("SCHEMA_OF_CSV", args) => SchemaOfCsv(args.head, args(1))
    case CallFunction("SCHEMA_OF_JSON", args) => SchemaOfJson(args.head, args(1))
    case CallFunction("SECOND", args) => Second(args.head)
    case CallFunction("SENTENCES", args) => Sentences(args.head, args(1), args(2))
    case CallFunction("SEQUENCE", args) => Sequence(args.head, args(1), args(2))
    case CallFunction("SHA", args) => Sha1(args.head)
    case CallFunction("SHA2", args) => Sha2(args.head, args(1))
    case CallFunction("SHIFTLEFT", args) => ShiftLeft(args.head, args(1))
    case CallFunction("SHIFTRIGHT", args) => ShiftRight(args.head, args(1))
    case CallFunction("SHIFTRIGHTUNSIGNED", args) => ShiftRightUnsigned(args.head, args(1))
    case CallFunction("SHUFFLE", args) => Shuffle(args.head)
    case CallFunction("SIGN", args) => Signum(args.head)
    case CallFunction("SIN", args) => Sin(args.head)
    case CallFunction("SINH", args) => Sinh(args.head)
    case CallFunction("SIZE", args) => Size(args.head)
    case CallFunction("SKEWNESS", args) => Skewness(args.head)
    case CallFunction("SLICE", args) => Slice(args.head, args(1), args(2))
    case CallFunction("SORT_ARRAY", args) => SortArray(args.head, args.lift(1))
    case CallFunction("SOUNDEX", args) => SoundEx(args.head)
    case CallFunction("SPACE", args) => StringSpace(args.head)
    case CallFunction("SPARK_PARTITION_ID", _) => SparkPartitionID()
    case CallFunction("SPLIT", args) =>
      val delim = if (args.size >= 3) Some(args(2)) else None
      StringSplit(args.head, args(1), delim)
    case CallFunction("SPLIT_PART", args) => StringSplitPart(args.head, args(1), args(2))
    case CallFunction("SQRT", args) => Sqrt(args.head)
    case CallFunction("STACK", args) => Stack(args)
    case CallFunction("STD", args) => StdSamp(args.head)
    case CallFunction("STDDEV", args) => StddevSamp(args.head)
    case CallFunction("STDDEV_POP", args) => StddevPop(args.head)
    case CallFunction("STR_TO_MAP", args) => StringToMap(args.head, args(1), args(2))
    case CallFunction("SUBSTR", args) => Substring(args.head, args(1), args.lift(2))
    case CallFunction("SUBSTRING_INDEX", args) => SubstringIndex(args.head, args(1), args(2))
    case CallFunction("SUM", args) => Sum(args.head)
    case CallFunction("TAN", args) => Tan(args.head)
    case CallFunction("TANH", args) => Tanh(args.head)
    case CallFunction("TIMESTAMP_MICROS", args) => MicrosToTimestamp(args.head)
    case CallFunction("TIMESTAMP_MILLIS", args) => MillisToTimestamp(args.head)
    case CallFunction("TIMESTAMP_SECONDS", args) => SecondsToTimestamp(args.head)
    case CallFunction("TO_CSV", args) => StructsToCsv(args.head, args(1))
    case CallFunction("TO_DATE", args) => ParseToDate(args.head, args.lift(1))
    case CallFunction("TO_JSON", args) => StructsToJson(args.head, args.lift(1))
    case CallFunction("TO_NUMBER", args) => ToNumber(args.head, args(1))
    case CallFunction("TO_TIMESTAMP", args) => ParseToTimestamp(args.head, args.lift(1))
    case CallFunction("TO_UNIX_TIMESTAMP", args) => ToUnixTimestamp(args.head, args(1))
    case CallFunction("TO_UTC_TIMESTAMP", args) => ToUTCTimestamp(args.head, args(1))
    case CallFunction("TRANSFORM", args) => ArrayTransform(args.head, args(1))
    case CallFunction("TRANSFORM_KEYS", args) => TransformKeys(args.head, args(1))
    case CallFunction("TRANSFORM_VALUES", args) => TransformValues(args.head, args(1))
    case CallFunction("TRANSLATE", args) => StringTranslate(args.head, args(1), args(2))
    case CallFunction("TRIM", args) => StringTrim(args.head, args.lift(1))
    case CallFunction("TRUNC", args) => TruncDate(args.head, args(1))
    case CallFunction("TRY_TO_NUMBER", args) => TryToNumber(args.head, args(1))
    case CallFunction("TYPEOF", args) => TypeOf(args.head)
    case CallFunction("UCASE", args) => Upper(args.head)
    case CallFunction("UNBASE64", args) => UnBase64(args.head)
    case CallFunction("UNHEX", args) => Unhex(args.head)
    case CallFunction("UNIX_DATE", args) => UnixDate(args.head)
    case CallFunction("UNIX_MICROS", args) => UnixMicros(args.head)
    case CallFunction("UNIX_MILLIS", args) => UnixMillis(args.head)
    case CallFunction("UNIX_SECONDS", args) => UnixSeconds(args.head)
    case CallFunction("UNIX_TIMESTAMP", args) => UnixTimestamp(args.head, args(1))
    case CallFunction("UUID", _) => Uuid()
    case CallFunction("VAR_POP", args) => VariancePop(args.head)
    case CallFunction("VAR_SAMP", args) => VarianceSamp(args.head)
    case CallFunction("VERSION", _) => SparkVersion()
    case CallFunction("WEEKDAY", args) => WeekDay(args.head)
    case CallFunction("WEEKOFYEAR", args) => WeekOfYear(args.head)
    case CallFunction("WHEN", _) =>
      throw new IllegalArgumentException("WHEN (CaseWhen) should be handled separately")
    case CallFunction("WIDTH_BUCKET", args) => WidthBucket(args.head, args(1), args(2), args(3))
    case CallFunction("WINDOW", _) =>
      throw new IllegalArgumentException("WINDOW (TimeWindow) should be handled separately")
    case CallFunction("XPATH", args) => XPathList(args.head, args(1))
    case CallFunction("XPATH_BOOLEAN", args) => XPathBoolean(args.head, args(1))
    case CallFunction("XPATH_DOUBLE", args) => XPathDouble(args.head, args(1))
    case CallFunction("XPATH_FLOAT", args) => XPathFloat(args.head, args(1))
    case CallFunction("XPATH_INT", args) => XPathInt(args.head, args(1))
    case CallFunction("XPATH_LONG", args) => XPathLong(args.head, args(1))
    case CallFunction("XPATH_SHORT", args) => XPathShort(args.head, args(1))
    case CallFunction("XPATH_STRING", args) => XPathString(args.head, args(1))
    case CallFunction("XXHASH64", args) => XxHash64(args)
    case CallFunction("YEAR", args) => Year(args.head)
    case CallFunction("ZIP_WITH", args) => ZipWith(args.head, args(1), args(2))
    case _ => call // fallback
  }
}

/** abs(expr) - Returns the absolute value of the numeric value. */
case class Abs(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "ABS"
  override def dataType: DataType = left.dataType
}

/** acos(expr) - Returns the inverse cosine (a.k.a. arc cosine) of `expr`, as if computed by `java.lang.Math.acos`. */
case class Acos(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "ACOS"
  override def dataType: DataType = left.dataType
}

/** acosh(expr) - Returns inverse hyperbolic cosine of `expr`. */
case class Acosh(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "ACOSH"
  override def dataType: DataType = left.dataType
}

/**
 * aggregate(expr, start, merge, finish) - Applies a binary operator to an initial state and all elements in the array,
 * and reduces this to a single state. The final state is converted into the final result by applying a finish function.
 */
case class ArrayAggregate(left: Expression, right: Expression, merge: Expression, finish: Expression)
    extends Expression
    with Fn {
  override def prettyName: String = "AGGREGATE"
  override def children: Seq[Expression] = Seq(left, right, merge, finish)
  override def dataType: DataType = ArrayType(right.dataType)
}

/** array(expr, ...) - Returns an array with the given elements. */
case class CreateArray(children: Seq[Expression], useStringTypeWhenEmpty: Boolean = false) extends Expression with Fn {
  override def prettyName: String = "ARRAY"
  override def dataType: DataType = ArrayType(
    children.headOption
      .map(_.dataType)
      .getOrElse(if (useStringTypeWhenEmpty) StringType else NullType))
}

/**
 * array_sort(expr, func) - Sorts the input array. If func is omitted, sort in ascending order. The elements of the
 * input array must be orderable. Null elements will be placed at the end of the returned array. Since 3.0.0 this
 * function also sorts and returns the array based on the given comparator function. The comparator will take two
 * arguments representing two elements of the array. It returns -1, 0, or 1 as the first element is less than, equal to,
 * or greater than the second element. If the comparator function returns other values (including null), the function
 * will fail and raise an error.
 */
case class ArraySort(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "ARRAY_SORT"
  override def dataType: DataType = left.dataType
}

/** ascii(str) - Returns the numeric value of the first character of `str`. */
case class Ascii(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "ASCII"
  override def dataType: DataType = LongType
}

/**
 * asin(expr) - Returns the inverse sine (a.k.a. arc sine) the arc sin of `expr`, as if computed by
 * `java.lang.Math.asin`.
 */
case class Asin(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "ASIN"
  override def dataType: DataType = DoubleType
}

/** asinh(expr) - Returns inverse hyperbolic sine of `expr`. */
case class Asinh(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "ASINH"
  override def dataType: DataType = DoubleType
}

/** assert_true(expr) - Throws an exception if `expr` is not true. */
case class AssertTrue(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "ASSERT_TRUE"
  override def dataType: DataType = UnresolvedType
}

/**
 * atan(expr) - Returns the inverse tangent (a.k.a. arc tangent) of `expr`, as if computed by `java.lang.Math.atan`
 */
case class Atan(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "ATAN"
  override def dataType: DataType = DoubleType
}

/**
 * atan2(exprY, exprX) - Returns the angle in radians between the positive x-axis of a plane and the point given by the
 * coordinates (`exprX`, `exprY`), as if computed by `java.lang.Math.atan2`.
 */
case class Atan2(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "ATAN2"
  override def dataType: DataType = DoubleType
}

/** atanh(expr) - Returns inverse hyperbolic tangent of `expr`. */
case class Atanh(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "ATANH"
  override def dataType: DataType = DoubleType
}

/** base64(bin) - Converts the argument from a binary `bin` to a base64 string. */
case class Base64(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "BASE64"
  override def dataType: DataType = StringType
}

/** bin(expr) - Returns the string representation of the long value `expr` represented in binary. */
case class Bin(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "BIN"
  override def dataType: DataType = StringType
}

/**
 * bit_count(expr) - Returns the number of bits that are set in the argument expr as an unsigned 64-bit integer, or NULL
 * if the argument is NULL.
 */
case class BitwiseCount(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "BIT_COUNT"
  override def dataType: DataType = LongType
}

/** bit_length(expr) - Returns the bit length of string data or number of bits of binary data. */
case class BitLength(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "BIT_LENGTH"
  override def dataType: DataType = LongType
}

/** bit_get(expr, bit) and getbit(expr, bit) retuirns bit value at position bit in expr */
case class BitwiseGet(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "GETBIT"
  override def dataType: DataType = UnresolvedType
}

/** bround(expr, d) - Returns `expr` rounded to `d` decimal places using HALF_EVEN rounding mode. */
case class BRound(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "BROUND"
  override def dataType: DataType = DoubleType
}

/**
 * cardinality(expr) - Returns the size of an array or a map. The function returns null for null input if
 * spark.sql.legacy.sizeOfNull is set to false or spark.sql.ansi.enabled is set to true. Otherwise, the function returns
 * -1 for null input. With the default settings, the function returns -1 for null input.
 */
case class Size(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "SIZE"
  override def dataType: DataType = UnresolvedType
}

/** cbrt(expr) - Returns the cube root of `expr`. */
case class Cbrt(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "CBRT"
  override def dataType: DataType = DoubleType
}

/** ceil(expr) - Returns the smallest integer not smaller than `expr`. */
case class Ceil(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "CEIL"
  override def dataType: DataType = LongType
}

/**
 * char(expr) - Returns the ASCII character having the binary equivalent to `expr`. If n is larger than 256 the result
 * is equivalent to chr(n % 256)
 */
case class Chr(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "CHAR"
  override def dataType: DataType = StringType
}

/**
 * char_length(expr) - Returns the character length of string data or number of bytes of binary data. The length of
 * string data includes the trailing spaces. The length of binary data includes binary zeros.
 */
case class Length(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "LENGTH"
  override def dataType: DataType = LongType
}

/** coalesce(expr1, expr2, ...) - Returns the first non-null argument if exists. Otherwise, null. */
case class Coalesce(children: Seq[Expression]) extends Expression with Fn {
  override def prettyName: String = "COALESCE"
  override def dataType: DataType = UnresolvedType
}

/** concat_ws(sep[, str | array(str)]+) - Returns the concatenation of the strings separated by `sep`. */
case class ConcatWs(children: Seq[Expression]) extends Expression with Fn {
  override def prettyName: String = "CONCAT_WS"
  override def dataType: DataType = StringType
}

/** conv(num, from_base, to_base) - Convert `num` from `from_base` to `to_base`. */
case class Conv(left: Expression, right: Expression, c: Expression) extends Expression with Fn {
  override def prettyName: String = "CONV"
  override def children: Seq[Expression] = Seq(left, right, c)
  override def dataType: DataType = UnresolvedType
}

/** cos(expr) - Returns the cosine of `expr`, as if computed by `java.lang.Math.cos`. */
case class Cos(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "COS"
  override def dataType: DataType = DoubleType
}

/**
 * cosh(expr) - Returns the hyperbolic cosine of `expr`, as if computed by `java.lang.Math.cosh`.
 */
case class Cosh(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "COSH"
  override def dataType: DataType = DoubleType
}

/** cot(expr) - Returns the cotangent of `expr`, as if computed by `1/java.lang.Math.cot`. */
case class Cot(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "COT"
  override def dataType: DataType = DoubleType
}

/** crc32(expr) - Returns a cyclic redundancy check value of the `expr` as a bigint. */
case class Crc32(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "CRC32"
  override def dataType: DataType = UnresolvedType
}

/**
 * cube([col1[, col2 ..]]) - create a multi-dimensional cube using the specified columns so that we can run aggregation
 * on them.
 */
case class Cube(children: Seq[Expression]) extends Expression with Fn {
  override def prettyName: String = "CUBE"
  override def dataType: DataType = UnresolvedType
}

/** current_catalog() - Returns the current catalog. */
case class CurrentCatalog() extends LeafExpression with Fn {
  override def prettyName: String = "CURRENT_CATALOG"
  override def dataType: DataType = StringType
}

/** current_database() - Returns the current database. */
case class CurrentDatabase() extends LeafExpression with Fn {
  override def prettyName: String = "CURRENT_DATABASE"
  override def dataType: DataType = StringType
}

/** dayofmonth(date) - Returns the day of month of the date/timestamp. */
case class DayOfMonth(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "DAYOFMONTH"
  override def dataType: DataType = IntegerType
}

/** decode(bin, charset) - Decodes the first argument using the second argument character set. */
case class Decode(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "DECODE"
  override def dataType: DataType = BinaryType
}

/** degrees(expr) - Converts radians to degrees. */
case class ToDegrees(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "DEGREES"
  override def dataType: DataType = DoubleType
}

/**
 * expr1 div expr2 - Divide `expr1` by `expr2`. It returns NULL if an operand is NULL or `expr2` is 0. The result is
 * casted to long.
 */
case class IntegralDivide(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "DIV"
  override def dataType: DataType = LongType
}

/** e() - Returns Euler's number, e. */
case class EulerNumber() extends LeafExpression with Fn {
  override def prettyName: String = "E"
  override def dataType: DataType = UnresolvedType
}

/**
 * element_at(array, index) - Returns element of array at given (1-based) index. If index < 0, accesses elements from
 * the last to the first. The function returns NULL if the index exceeds the length of the array and
 * `spark.sql.ansi.enabled` is set to false. If `spark.sql.ansi.enabled` is set to true, it throws
 * ArrayIndexOutOfBoundsException for invalid indices.
 *
 * element_at(map, key) - Returns value for given key. The function returns NULL if the key is not contained in the map
 * and `spark.sql.ansi.enabled` is set to false. If `spark.sql.ansi.enabled` is set to true, it throws
 * NoSuchElementException instead.
 */
case class ElementAt(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "ELEMENT_AT"
  override def dataType: DataType = UnresolvedType
}

/**
 * elt(n, input1, input2, ...) - Returns the `n`-th input, e.g., returns `input2` when `n` is 2. The function returns
 * NULL if the index exceeds the length of the array and `spark.sql.ansi.enabled` is set to false. If
 * `spark.sql.ansi.enabled` is set to true, it throws ArrayIndexOutOfBoundsException for invalid indices.
 */
case class Elt(children: Seq[Expression]) extends Expression with Fn {
  override def prettyName: String = "ELT"
  override def dataType: DataType = UnresolvedType
}

/** encode(str, charset) - Encodes the first argument using the second argument character set. */
case class Encode(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "ENCODE"
  override def dataType: DataType = UnresolvedType
}

/** exists(expr, pred) - Tests whether a predicate holds for one or more elements in the array. */
case class ArrayExists(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "EXISTS"
  override def dataType: DataType = UnresolvedType
}

/** exp(expr) - Returns e to the power of `expr`. */
case class Exp(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "EXP"
  override def dataType: DataType = UnresolvedType
}

/**
 * explode(expr) - Separates the elements of array `expr` into multiple rows, or the elements of map `expr` into
 * multiple rows and columns. Unless specified otherwise, uses the default column name `col` for elements of the array
 * or `key` and `value` for the elements of the map.
 */
case class Explode(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "EXPLODE"
  override def dataType: DataType = UnresolvedType
}

/**
 * variant_explode(expr) - Separates the elements of a variant type `expr` into multiple rows. This function is used
 * specifically for handling variant data types, ensuring that each element is processed and outputted as a separate row.
 * The default column name for the elements is `col`.
 */
case class VariantExplode(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "VARIANT_EXPLODE"
  override def dataType: DataType = UnresolvedType
}

/**
 *  variant_explode_outer(expr) - Separates the elements of a variant type `expr` into multiple rows,
 *  including null values. This function is used specifically for handling variant data types, ensuring that
 *  each element, including nulls, is processed and outputted as a separate row. The default column name for the
 *  elements is `col`.
 */
case class VariantExplodeOuter(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "VARIANT_EXPLODE_OUTER"
  override def dataType: DataType = UnresolvedType
}

/** expm1(expr) - Returns exp(`expr`) - 1. */
case class Expm1(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "EXPM1"
  override def dataType: DataType = UnresolvedType
}

/** extract(field FROM source) - Extracts a part of the date/timestamp or interval source. */
case class Extract(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "EXTRACT"
  override def dataType: DataType = UnresolvedType
}

/** factorial(expr) - Returns the factorial of `expr`. `expr` is [0..20]. Otherwise, null. */
case class Factorial(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "FACTORIAL"
  override def dataType: DataType = UnresolvedType
}

/** filter(expr, func) - Filters the input array using the given predicate. */
case class ArrayFilter(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "FILTER"
  override def dataType: DataType = UnresolvedType
}

/**
 * find_in_set(str, str_array) - Returns the index (1-based) of the given string (`str`) in the comma-delimited list
 * (`str_array`). Returns 0, if the string was not found or if the given string (`str`) contains a comma.
 */
case class FindInSet(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "FIND_IN_SET"
  override def dataType: DataType = UnresolvedType
}

/** floor(expr) - Returns the largest integer not greater than `expr`. */
case class Floor(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "FLOOR"
  override def dataType: DataType = UnresolvedType
}

/** forall(expr, pred) - Tests whether a predicate holds for all elements in the array. */
case class ArrayForAll(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "FORALL"
  override def dataType: DataType = UnresolvedType
}

/**
 * format_number(expr1, expr2) - Formats the number `expr1` like '#,###,###.##', rounded to `expr2` decimal places. If
 * `expr2` is 0, the result has no decimal point or fractional part. `expr2` also accept a user specified format. This
 * is supposed to function like MySQL's FORMAT.
 */
case class FormatNumber(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "FORMAT_NUMBER"
  override def dataType: DataType = UnresolvedType
}

/** format_string(strfmt, obj, ...) - Returns a formatted string from printf-style format strings. */
case class FormatString(children: Seq[Expression]) extends Expression with Fn {
  override def prettyName: String = "FORMAT_STRING"
  override def dataType: DataType = UnresolvedType
}

/** from_csv(csvStr, schema[, options]) - Returns a struct value with the given `csvStr` and `schema`. */
case class CsvToStructs(left: Expression, right: Expression, c: Expression) extends Expression with Fn {
  override def prettyName: String = "FROM_CSV"
  override def children: Seq[Expression] = Seq(left, right, c)
  override def dataType: DataType = UnresolvedType
}

/** greatest(expr, ...) - Returns the greatest value of all parameters, skipping null values. */
case class Greatest(children: Seq[Expression]) extends Expression with Fn {
  override def prettyName: String = "GREATEST"
  override def dataType: DataType = UnresolvedType
}

/**
 * grouping(col) - indicates whether a specified column in a GROUP BY is aggregated or not, returns 1 for aggregated or
 * 0 for not aggregated in the result set.",
 */
case class Grouping(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "GROUPING"
  override def dataType: DataType = UnresolvedType
}

/**
 * grouping_id([col1[, col2 ..]]) - returns the level of grouping, equals to `(grouping(c1) << (n-1)) + (grouping(c2) <<
 * (n-2)) + ... + grouping(cn)`
 */
case class GroupingID(children: Seq[Expression]) extends Expression with Fn {
  override def prettyName: String = "GROUPING_ID"
  override def dataType: DataType = UnresolvedType
}

/** hash(expr1, expr2, ...) - Returns a hash value of the arguments. */
case class Murmur3Hash(children: Seq[Expression]) extends Expression with Fn {
  override def prettyName: String = "HASH"
  override def dataType: DataType = UnresolvedType
}

/** hex(expr) - Converts `expr` to hexadecimal. */
case class Hex(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "HEX"
  override def dataType: DataType = UnresolvedType
}

/** hypot(expr1, expr2) - Returns sqrt(`expr1`**2 + `expr2`**2). */
case class Hypot(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "HYPOT"
  override def dataType: DataType = UnresolvedType
}

/** if(expr1, expr2, expr3) - If `expr1` evaluates to true, then returns `expr2`; otherwise returns `expr3`. */
case class If(left: Expression, right: Expression, c: Expression) extends Expression with Fn {
  override def prettyName: String = "IF"
  override def children: Seq[Expression] = Seq(left, right, c)
  override def dataType: DataType = UnresolvedType
}

/** ifnull(expr1, expr2) - Returns `expr2` if `expr1` is null, or `expr1` otherwise. */
case class IfNull(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "IFNULL"
  override def dataType: DataType = UnresolvedType
}

/** expr1 in(expr2, expr3, ...) - Returns true if `expr` equals to any valN. */
case class In(left: Expression, other: Seq[Expression]) extends Expression with Fn {
  override def prettyName: String = "IN"
  override def children: Seq[Expression] = left +: other
  override def dataType: DataType = UnresolvedType
}

/**
 * initcap(str) - Returns `str` with the first letter of each word in uppercase. All other letters are in lowercase.
 * Words are delimited by white space.
 */
case class InitCap(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "INITCAP"
  override def dataType: DataType = UnresolvedType
}

/**
 * inline(expr) - Explodes an array of structs into a table. Uses column names col1, col2, etc. by default unless
 * specified otherwise.
 */
case class Inline(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "INLINE"
  override def dataType: DataType = UnresolvedType
}

/** input_file_block_length() - Returns the length of the block being read, or -1 if not available. */
case class InputFileBlockLength() extends LeafExpression with Fn {
  override def prettyName: String = "INPUT_FILE_BLOCK_LENGTH"
  override def dataType: DataType = UnresolvedType
}

/** input_file_block_start() - Returns the start offset of the block being read, or -1 if not available. */
case class InputFileBlockStart() extends LeafExpression with Fn {
  override def prettyName: String = "INPUT_FILE_BLOCK_START"
  override def dataType: DataType = UnresolvedType
}

/** input_file_name() - Returns the name of the file being read, or empty string if not available. */
case class InputFileName() extends LeafExpression with Fn {
  override def prettyName: String = "INPUT_FILE_NAME"
  override def dataType: DataType = UnresolvedType
}

/** instr(str, substr) - Returns the (1-based) index of the first occurrence of `substr` in `str`. */
case class StringInstr(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "INSTR"
  override def dataType: DataType = UnresolvedType
}

/** isnan(expr) - Returns true if `expr` is NaN, or false otherwise. */
case class IsNaN(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "ISNAN"
  override def dataType: DataType = UnresolvedType
}

/** java_method(class, method[, arg1[, arg2 ..]]) - Calls a method with reflection. */
case class CallMethodViaReflection(children: Seq[Expression]) extends Expression with Fn {
  override def prettyName: String = "JAVA_METHOD"
  override def dataType: DataType = UnresolvedType
}

/** lcase(str) - Returns `str` with all characters changed to lowercase. */
case class Lower(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "LOWER"
  override def dataType: DataType = UnresolvedType
}

/** least(expr, ...) - Returns the least value of all parameters, skipping null values. */
case class Least(children: Seq[Expression]) extends Expression with Fn {
  override def prettyName: String = "LEAST"
  override def dataType: DataType = UnresolvedType
}

/**
 * left(str, len) - Returns the leftmost `len`(`len` can be string type) characters from the string `str`,if `len` is
 * less or equal than 0 the result is an empty string.
 */
case class Left(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "LEFT"
  override def dataType: DataType = UnresolvedType
}

/** levenshtein(str1, str2) - Returns the Levenshtein distance between the two given strings. */
case class Levenshtein(left: Expression, right: Expression, maxDistance: Option[Expression])
    extends Expression
    with Fn {
  override def prettyName: String = "LEVENSHTEIN"
  override def children: Seq[Expression] = Seq(left, right) ++ maxDistance.toSeq
  override def dataType: DataType = UnresolvedType
}

/** ln(expr) - Returns the natural logarithm (base e) of `expr`. */
case class Log(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "LN"
  override def dataType: DataType = UnresolvedType
}

/**
 * locate(substr, str[, pos]) - Returns the position of the first occurrence of `substr` in `str` after position `pos`.
 * The given `pos` and return value are 1-based.
 */
case class StringLocate(left: Expression, right: Expression, c: Expression = Literal(1)) extends Expression with Fn {
  override def prettyName: String = "POSITION"
  override def children: Seq[Expression] = Seq(left, right, c)
  override def dataType: DataType = UnresolvedType
}

/** log(base, expr) - Returns the logarithm of `expr` with `base`. */
case class Logarithm(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "LOG"
  override def dataType: DataType = UnresolvedType
}

/** log10(expr) - Returns the logarithm of `expr` with base 10. */
case class Log10(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "LOG10"
  override def dataType: DataType = UnresolvedType
}

/** log1p(expr) - Returns log(1 + `expr`). */
case class Log1p(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "LOG1P"
  override def dataType: DataType = UnresolvedType
}

/** log2(expr) - Returns the logarithm of `expr` with base 2. */
case class Log2(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "LOG2"
  override def dataType: DataType = UnresolvedType
}

/**
 * lpad(str, len[, pad]) - Returns `str`, left-padded with `pad` to a length of `len`. If `str` is longer than `len`,
 * the return value is shortened to `len` characters. If `pad` is not specified, `str` will be padded to the left with
 * space characters.
 */
case class StringLPad(left: Expression, right: Expression, pad: Expression = Literal(" ")) extends Expression with Fn {
  override def prettyName: String = "LPAD"
  override def children: Seq[Expression] = Seq(left, right, pad)
  override def dataType: DataType = UnresolvedType
}

/** ltrim(str) - Removes the leading space characters from `str`. */
case class StringTrimLeft(left: Expression, right: Option[Expression]) extends Expression with Fn {
  override def prettyName: String = "LTRIM"
  override def children: Seq[Expression] = Seq(left) ++ right
  override def dataType: DataType = UnresolvedType
}

/**
 * make_interval(years, months, weeks, days, hours, mins, secs) - Make interval from years, months, weeks, days, hours,
 * mins and secs.
 */
case class MakeInterval(
    years: Expression,
    months: Expression,
    weeks: Expression,
    hours: Expression,
    mins: Expression,
    secs: Expression)
    extends Expression
    with Fn {
  override def prettyName: String = "MAKE_INTERVAL"
  override def children: Seq[Expression] = Seq(years, months, weeks, hours, mins, secs)
  override def dataType: DataType = UnresolvedType
}

/** map(key0, value0, key1, value1, ...) - Creates a map with the given key/value pairs. */
case class CreateMap(children: Seq[Expression], useStringTypeWhenEmpty: Boolean) extends Expression with Fn {
  override def prettyName: String = "MAP"
  override def dataType: DataType = UnresolvedType
}

/** map_filter(expr, func) - Filters entries in a map using the function. */
case class MapFilter(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "MAP_FILTER"
  override def dataType: DataType = UnresolvedType
}

/**
 * map_from_arrays(keys, values) - Creates a map with a pair of the given key/value arrays. All elements in keys should
 * not be null
 */
case class MapFromArrays(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "MAP_FROM_ARRAYS"
  override def dataType: DataType = UnresolvedType
}

/**
 * map_zip_with(map1, map2, function) - Merges two given maps into a single map by applying function to the pair of
 * values with the same key. For keys only presented in one map, NULL will be passed as the value for the missing key.
 * If an input map contains duplicated keys, only the first entry of the duplicated key is passed into the lambda
 * function.
 */
case class MapZipWith(left: Expression, right: Expression, c: Expression) extends Expression with Fn {
  override def prettyName: String = "MAP_ZIP_WITH"
  override def children: Seq[Expression] = Seq(left, right, c)
  override def dataType: DataType = UnresolvedType
}

/** md5(expr) - Returns an MD5 128-bit checksum as a hex string of `expr`. */
case class Md5(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "MD5"
  override def dataType: DataType = UnresolvedType
}

/** expr1 mod expr2 - Returns the remainder after `expr1`/`expr2`. */
case class Remainder(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "MOD"
  override def dataType: DataType = left.dataType
}

/**
 * monotonically_increasing_id() - Returns monotonically increasing 64-bit integers. The generated ID is guaranteed to
 * be monotonically increasing and unique, but not consecutive. The current implementation puts the partition ID in the
 * upper 31 bits, and the lower 33 bits represent the record number within each partition. The assumption is that the
 * data frame has less than 1 billion partitions, and each partition has less than 8 billion records. The function is
 * non-deterministic because its result depends on partition IDs.
 */
case class MonotonicallyIncreasingID() extends LeafExpression with Fn {
  override def prettyName: String = "MONOTONICALLY_INCREASING_ID"
  override def dataType: DataType = UnresolvedType
}

/** named_struct(name1, val1, name2, val2, ...) - Creates a struct with the given field names and values. */
case class CreateNamedStruct(children: Seq[Expression]) extends Expression with Fn {
  override def prettyName: String = "NAMED_STRUCT"
  override def dataType: DataType = UnresolvedType
}

/** nanvl(expr1, expr2) - Returns `expr1` if it's not NaN, or `expr2` otherwise. */
case class NaNvl(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "NANVL"
  override def dataType: DataType = UnresolvedType
}

/** negative(expr) - Returns the negated value of `expr`. */
case class UnaryMinus(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "NEGATIVE"
  override def dataType: DataType = UnresolvedType
}

/** nullif(expr1, expr2) - Returns null if `expr1` equals to `expr2`, or `expr1` otherwise. */
case class NullIf(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "NULLIF"
  override def dataType: DataType = UnresolvedType
}

/** nvl(expr1, expr2) - Returns `expr2` if `expr1` is null, or `expr1` otherwise. */
case class Nvl(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "NVL"
  override def dataType: DataType = UnresolvedType
}

/** nvl2(expr1, expr2, expr3) - Returns `expr2` if `expr1` is not null, or `expr3` otherwise. */
case class Nvl2(left: Expression, right: Expression, c: Expression) extends Expression with Fn {
  override def prettyName: String = "NVL2"
  override def children: Seq[Expression] = Seq(left, right, c)
  override def dataType: DataType = UnresolvedType
}

/** octet_length(expr) - Returns the byte length of string data or number of bytes of binary data. */
case class OctetLength(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "OCTET_LENGTH"
  override def dataType: DataType = UnresolvedType
}

/** overlay(input, replace, pos[, len]) - Replace `input` with `replace` that starts at `pos` and is of length `len`. */
case class Overlay(left: Expression, right: Expression, c: Expression, d: Expression) extends Expression with Fn {
  override def prettyName: String = "OVERLAY"
  override def children: Seq[Expression] = Seq(left, right, c, d)
  override def dataType: DataType = UnresolvedType
}

/** parse_url(url, partToExtract[, key]) - Extracts a part from a URL. */
case class ParseUrl(children: Seq[Expression]) extends Expression with Fn {
  override def prettyName: String = "PARSE_URL"
  override def dataType: DataType = UnresolvedType
}

/** pi() - Returns pi. */
case class Pi() extends LeafExpression with Fn {
  override def prettyName: String = "PI"
  override def dataType: DataType = UnresolvedType
}

/** pmod(expr1, expr2) - Returns the positive value of `expr1` mod `expr2`. */
case class Pmod(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "PMOD"
  override def dataType: DataType = UnresolvedType
}

/**
 * posexplode(expr) - Separates the elements of array `expr` into multiple rows with positions, or the elements of map
 * `expr` into multiple rows and columns with positions. Unless specified otherwise, uses the column name `pos` for
 * position, `col` for elements of the array or `key` and `value` for elements of the map.
 */
case class PosExplode(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "POSEXPLODE"
  override def dataType: DataType = UnresolvedType
}

/** positive(expr) - Returns the value of `expr`. */
case class UnaryPositive(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "POSITIVE"
  override def dataType: DataType = UnresolvedType
}

/**
 * pow(expr1, expr2) - Raises `expr1` to the power of `expr2`.
 * @see
 *   https://docs.databricks.com/en/sql/language-manual/functions/pow.html
 */
case class Pow(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "POWER" // alias: POW
  override def dataType: DataType = UnresolvedType
}

/** radians(expr) - Converts degrees to radians. */
case class ToRadians(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "RADIANS"
  override def dataType: DataType = UnresolvedType
}

/** raise_error(expr) - Throws an exception with `expr`. */
case class RaiseError(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "RAISE_ERROR"
  override def dataType: DataType = UnresolvedType
}

/**
 * rand([seed]) - Returns a random value with independent and identically distributed (i.i.d.) uniformly distributed
 * values in [0, 1).
 */
case class Rand(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "RAND"
  override def dataType: DataType = UnresolvedType
}

/**
 * randn([seed]) - Returns a random value with independent and identically distributed (i.i.d.) values drawn from the
 * standard normal distribution.
 */
case class Randn(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "RANDN"
  override def dataType: DataType = UnresolvedType
}

/**
 * regexp_extract(str, regexp[, idx]) - Extract the first string in the `str` that match the `regexp` expression and
 * corresponding to the regex group index.
 */
case class RegExpExtract(left: Expression, right: Expression, c: Expression) extends Expression with Fn {
  override def prettyName: String = "REGEXP_EXTRACT"
  override def children: Seq[Expression] = Seq(left, right, c)
  override def dataType: DataType = UnresolvedType
}

/**
 * regexp_extract_all(str, regexp[, idx]) - Extract all strings in the `str` that match the `regexp` expression and
 * corresponding to the regex group index.
 */
case class RegExpExtractAll(left: Expression, right: Expression, c: Expression) extends Expression with Fn {
  override def prettyName: String = "REGEXP_EXTRACT_ALL"
  override def children: Seq[Expression] = Seq(left, right, c)
  override def dataType: DataType = UnresolvedType
}

/** regexp_replace(str, regexp, rep[, position]) - Replaces all substrings of `str` that match `regexp` with `rep`. */
case class RegExpReplace(left: Expression, right: Expression, c: Expression, d: Option[Expression])
    extends Expression
    with Fn {
  override def prettyName: String = "REGEXP_REPLACE"
  override def children: Seq[Expression] = Seq(left, right, c) ++ d
  override def dataType: DataType = UnresolvedType
}

/** repeat(str, n) - Returns the string which repeats the given string value n times. */
case class StringRepeat(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "REPEAT"
  override def dataType: DataType = UnresolvedType
}

/** replace(str, search[, replace]) - Replaces all occurrences of `search` with `replace`. */
case class StringReplace(left: Expression, right: Expression, c: Expression) extends Expression with Fn {
  override def prettyName: String = "REPLACE"
  override def children: Seq[Expression] = Seq(left, right, c)
  override def dataType: DataType = UnresolvedType
}

/**
 * right(str, len) - Returns the rightmost `len`(`len` can be string type) characters from the string `str`,if `len` is
 * less or equal than 0 the result is an empty string.
 */
case class Right(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "RIGHT"
  override def dataType: DataType = UnresolvedType
}

/**
 * rint(expr) - Returns the double value that is closest in value to the argument and is equal to a mathematical
 * integer.
 */
case class Rint(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "RINT"
  override def dataType: DataType = UnresolvedType
}

/**
 * rollup([col1[, col2 ..]]) - create a multi-dimensional rollup using the specified columns so that we can run
 * aggregation on them.
 */
case class Rollup(children: Seq[Expression]) extends Expression with Fn {
  override def prettyName: String = "ROLLUP"
  override def dataType: DataType = UnresolvedType
}

/** round(expr, d) - Returns `expr` rounded to `d` decimal places using HALF_UP rounding mode. */
case class Round(left: Expression, right: Option[Expression]) extends Expression with Fn {
  override def children: Seq[Expression] = Seq(left) ++ right
  override def prettyName: String = "ROUND"
  override def dataType: DataType = UnresolvedType
}

/**
 * rpad(str, len[, pad]) - Returns `str`, right-padded with `pad` to a length of `len`. If `str` is longer than `len`,
 * the return value is shortened to `len` characters. If `pad` is not specified, `str` will be padded to the right with
 * space characters.
 */
case class StringRPad(left: Expression, right: Expression, c: Expression) extends Expression with Fn {
  override def prettyName: String = "RPAD"
  override def children: Seq[Expression] = Seq(left, right, c)
  override def dataType: DataType = UnresolvedType
}

/** rtrim(str) - Removes the trailing space characters from `str`. */
case class StringTrimRight(left: Expression, right: Option[Expression]) extends Expression with Fn {
  override def children: Seq[Expression] = Seq(left) ++ right
  override def prettyName: String = "RTRIM"
  override def dataType: DataType = UnresolvedType
}

/** schema_of_csv(csv[, options]) - Returns schema in the DDL format of CSV string. */
case class SchemaOfCsv(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "SCHEMA_OF_CSV"
  override def dataType: DataType = UnresolvedType
}

/** sentences(str[, lang, country]) - Splits `str` into an array of array of words. */
case class Sentences(left: Expression, right: Expression, c: Expression) extends Expression with Fn {
  override def prettyName: String = "SENTENCES"
  override def children: Seq[Expression] = Seq(left, right, c)
  override def dataType: DataType = UnresolvedType
}

/** sha(expr) - Returns a sha1 hash value as a hex string of the `expr`. */
case class Sha1(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "SHA"
  override def dataType: DataType = UnresolvedType
}

/**
 * sha2(expr, bitLength) - Returns a checksum of SHA-2 family as a hex string of `expr`. SHA-224, SHA-256, SHA-384, and
 * SHA-512 are supported. Bit length of 0 is equivalent to 256.
 */
case class Sha2(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "SHA2"
  override def dataType: DataType = UnresolvedType
}

/** shiftleft(base, expr) - Bitwise left shift. */
case class ShiftLeft(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "SHIFTLEFT"
  override def dataType: DataType = UnresolvedType
}

/** shiftright(base, expr) - Bitwise (signed) right shift. */
case class ShiftRight(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "SHIFTRIGHT"
  override def dataType: DataType = UnresolvedType
}

/** shiftrightunsigned(base, expr) - Bitwise unsigned right shift. */
case class ShiftRightUnsigned(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "SHIFTRIGHTUNSIGNED"
  override def dataType: DataType = UnresolvedType
}

/** sign(expr) - Returns -1.0, 0.0 or 1.0 as `expr` is negative, 0 or positive. */
case class Signum(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "SIGN"
  override def dataType: DataType = UnresolvedType
}

/** sin(expr) - Returns the sine of `expr`, as if computed by `java.lang.Math.sin`. */
case class Sin(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "SIN"
  override def dataType: DataType = UnresolvedType
}

/** sinh(expr) - Returns hyperbolic sine of `expr`, as if computed by `java.lang.Math.sinh`. */
case class Sinh(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "SINH"
  override def dataType: DataType = UnresolvedType
}

/** soundex(str) - Returns Soundex code of the string. */
case class SoundEx(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "SOUNDEX"
  override def dataType: DataType = UnresolvedType
}

/** space(n) - Returns a string consisting of `n` spaces. */
case class StringSpace(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "SPACE"
  override def dataType: DataType = UnresolvedType
}

/** spark_partition_id() - Returns the current partition id. */
case class SparkPartitionID() extends LeafExpression with Fn {
  override def prettyName: String = "SPARK_PARTITION_ID"
  override def dataType: DataType = UnresolvedType
}

/**
 * split(str, regex, limit) - Splits `str` around occurrences that match `regex` and returns an array with a length of
 * at most `limit`
 */
case class StringSplit(left: Expression, right: Expression, c: Option[Expression]) extends Expression with Fn {
  override def prettyName: String = "SPLIT"
  override def children: Seq[Expression] = Seq(left, right) ++ c.toSeq
  override def dataType: DataType = UnresolvedType
}

/**
 * split_part(str, delim, partNum) - Splits str around occurrences of delim and returns the partNum part.
 */
case class StringSplitPart(str: Expression, delim: Expression, partNum: Expression) extends Expression with Fn {
  override def prettyName: String = "SPLIT_PART"
  override def children: Seq[Expression] = Seq(str, delim, partNum)
  override def dataType: DataType = StringType
}

/** sqrt(expr) - Returns the square root of `expr`. */
case class Sqrt(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "SQRT"
  override def dataType: DataType = UnresolvedType
}

/**
 * stack(n, expr1, ..., exprk) - Separates `expr1`, ..., `exprk` into `n` rows. Uses column names col0, col1, etc. by
 * default unless specified otherwise.
 */
case class Stack(children: Seq[Expression]) extends Expression with Fn {
  override def prettyName: String = "STACK"
  override def dataType: DataType = UnresolvedType
}

/**
 * str_to_map(text[, pairDelim[, keyValueDelim]]) - Creates a map after splitting the text into key/value pairs using
 * delimiters. Default delimiters are ',' for `pairDelim` and ':' for `keyValueDelim`. Both `pairDelim` and
 * `keyValueDelim` are treated as regular expressions.
 */
case class StringToMap(left: Expression, right: Expression, c: Expression) extends Expression with Fn {
  override def prettyName: String = "STR_TO_MAP"
  override def children: Seq[Expression] = Seq(left, right, c)
  override def dataType: DataType = UnresolvedType
}

/**
 * substr(str, pos[, len]) - Returns the substring of `str` that starts at `pos` and is of length `len`, or the slice of
 * byte array that starts at `pos` and is of length `len`.
 *
 * substr(str FROM pos[ FOR len]]) - Returns the substring of `str` that starts at `pos` and is of length `len`, or the
 * slice of byte array that starts at `pos` and is of length `len`.
 */
case class Substring(str: Expression, pos: Expression, len: Option[Expression] = None) extends Expression with Fn {
  override def prettyName: String = "SUBSTR"
  override def children: Seq[Expression] = Seq(str, pos) ++ len.toSeq
  override def dataType: DataType = UnresolvedType
}

/**
 * substring_index(str, delim, count) - Returns the substring from `str` before `count` occurrences of the delimiter
 * `delim`. If `count` is positive, everything to the left of the final delimiter (counting from the left) is returned.
 * If `count` is negative, everything to the right of the final delimiter (counting from the right) is returned. The
 * function substring_index performs a case-sensitive match when searching for `delim`.
 */
case class SubstringIndex(left: Expression, right: Expression, c: Expression) extends Expression with Fn {
  override def prettyName: String = "SUBSTRING_INDEX"
  override def children: Seq[Expression] = Seq(left, right, c)
  override def dataType: DataType = UnresolvedType
}

/** tan(expr) - Returns the tangent of `expr`, as if computed by `java.lang.Math.tan`. */
case class Tan(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "TAN"
  override def dataType: DataType = UnresolvedType
}

/**
 * tanh(expr) - Returns the hyperbolic tangent of `expr`, as if computed by `java.lang.Math.tanh`.
 */
case class Tanh(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "TANH"
  override def dataType: DataType = UnresolvedType
}

/** to_csv(expr[, options]) - Returns a CSV string with a given struct value */
case class StructsToCsv(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "TO_CSV"
  override def dataType: DataType = UnresolvedType
}

/** transform(expr, func) - Transforms elements in an array using the function. */
case class ArrayTransform(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "TRANSFORM"
  override def dataType: DataType = UnresolvedType
}

/** transform_keys(expr, func) - Transforms elements in a map using the function. */
case class TransformKeys(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "TRANSFORM_KEYS"
  override def dataType: DataType = UnresolvedType
}

/** transform_values(expr, func) - Transforms values in the map using the function. */
case class TransformValues(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "TRANSFORM_VALUES"
  override def dataType: DataType = UnresolvedType
}

/**
 * translate(input, from, to) - Translates the `input` string by replacing the characters present in the `from` string
 * with the corresponding characters in the `to` string.
 */
case class StringTranslate(left: Expression, right: Expression, c: Expression) extends Expression with Fn {
  override def prettyName: String = "TRANSLATE"
  override def children: Seq[Expression] = Seq(left, right, c)
  override def dataType: DataType = UnresolvedType
}

/**
 * trim(str) - Removes the leading and trailing space characters from `str`.
 *
 * trim(BOTH FROM str) - Removes the leading and trailing space characters from `str`.
 *
 * trim(LEADING FROM str) - Removes the leading space characters from `str`.
 *
 * trim(TRAILING FROM str) - Removes the trailing space characters from `str`.
 *
 * trim(trimStr FROM str) - Remove the leading and trailing `trimStr` characters from `str`.
 *
 * trim(BOTH trimStr FROM str) - Remove the leading and trailing `trimStr` characters from `str`.
 *
 * trim(LEADING trimStr FROM str) - Remove the leading `trimStr` characters from `str`.
 *
 * trim(TRAILING trimStr FROM str) - Remove the trailing `trimStr` characters from `str`.
 */
case class StringTrim(left: Expression, right: Option[Expression]) extends Expression with Fn {
  override def children: Seq[Expression] = Seq(left) ++ right
  override def prettyName: String = "TRIM"
  override def dataType: DataType = UnresolvedType
}

/** typeof(expr) - Return DDL-formatted type string for the data type of the input. */
case class TypeOf(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "TYPEOF"
  override def dataType: DataType = UnresolvedType
}

/** ucase(str) - Returns `str` with all characters changed to uppercase. */
case class Upper(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "UCASE"
  override def dataType: DataType = UnresolvedType
}

/** unbase64(str) - Converts the argument from a base 64 string `str` to a binary. */
case class UnBase64(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "UNBASE64"
  override def dataType: DataType = UnresolvedType
}

/** unhex(expr) - Converts hexadecimal `expr` to binary. */
case class Unhex(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "UNHEX"
  override def dataType: DataType = UnresolvedType
}

/**
 * uuid() - Returns an universally unique identifier (UUID) string. The value is returned as a canonical UUID
 * 36-character string.
 */
case class Uuid() extends LeafExpression with Fn {
  override def prettyName: String = "UUID"
  override def dataType: DataType = UnresolvedType
}

/**
 * version() - Returns the Spark version. The string contains 2 fields, the first being a release version and the second
 * being a git revision.
 */
case class SparkVersion() extends LeafExpression with Fn {
  override def prettyName: String = "VERSION"
  override def dataType: DataType = UnresolvedType
}

/**
 * width_bucket(value, min_value, max_value, num_bucket) - Returns the bucket number to which `value` would be assigned
 * in an equiwidth histogram with `num_bucket` buckets, in the range `min_value` to `max_value`."
 */
case class WidthBucket(left: Expression, right: Expression, c: Expression, d: Expression) extends Expression with Fn {
  override def prettyName: String = "WIDTH_BUCKET"
  override def children: Seq[Expression] = Seq(left, right, c, d)
  override def dataType: DataType = UnresolvedType
}

/** N/A. */
case class TimeWindow(left: Expression, windowDuration: Long, slideDuration: Long, startTime: Long)
    extends Unary(left)
    with Fn {
  override def prettyName: String = "WINDOW"
  override def dataType: DataType = UnresolvedType
}

/** xpath(xml, xpath) - Returns a string array of values within the nodes of xml that match the XPath expression. */
case class XPathList(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "XPATH"
  override def dataType: DataType = UnresolvedType
}

/**
 * xpath_boolean(xml, xpath) - Returns true if the XPath expression evaluates to true, or if a matching node is found.
 */
case class XPathBoolean(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "XPATH_BOOLEAN"
  override def dataType: DataType = UnresolvedType
}

/**
 * xpath_double(xml, xpath) - Returns a double value, the value zero if no match is found, or NaN if a match is found
 * but the value is non-numeric.
 */
case class XPathDouble(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "XPATH_DOUBLE"
  override def dataType: DataType = UnresolvedType
}

/**
 * xpath_float(xml, xpath) - Returns a float value, the value zero if no match is found, or NaN if a match is found but
 * the value is non-numeric.
 */
case class XPathFloat(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "XPATH_FLOAT"
  override def dataType: DataType = UnresolvedType
}

/**
 * xpath_int(xml, xpath) - Returns an integer value, or the value zero if no match is found, or a match is found but the
 * value is non-numeric.
 */
case class XPathInt(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "XPATH_INT"
  override def dataType: DataType = UnresolvedType
}

/**
 * xpath_long(xml, xpath) - Returns a long integer value, or the value zero if no match is found, or a match is found
 * but the value is non-numeric.
 */
case class XPathLong(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "XPATH_LONG"
  override def dataType: DataType = UnresolvedType
}

/**
 * xpath_short(xml, xpath) - Returns a short integer value, or the value zero if no match is found, or a match is found
 * but the value is non-numeric.
 */
case class XPathShort(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "XPATH_SHORT"
  override def dataType: DataType = UnresolvedType
}

/** xpath_string(xml, xpath) - Returns the text contents of the first xml node that matches the XPath expression. */
case class XPathString(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "XPATH_STRING"
  override def dataType: DataType = UnresolvedType
}

/** xxhash64(expr1, expr2, ...) - Returns a 64-bit hash value of the arguments. */
case class XxHash64(children: Seq[Expression]) extends Expression with Fn {
  override def prettyName: String = "XXHASH64"
  override def dataType: DataType = UnresolvedType
}

/**
 * zip_with(left, right, func) - Merges the two given arrays, element-wise, into a single array using function. If one
 * array is shorter, nulls are appended at the end to match the length of the longer array, before applying function.
 */
case class ZipWith(left: Expression, right: Expression, c: Expression) extends Expression with Fn {
  override def prettyName: String = "ZIP_WITH"
  override def children: Seq[Expression] = Seq(left, right, c)
  override def dataType: DataType = UnresolvedType
}

/** any(expr) - Returns true if at least one value of `expr` is true. */
case class BoolOr(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "ANY"
  override def dataType: DataType = UnresolvedType
}

/**
 * approx_count_distinct(expr[, relativeSD]) - Returns the estimated cardinality by HyperLogLog++. `relativeSD` defines
 * the maximum relative standard deviation allowed.
 */
case class HyperLogLogPlusPlus(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "APPROX_COUNT_DISTINCT"
  override def dataType: DataType = UnresolvedType
}

/** avg(expr) - Returns the mean calculated from values of a group. */
case class Average(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "AVG"
  override def dataType: DataType = UnresolvedType
}

/** bit_and(expr) - Returns the bitwise AND of all non-null input values, or null if none. */
case class BitAndAgg(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "BIT_AND"
  override def dataType: DataType = UnresolvedType
}

/** bit_or(expr) - Returns the bitwise OR of all non-null input values, or null if none. */
case class BitOrAgg(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "BIT_OR"
  override def dataType: DataType = UnresolvedType
}

/** bit_xor(expr) - Returns the bitwise XOR of all non-null input values, or null if none. */
case class BitXorAgg(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "BIT_XOR"
  override def dataType: DataType = UnresolvedType
}

/** bool_and(expr) - Returns true if all values of `expr` are true. */
case class BoolAnd(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "BOOL_AND"
  override def dataType: DataType = UnresolvedType
}

/** collect_list(expr) - Collects and returns a list of non-unique elements. */
case class CollectList(expr: Expression, cond: Option[Expression] = None) extends Expression with Fn {
  // COLLECT_LIST and ARRAY_AGG are synonyms, but ARRAY_AGG is used in the test examples
  override def prettyName: String = "ARRAY_AGG"
  override def dataType: DataType = UnresolvedType
  override def children: Seq[Expression] = Seq(expr) ++ cond.toSeq
}

/** collect_set(expr) - Collects and returns a set of unique elements. */
case class CollectSet(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "COLLECT_SET"
  override def dataType: DataType = UnresolvedType
}

/** corr(expr1, expr2) - Returns Pearson coefficient of correlation between a set of number pairs. */
case class Corr(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "CORR"
  override def dataType: DataType = UnresolvedType
}

/**
 * count(*) - Returns the total number of retrieved rows, including rows containing null.
 *
 * count(expr[, expr...]) - Returns the number of rows for which the supplied expression(s) are all non-null.
 *
 * count(DISTINCT expr[, expr...]) - Returns the number of rows for which the supplied expression(s) are unique and
 * non-null.
 */
case class Count(children: Seq[Expression]) extends Expression with Fn {
  override def prettyName: String = "COUNT"
  override def dataType: DataType = UnresolvedType
}

/** count_if(expr) - Returns the number of `TRUE` values for the expression. */
case class CountIf(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "COUNT_IF"
  override def dataType: DataType = UnresolvedType
}

/**
 * count_min_sketch(col, eps, confidence, seed) - Returns a count-min sketch of a column with the given esp, confidence
 * and seed. The result is an array of bytes, which can be deserialized to a `CountMinSketch` before usage. Count-min
 * sketch is a probabilistic data structure used for cardinality estimation using sub-linear space.
 */
case class CountMinSketchAgg(left: Expression, right: Expression, c: Expression, d: Expression)
    extends Expression
    with Fn {
  override def prettyName: String = "COUNT_MIN_SKETCH"
  override def children: Seq[Expression] = Seq(left, right, c, d)
  override def dataType: DataType = UnresolvedType
}

/** covar_pop(expr1, expr2) - Returns the population covariance of a set of number pairs. */
case class CovPopulation(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "COVAR_POP"
  override def dataType: DataType = UnresolvedType
}

/** covar_samp(expr1, expr2) - Returns the sample covariance of a set of number pairs. */
case class CovSample(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "COVAR_SAMP"
  override def dataType: DataType = UnresolvedType
}

/**
 * first(expr[, isIgnoreNull]) - Returns the first value of `expr` for a group of rows. If `isIgnoreNull` is true,
 * returns only non-null values.
 */
case class First(left: Expression, right: Option[Expression] = None) extends Expression with Fn {
  override def children: Seq[Expression] = Seq(left) ++ right
  override def prettyName: String = "FIRST"
  override def dataType: DataType = UnresolvedType
}

/** kurtosis(expr) - Returns the kurtosis value calculated from values of a group. */
case class Kurtosis(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "KURTOSIS"
  override def dataType: DataType = UnresolvedType
}

/**
 * last(expr[, isIgnoreNull]) - Returns the last value of `expr` for a group of rows. If `isIgnoreNull` is true, returns
 * only non-null values
 */
case class Last(left: Expression, right: Option[Expression] = None) extends Expression with Fn {
  override def children: Seq[Expression] = Seq(left) ++ right
  override def prettyName: String = "LAST"
  override def dataType: DataType = UnresolvedType
}

/** max(expr) - Returns the maximum value of `expr`. */
case class Max(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "MAX"
  override def dataType: DataType = UnresolvedType
}

/** max_by(x, y) - Returns the value of `x` associated with the maximum value of `y`. */
case class MaxBy(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "MAX_BY"
  override def dataType: DataType = UnresolvedType
}

/** min(expr) - Returns the minimum value of `expr`. */
case class Min(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "MIN"
  override def dataType: DataType = UnresolvedType
}

/** min_by(x, y) - Returns the value of `x` associated with the minimum value of `y`. */
case class MinBy(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "MIN_BY"
  override def dataType: DataType = UnresolvedType
}

/**
 * percentile(col, percentage [, frequency]) - Returns the exact percentile value of numeric column `col` at the given
 * percentage. The value of percentage must be between 0.0 and 1.0. The value of frequency should be positive integral
 *
 * percentile(col, array(percentage1 [, percentage2]...) [, frequency]) - Returns the exact percentile value array of
 * numeric column `col` at the given percentage(s). Each value of the percentage array must be between 0.0 and 1.0. The
 * value of frequency should be positive integral
 */
case class Percentile(left: Expression, right: Expression, c: Expression) extends Expression with Fn {
  override def prettyName: String = "PERCENTILE"
  override def children: Seq[Expression] = Seq(left, right, c)
  override def dataType: DataType = UnresolvedType
}

/**
 * percentile_approx(col, percentage [, accuracy]) - Returns the approximate `percentile` of the numeric column `col`
 * which is the smallest value in the ordered `col` values (sorted from least to greatest) such that no more than
 * `percentage` of `col` values is less than the value or equal to that value. The value of percentage must be between
 * 0.0 and 1.0. The `accuracy` parameter (default: 10000) is a positive numeric literal which controls approximation
 * accuracy at the cost of memory. Higher value of `accuracy` yields better accuracy, `1.0/accuracy` is the relative
 * error of the approximation. When `percentage` is an array, each value of the percentage array must be between 0.0 and
 * 1.0. In this case, returns the approximate percentile array of column `col` at the given percentage array.
 */
case class ApproximatePercentile(left: Expression, right: Expression, c: Expression) extends Expression with Fn {
  override def prettyName: String = "PERCENTILE_APPROX"
  override def children: Seq[Expression] = Seq(left, right, c)
  override def dataType: DataType = UnresolvedType
}

/** skewness(expr) - Returns the skewness value calculated from values of a group. */
case class Skewness(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "SKEWNESS"
  override def dataType: DataType = UnresolvedType
}

/** std(expr) - Returns the sample standard deviation calculated from values of a group. */
case class StdSamp(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "STD"
  override def dataType: DataType = UnresolvedType
}

/** stddev(expr) - Returns the sample standard deviation calculated from values of a group. */
case class StddevSamp(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "STDDEV"
  override def dataType: DataType = UnresolvedType
}

/** stddev_pop(expr) - Returns the population standard deviation calculated from values of a group. */
case class StddevPop(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "STDDEV_POP"
  override def dataType: DataType = UnresolvedType
}

/** sum(expr) - Returns the sum calculated from values of a group. */
case class Sum(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "SUM"
  override def dataType: DataType = UnresolvedType
}

/** var_pop(expr) - Returns the population variance calculated from values of a group. */
case class VariancePop(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "VAR_POP"
  override def dataType: DataType = UnresolvedType
}

/** var_samp(expr) - Returns the sample variance calculated from values of a group. */
case class VarianceSamp(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "VAR_SAMP"
  override def dataType: DataType = UnresolvedType
}

/** array_contains(array, value) - Returns true if the array contains the value. */
case class ArrayContains(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "ARRAY_CONTAINS"
  override def dataType: DataType = UnresolvedType
}

/** array_distinct(array) - Removes duplicate values from the array. */
case class ArrayDistinct(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "ARRAY_DISTINCT"
  override def dataType: DataType = UnresolvedType
}

/**
 * array_except(array1, array2) - Returns an array of the elements in array1 but not in array2, without duplicates.
 */
case class ArrayExcept(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "ARRAY_EXCEPT"
  override def dataType: DataType = UnresolvedType
}

/**
 * array_intersect(array1, array2) - Returns an array of the elements in the intersection of array1 and array2, without
 * duplicates.
 */
case class ArrayIntersect(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "ARRAY_INTERSECT"
  override def dataType: DataType = UnresolvedType
}

/**
 * array_join(array, delimiter[, nullReplacement]) - Concatenates the elements of the given array using the delimiter
 * and an optional string to replace nulls. If no value is set for nullReplacement, any null value is filtered.
 */
case class ArrayJoin(left: Expression, right: Expression, c: Option[Expression] = None) extends Expression with Fn {
  override def prettyName: String = "ARRAY_JOIN"
  override def children: Seq[Expression] = Seq(left, right) ++ c.toSeq
  override def dataType: DataType = UnresolvedType
}

/** array_max(array) - Returns the maximum value in the array. NULL elements are skipped. */
case class ArrayMax(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "ARRAY_MAX"
  override def dataType: DataType = UnresolvedType
}

/** array_min(array) - Returns the minimum value in the array. NULL elements are skipped. */
case class ArrayMin(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "ARRAY_MIN"
  override def dataType: DataType = UnresolvedType
}

/** array_position(array, element) - Returns the (1-based) index of the first element of the array as long. */
case class ArrayPosition(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "ARRAY_POSITION"
  override def dataType: DataType = UnresolvedType
}

/** array_remove(array, element) - Remove all elements that equal to element from array. */
case class ArrayRemove(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "ARRAY_REMOVE"
  override def dataType: DataType = UnresolvedType
}

/** array_repeat(element, count) - Returns the array containing element count times. */
case class ArrayRepeat(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "ARRAY_REPEAT"
  override def dataType: DataType = UnresolvedType
}

/**
 * array_union(array1, array2) - Returns an array of the elements in the union of array1 and array2, without duplicates.
 */
case class ArrayUnion(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "ARRAY_UNION"
  override def dataType: DataType = UnresolvedType
}

/**
 * arrays_overlap(a1, a2) - Returns true if a1 contains at least a non-null element present also in a2. If the arrays
 * have no common element and they are both non-empty and either of them contains a null element null is returned, false
 * otherwise.
 */
case class ArraysOverlap(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "ARRAYS_OVERLAP"
  override def dataType: DataType = UnresolvedType
}

/**
 * arrays_zip(a1, a2, ...) - Returns a merged array of structs in which the N-th struct contains all N-th values of
 * input arrays.
 */
case class ArraysZip(children: Seq[Expression]) extends Expression with Fn {
  override def prettyName: String = "ARRAYS_ZIP"
  override def dataType: DataType = UnresolvedType
}

/** concat(col1, col2, ..., colN) - Returns the concatenation of col1, col2, ..., colN. */
case class Concat(children: Seq[Expression]) extends Expression with Fn {
  override def prettyName: String = "CONCAT"
  override def dataType: DataType = UnresolvedType
}

/** flatten(arrayOfArrays) - Transforms an array of arrays into a single array. */
case class Flatten(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "FLATTEN"
  override def dataType: DataType = UnresolvedType
}

/** reverse(array) - Returns a reversed string or an array with reverse order of elements. */
case class Reverse(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "REVERSE"
  override def dataType: DataType = UnresolvedType
}

/**
 * sequence(start, stop, step) - Generates an array of elements from start to stop (inclusive), incrementing by step.
 * The type of the returned elements is the same as the type of argument expressions.
 *
 * Supported types are: byte, short, integer, long, date, timestamp.
 *
 * The start and stop expressions must resolve to the same type. If start and stop expressions resolve to the 'date' or
 * 'timestamp' type then the step expression must resolve to the 'interval' type, otherwise to the same type as the
 * start and stop expressions.
 */
case class Sequence(left: Expression, right: Expression, c: Expression) extends Expression with Fn {
  override def prettyName: String = "SEQUENCE"
  override def children: Seq[Expression] = Seq(left, right, c)
  override def dataType: DataType = UnresolvedType
}

/** shuffle(array) - Returns a random permutation of the given array. */
case class Shuffle(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "SHUFFLE"
  override def dataType: DataType = UnresolvedType
}

/**
 * slice(x, start, length) - Subsets array x starting from index start (array indices start at 1, or starting from the
 * end if start is negative) with the specified length.
 */
case class Slice(left: Expression, right: Expression, c: Expression) extends Expression with Fn {
  override def prettyName: String = "SLICE"
  override def children: Seq[Expression] = Seq(left, right, c)
  override def dataType: DataType = UnresolvedType
}

/**
 * sort_array(array[, ascendingOrder]) - Sorts the input array in ascending or descending order according to the natural
 * ordering of the array elements. Null elements will be placed at the beginning of the returned array in ascending
 * order or at the end of the returned array in descending order.
 */
case class SortArray(left: Expression, right: Option[Expression] = None) extends Expression with Fn {
  override def prettyName: String = "SORT_ARRAY"
  override def children: Seq[Expression] = Seq(left) ++ right.toSeq
  override def dataType: DataType = UnresolvedType
}

/** add_months(start_date, num_months) - Returns the date that is `num_months` after `start_date`. */
case class AddMonths(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "ADD_MONTHS"
  override def dataType: DataType = UnresolvedType
}

/**
 * current_date() - Returns the current date at the start of query evaluation. All calls of current_date within the same
 * query return the same value.
 *
 * current_date - Returns the current date at the start of query evaluation.
 */
case class CurrentDate() extends LeafExpression with Fn {
  override def prettyName: String = "CURRENT_DATE"
  override def dataType: DataType = UnresolvedType
}

/**
 * current_timestamp() - Returns the current timestamp at the start of query evaluation. All calls of current_timestamp
 * within the same query return the same value.
 *
 * current_timestamp - Returns the current timestamp at the start of query evaluation.
 */
case class CurrentTimestamp() extends LeafExpression with Fn {
  override def prettyName: String = "CURRENT_TIMESTAMP"
  override def dataType: DataType = UnresolvedType
}

/** current_timezone() - Returns the current session local timezone. */
case class CurrentTimeZone() extends LeafExpression with Fn {
  override def prettyName: String = "CURRENT_TIMEZONE"
  override def dataType: DataType = UnresolvedType
}

/** date_add(start_date, num_days) - Returns the date that is `num_days` after `start_date`. */
case class DateAdd(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "DATE_ADD"
  override def dataType: DataType = UnresolvedType
}

/**
 * date_format(timestamp, fmt) - Converts `timestamp` to a value of string in the format specified by the date format
 * `fmt`.
 */
case class DateFormatClass(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "DATE_FORMAT"
  override def dataType: DataType = UnresolvedType
}

/** date_from_unix_date(days) - Create date from the number of days since 1970-01-01. */
case class DateFromUnixDate(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "DATE_FROM_UNIX_DATE"
  override def dataType: DataType = UnresolvedType
}

/** date_part(field, source) - Extracts a part of the date/timestamp or interval source. */
case class DatePart(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "DATE_PART"
  override def dataType: DataType = UnresolvedType
}

/** date_sub(start_date, num_days) - Returns the date that is `num_days` before `start_date`. */
case class DateSub(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "DATE_SUB"
  override def dataType: DataType = UnresolvedType
}

/** date_trunc(fmt, ts) - Returns timestamp `ts` truncated to the unit specified by the format model `fmt`. */
case class TruncTimestamp(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "DATE_TRUNC"
  override def dataType: DataType = UnresolvedType
}

/** datediff(endDate, startDate) - Returns the number of days from `startDate` to `endDate`. */
case class DateDiff(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "DATEDIFF"
  override def dataType: DataType = UnresolvedType
}

/** datediff(units, start, end) - Returns the difference between two timestamps measured in `units`. */
case class TimestampDiff(unit: String, start: Expression, end: Expression, timeZoneId: Option[String] = None)
    extends Binary(start, end)
    with Fn {
  // TIMESTAMPDIFF and DATEDIFF are synonyms, but DATEDIFF is used in the example queries, so we stick to it for now.
  override def prettyName: String = "DATEDIFF"
  override def dataType: DataType = UnresolvedType
}

/** dayofweek(date) - Returns the day of the week for date/timestamp (1 = Sunday, 2 = Monday, ..., 7 = Saturday). */
case class DayOfWeek(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "DAYOFWEEK"
  override def dataType: DataType = UnresolvedType
}

/** dayofyear(date) - Returns the day of year of the date/timestamp. */
case class DayOfYear(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "DAYOFYEAR"
  override def dataType: DataType = UnresolvedType
}

/** from_unixtime(unix_time[, fmt]) - Returns `unix_time` in the specified `fmt`. */
case class FromUnixTime(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "FROM_UNIXTIME"
  override def dataType: DataType = UnresolvedType
}

/**
 * from_utc_timestamp(timestamp, timezone) - Given a timestamp like '2017-07-14 02:40:00.0', interprets it as a time in
 * UTC, and renders that time as a timestamp in the given time zone. For example, 'GMT+1' would yield '2017-07-14
 * 03:40:00.0'.
 */
case class FromUTCTimestamp(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "FROM_UTC_TIMESTAMP"
  override def dataType: DataType = UnresolvedType
}

/** hour(timestamp) - Returns the hour component of the string/timestamp. */
case class Hour(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "HOUR"
  override def dataType: DataType = UnresolvedType
}

/** last_day(date) - Returns the last day of the month which the date belongs to. */
case class LastDay(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "LAST_DAY"
  override def dataType: DataType = UnresolvedType
}

/** make_date(year, month, day) - Create date from year, month and day fields. */
case class MakeDate(left: Expression, right: Expression, c: Expression) extends Expression with Fn {
  override def prettyName: String = "MAKE_DATE"
  override def children: Seq[Expression] = Seq(left, right, c)
  override def dataType: DataType = UnresolvedType
}

/**
 * make_timestamp(year, month, day, hour, min, sec[, timezone]) - Create timestamp from year, month, day, hour, min, sec
 * and timezone fields.
 */
case class MakeTimestamp(
    left: Expression,
    right: Expression,
    c: Expression,
    d: Expression,
    e: Expression,
    f: Expression,
    g: Option[Expression])
    extends Expression
    with Fn {
  override def prettyName: String = "MAKE_TIMESTAMP"
  override def children: Seq[Expression] = Seq(left, right, c, d, e, f) ++ g.toSeq
  override def dataType: DataType = UnresolvedType
}

/** minute(timestamp) - Returns the minute component of the string/timestamp. */
case class Minute(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "MINUTE"
  override def dataType: DataType = UnresolvedType
}

/** month(date) - Returns the month component of the date/timestamp. */
case class Month(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "MONTH"
  override def dataType: DataType = UnresolvedType
}

/**
 * months_between(timestamp1, timestamp2[, roundOff]) - If `timestamp1` is later than `timestamp2`, then the result is
 * positive. If `timestamp1` and `timestamp2` are on the same day of month, or both are the last day of month, time of
 * day will be ignored. Otherwise, the difference is calculated based on 31 days per month, and rounded to 8 digits
 * unless roundOff=false.
 */
case class MonthsBetween(left: Expression, right: Expression, c: Expression) extends Expression with Fn {
  override def prettyName: String = "MONTHS_BETWEEN"
  override def children: Seq[Expression] = Seq(left, right, c)
  override def dataType: DataType = UnresolvedType
}

/**
 * next_day(start_date, day_of_week) - Returns the first date which is later than `start_date` and named as indicated.
 */
case class NextDay(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "NEXT_DAY"
  override def dataType: DataType = UnresolvedType
}

/** now() - Returns the current timestamp at the start of query evaluation. */
case class Now() extends LeafExpression with Fn {
  override def prettyName: String = "NOW"
  override def dataType: DataType = UnresolvedType
}

/** quarter(date) - Returns the quarter of the year for date, in the range 1 to 4. */
case class Quarter(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "QUARTER"
  override def dataType: DataType = UnresolvedType
}

/** second(timestamp) - Returns the second component of the string/timestamp. */
case class Second(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "SECOND"
  override def dataType: DataType = UnresolvedType
}

/** timestamp_micros(microseconds) - Creates timestamp from the number of microseconds since UTC epoch. */
case class MicrosToTimestamp(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "TIMESTAMP_MICROS"
  override def dataType: DataType = UnresolvedType
}

/** timestamp_millis(milliseconds) - Creates timestamp from the number of milliseconds since UTC epoch. */
case class MillisToTimestamp(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "TIMESTAMP_MILLIS"
  override def dataType: DataType = UnresolvedType
}

/** timestamp_seconds(seconds) - Creates timestamp from the number of seconds (can be fractional) since UTC epoch. */
case class SecondsToTimestamp(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "TIMESTAMP_SECONDS"
  override def dataType: DataType = UnresolvedType
}

/**
 * to_date(date_str[, fmt]) - Parses the `date_str` expression with the `fmt` expression to a date. Returns null with
 * invalid input. By default, it follows casting rules to a date if the `fmt` is omitted.
 */
case class ParseToDate(left: Expression, right: Option[Expression]) extends Expression with Fn {
  override def prettyName: String = "TO_DATE"
  override def children: Seq[Expression] = Seq(left) ++ right.toSeq
  override def dataType: DataType = UnresolvedType
}

/**
 * to_timestamp(timestamp_str[, fmt]) - Parses the `timestamp_str` expression with the `fmt` expression to a timestamp.
 * Returns null with invalid input. By default, it follows casting rules to a timestamp if the `fmt` is omitted.
 */
case class ParseToTimestamp(left: Expression, right: Option[Expression] = None) extends Expression with Fn {
  override def prettyName: String = "TO_TIMESTAMP"
  override def dataType: DataType = UnresolvedType
  override def children: Seq[Expression] = Seq(left) ++ right.toSeq
}

/** to_unix_timestamp(timeExp[, fmt]) - Returns the UNIX timestamp of the given time. */
case class ToUnixTimestamp(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "TO_UNIX_TIMESTAMP"
  override def dataType: DataType = UnresolvedType
}

/**
 * to_utc_timestamp(timestamp, timezone) - Given a timestamp like '2017-07-14 02:40:00.0', interprets it as a time in
 * the given time zone, and renders that time as a timestamp in UTC. For example, 'GMT+1' would yield '2017-07-14
 * 01:40:00.0'.
 */
case class ToUTCTimestamp(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "TO_UTC_TIMESTAMP"
  override def dataType: DataType = UnresolvedType
}

/**
 * trunc(date, fmt) - Returns `date` with the time portion of the day truncated to the unit specified by the format
 * model `fmt`.
 */
case class TruncDate(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "TRUNC"
  override def dataType: DataType = UnresolvedType
}

/** unix_date(date) - Returns the number of days since 1970-01-01. */
case class UnixDate(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "UNIX_DATE"
  override def dataType: DataType = UnresolvedType
}

/** unix_micros(timestamp) - Returns the number of microseconds since 1970-01-01 00:00:00 UTC. */
case class UnixMicros(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "UNIX_MICROS"
  override def dataType: DataType = UnresolvedType
}

/**
 * unix_millis(timestamp) - Returns the number of milliseconds since 1970-01-01 00:00:00 UTC. Truncates higher levels of
 * precision.
 */
case class UnixMillis(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "UNIX_MILLIS"
  override def dataType: DataType = UnresolvedType
}

/**
 * unix_seconds(timestamp) - Returns the number of seconds since 1970-01-01 00:00:00 UTC. Truncates higher levels of
 * precision.
 */
case class UnixSeconds(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "UNIX_SECONDS"
  override def dataType: DataType = UnresolvedType
}

/** unix_timestamp([timeExp[, fmt]]) - Returns the UNIX timestamp of current or specified time. */
case class UnixTimestamp(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "UNIX_TIMESTAMP"
  override def dataType: DataType = UnresolvedType
}

/** weekday(date) - Returns the day of the week for date/timestamp (0 = Monday, 1 = Tuesday, ..., 6 = Sunday). */
case class WeekDay(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "WEEKDAY"
  override def dataType: DataType = UnresolvedType
}

/**
 * weekofyear(date) - Returns the week of the year of the given date. A week is considered to start on a Monday and week
 * 1 is the first week with >3 days.
 */
case class WeekOfYear(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "WEEKOFYEAR"
  override def dataType: DataType = UnresolvedType
}

/** year(date) - Returns the year component of the date/timestamp. */
case class Year(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "YEAR"
  override def dataType: DataType = UnresolvedType
}

/** from_json(jsonStr, schema[, options]) - Returns a struct value with the given `jsonStr` and `schema`. */
case class JsonToStructs(left: Expression, right: Expression, c: Option[Expression]) extends Expression with Fn {
  override def prettyName: String = "FROM_JSON"
  override def children: Seq[Expression] = Seq(left, right) ++ c
  override def dataType: DataType = UnresolvedType
}

/** get_json_object(json_txt, path) - Extracts a json object from `path`. */
case class GetJsonObject(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "GET_JSON_OBJECT"
  override def dataType: DataType = UnresolvedType
}

/** json_array_length(jsonArray) - Returns the number of elements in the outmost JSON array. */
case class LengthOfJsonArray(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "JSON_ARRAY_LENGTH"
  override def dataType: DataType = UnresolvedType
}

/** json_object_keys(json_object) - Returns all the keys of the outmost JSON object as an array. */
case class JsonObjectKeys(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "JSON_OBJECT_KEYS"
  override def dataType: DataType = UnresolvedType
}

/**
 * json_tuple(jsonStr, p1, p2, ..., pn) - Returns a tuple like the function get_json_object, but it takes multiple
 * names. All the input parameters and output column types are string.
 */
case class JsonTuple(children: Seq[Expression]) extends Expression with Fn {
  override def prettyName: String = "JSON_TUPLE"
  override def dataType: DataType = UnresolvedType
}

/** schema_of_json(json[, options]) - Returns schema in the DDL format of JSON string. */
case class SchemaOfJson(left: Expression, right: Expression) extends Binary(left, right) with Fn {
  override def prettyName: String = "SCHEMA_OF_JSON"
  override def dataType: DataType = UnresolvedType
}

/** to_json(expr[, options]) - Returns a JSON string with a given struct value */
case class StructsToJson(left: Expression, right: Option[Expression]) extends Expression with Fn {
  override def prettyName: String = "TO_JSON"
  override def children: Seq[Expression] = Seq(left) ++ right.toSeq
  override def dataType: DataType = UnresolvedType
}

/** map_concat(map, ...) - Returns the union of all the given maps */
case class MapConcat(children: Seq[Expression]) extends Expression with Fn {
  override def prettyName: String = "MAP_CONCAT"
  override def dataType: DataType = UnresolvedType
}

/** map_entries(map) - Returns an unordered array of all entries in the given map. */
case class MapEntries(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "MAP_ENTRIES"
  override def dataType: DataType = UnresolvedType
}

/** map_from_entries(arrayOfEntries) - Returns a map created from the given array of entries. */
case class MapFromEntries(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "MAP_FROM_ENTRIES"
  override def dataType: DataType = UnresolvedType
}

/** map_keys(map) - Returns an unordered array containing the keys of the map. */
case class MapKeys(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "MAP_KEYS"
  override def dataType: DataType = UnresolvedType
}

/** map_values(map) - Returns an unordered array containing the values of the map. */
case class MapValues(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "MAP_VALUES"
  override def dataType: DataType = UnresolvedType
}

/** cume_dist() - Computes the position of a value relative to all values in the partition. */
case class CumeDist() extends LeafExpression with Fn {
  override def prettyName: String = "CUME_DIST"
  override def dataType: DataType = UnresolvedType
}

/**
 * dense_rank() - Computes the rank of a value in a group of values. The result is one plus the previously assigned rank
 * value. Unlike the function rank, dense_rank will not produce gaps in the ranking sequence.
 */
case class DenseRank(children: Seq[Expression]) extends Expression with Fn {
  override def prettyName: String = "DENSE_RANK"
  override def dataType: DataType = UnresolvedType
}

/**
 * lag(input[, offset[, default]]) - Returns the value of `input` at the `offset`th row before the current row in the
 * window. The default value of `offset` is 1 and the default value of `default` is null. If the value of `input` at the
 * `offset`th row is null, null is returned. If there is no such offset row (e.g., when the offset is 1, the first row
 * of the window does not have any previous row), `default` is returned.
 */
case class Lag(left: Expression, offset: Option[Expression] = None, default: Option[Expression] = None)
    extends Expression
    with Fn {
  override def prettyName: String = "LAG"
  override def children: Seq[Expression] = Seq(left) ++ offset ++ default
  override def dataType: DataType = left.dataType
}

/**
 * lead(input[, offset[, default]]) - Returns the value of `input` at the `offset`th row after the current row in the
 * window. The default value of `offset` is 1 and the default value of `default` is null. If the value of `input` at the
 * `offset`th row is null, null is returned. If there is no such an offset row (e.g., when the offset is 1, the last row
 * of the window does not have any subsequent row), `default` is returned.
 */
case class Lead(left: Expression, offset: Option[Expression] = None, default: Option[Expression] = None)
    extends Expression
    with Fn {
  override def children: Seq[Expression] = Seq(left) ++ offset ++ default
  override def prettyName: String = "LEAD"
  override def dataType: DataType = left.dataType
}

/**
 * nth_value(input[, offset]) - Returns the value of `input` at the row that is the `offset`th row from beginning of the
 * window frame. Offset starts at 1. If ignoreNulls=true, we will skip nulls when finding the `offset`th row. Otherwise,
 * every row counts for the `offset`. If there is no such an `offset`th row (e.g., when the offset is 10, size of the
 * window frame is less than 10), null is returned.
 */
case class NthValue(input: Expression, offset: Expression = Literal(1), ignoreNulls: Option[Expression] = None)
    extends Expression
    with Fn {
  override def children: Seq[Expression] = Seq(input, offset) ++ ignoreNulls
  override def prettyName: String = "NTH_VALUE"
  override def dataType: DataType = input.dataType
}

/**
 * ntile(n) - Divides the rows for each window partition into `n` buckets ranging from 1 to at most `n`.
 */
case class NTile(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "NTILE"
  override def dataType: DataType = UnresolvedType
}

/** percent_rank() - Computes the percentage ranking of a value in a group of values. */
case class PercentRank(children: Seq[Expression]) extends Expression with Fn {
  override def prettyName: String = "PERCENT_RANK"
  override def dataType: DataType = UnresolvedType
}

/**
 * rank() - Computes the rank of a value in a group of values. The result is one plus the number of rows preceding or
 * equal to the current row in the ordering of the partition. The values will produce gaps in the sequence.
 */
case class Rank(children: Seq[Expression]) extends Expression with Fn {
  override def prettyName: String = "RANK"
  override def dataType: DataType = UnresolvedType
}

/**
 * row_number() - Assigns a unique, sequential number to each row, starting with one, according to the ordering of rows
 * within the window partition.
 */
case class RowNumber() extends LeafExpression with Fn {
  override def prettyName: String = "ROW_NUMBER"
  override def dataType: DataType = UnresolvedType
}

/**
 * to_number(expr, fmt) - Returns expr cast to DECIMAL using formatting fmt
 */
case class ToNumber(expr: Expression, fmt: Expression) extends Binary(expr, fmt) with Fn {
  override def prettyName: String = "TO_NUMBER"
  override def dataType: DataType = UnresolvedType
}

/**
 * try_to_number(expr, fmt) - Returns expr cast to DECIMAL using formatting fmt, or NULL if expr does not match the
 * format.
 */
case class TryToNumber(expr: Expression, fmt: Expression) extends Binary(expr, fmt) with Fn {
  override def prettyName: String = "TRY_TO_NUMBER"
  override def dataType: DataType = UnresolvedType
}

/**
 * try_to_timestamp(expr, fmt) - Returns expr cast to a timestamp using an optional formatting, or NULL if the cast
 * fails.
 */
case class TryToTimestamp(expr: Expression, fmt: Option[Expression] = None) extends Expression with Fn {
  override def prettyName: String = "TRY_TO_TIMESTAMP"
  override def dataType: DataType = TimestampType
  override def children: Seq[Expression] = Seq(expr) ++ fmt.toSeq
}

/**
 * timestampadd(unit, value, expr) - Adds value units to a timestamp expr
 */
case class TimestampAdd(unit: String, quantity: Expression, timestamp: Expression) extends Expression with Fn {
  // TIMESTAMPADD, DATE_ADD and DATEADD are synonyms, but the latter is used in the examples.
  override def prettyName: String = "DATEADD"
  override def children: Seq[Expression] = Seq(quantity, timestamp)
  override def dataType: DataType = TimestampType
}

/**
 * try_cast(sourceExpr AS targetType) - Returns the value of sourceExpr cast to data type targetType if possible, or
 * NULL if not possible.
 */
case class TryCast(expr: Expression, override val dataType: DataType) extends Expression {
  override def children: Seq[Expression] = Seq(expr)
}

/**
 * parse_json(expr) - Parses the JSON string `expr` and returns the resulting structure.
 */
case class ParseJson(left: Expression) extends Unary(left) with Fn {
  override def prettyName: String = "PARSE_JSON"
  override def dataType: DataType = VariantType
}

/**
 * startswith(expr, startExpr) - Returns true if expr begins with startExpr.
 */
case class StartsWith(expr: Expression, startExpr: Expression) extends Binary(expr, startExpr) with Fn {
  override def prettyName: String = "STARTSWITH"
  override def dataType: DataType = BooleanType
}