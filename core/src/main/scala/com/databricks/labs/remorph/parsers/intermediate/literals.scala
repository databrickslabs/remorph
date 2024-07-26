package com.databricks.labs.remorph.parsers.intermediate

object Literal {
  def apply(value: Array[Byte]): Literal = Literal(binary = Some(value))
  def apply(value: Boolean): Literal = Literal(boolean = Some(value))
  def apply(value: Byte): Literal = Literal(byte = Some(value.intValue()))
  def apply(value: Short): Literal = Literal(short = Some(value.intValue()))
  def apply(value: Int): Literal = Literal(integer = Some(value))
  def apply(value: Long): Literal = Literal(long = Some(value))
  def apply(value: Float): Literal = Literal(float = Some(value))
  def apply(value: Decimal): Literal = Literal(decimal = Some(value))
  def apply(value: Double): Literal = Literal(double = Some(value))
  def apply(value: String): Literal = Literal(string = Some(value))
  def apply(value: java.sql.Date): Literal = Literal(date = Some(value.getTime))
  def apply(value: java.sql.Timestamp): Literal = Literal(timestamp = Some(value.getTime))
  def apply(value: Map[String, Expression]): Literal = Literal(map = Some(
    MapExpr(
      StringType,
      value.values.head.dataType,
      value.keys.map(key => Literal(string = Some(key))).toSeq,
      value.values.toSeq)))
  def apply(values: Seq[Expression]): Literal =
    Literal(array = Some(ArrayExpr(values.headOption.map(_.dataType).getOrElse(UnresolvedType), values)))
}

case class Literal(
    nullType: Option[DataType] = None,
    binary: Option[Array[Byte]] = None,
    boolean: Option[Boolean] = None,
    byte: Option[Int] = None,
    short: Option[Int] = None,
    integer: Option[Int] = None,
    long: Option[Long] = None,
    float: Option[Float] = None,
    decimal: Option[Decimal] = None,
    double: Option[Double] = None,
    string: Option[String] = None,
    date: Option[Long] = None,
    timestamp: Option[Long] = None,
    timestamp_ntz: Option[Long] = None,
    calendar_interval: Option[CalendarInterval] = None,
    year_month_interval: Option[Int] = None,
    day_time_interval: Option[Long] = None,
    array: Option[ArrayExpr] = None,
    map: Option[MapExpr] = None,
    json: Option[JsonExpr] = None)
    extends LeafExpression {

  override def dataType: DataType = {
    this match {
      case _ if binary.isDefined => BinaryType
      case _ if boolean.isDefined => BooleanType
      case _ if byte.isDefined => ByteType(byte)
      case _ if short.isDefined => ShortType
      case _ if integer.isDefined => IntegerType
      case _ if long.isDefined => LongType
      case _ if float.isDefined => FloatType
      case _ if decimal.isDefined => DecimalType(decimal.get.precision, decimal.get.scale)
      case _ if double.isDefined => DoubleType
      case _ if string.isDefined => StringType
      case _ if date.isDefined => DateType
      case _ if timestamp.isDefined => TimestampType
      case _ if timestamp_ntz.isDefined => TimestampNTZType
      case _ if calendar_interval.isDefined => CalendarIntervalType
      case _ if year_month_interval.isDefined => YearMonthIntervalType
      case _ if day_time_interval.isDefined => DayTimeIntervalType
      case _ if array.isDefined => ArrayType(array.map(_.dataType).getOrElse(UnresolvedType))
      case _ if map.isDefined =>
        MapType(map.map(_.key_type).getOrElse(UnresolvedType), map.map(_.value_type).getOrElse(UnresolvedType))
      case _ if json.isDefined => UDTType()
      case _ => NullType
    }
  }
}
