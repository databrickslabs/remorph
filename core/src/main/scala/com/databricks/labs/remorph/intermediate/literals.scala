package com.databricks.labs.remorph.intermediate

import java.time.ZoneOffset

case class Literal(value: Any, dataType: DataType) extends LeafExpression

object Literal {
  val True: Literal = Literal(true, BooleanType)
  val False: Literal = Literal(false, BooleanType)
  val Null: Literal = Literal(null, NullType)
  private val byteType = ByteType(Some(1))
  private[intermediate] val defaultDecimal = DecimalType(38, 18)

  // this factory returns Expression instead of Literal, because array and map literals have children
  // and Literal is a LeafExpression, which has no children by definition.
  def apply(value: Any): Expression = value match {
    case null => Null
    case i: Int => Literal(i, IntegerType)
    case l: Long => Literal(l, LongType)
    case f: Float => NumericLiteral(f)
    case d: Double => NumericLiteral(d)
    case b: Byte => Literal(b, byteType)
    case s: Short => Literal(s, ShortType)
    case s: String => Literal(s, StringType)
    case c: Char => Literal(c.toString, StringType)
    case b: Boolean => Literal(b, BooleanType)
    case d: BigDecimal => Literal(d, DecimalType.fromBigDecimal(d))
    // TODO: revise date type handling later
    case d: java.sql.Date => Literal(d.toLocalDate.toEpochDay, DateType)
    case d: java.time.LocalDate => Literal(d.toEpochDay, DateType)
    case d: java.sql.Timestamp => Literal(d.getTime, TimestampType)
    case d: java.time.LocalDateTime => Literal(d.toEpochSecond(ZoneOffset.UTC), TimestampType)
    case d: Array[Byte] => Literal(d, BinaryType)
    case a: Array[_] =>
      val elementType = componentTypeToDataType(a.getClass.getComponentType)
      val dataType = ArrayType(elementType)
      Literal(convert(a, dataType), dataType)
    case s: Seq[_] =>
      val elementType = componentTypeToDataType(s.head.getClass)
      val dataType = ArrayType(elementType)
      convert(s, dataType)
    case m: Map[_, _] =>
      val keyType = componentTypeToDataType(m.keys.head.getClass)
      val valueType = componentTypeToDataType(m.values.head.getClass)
      val dataType = MapType(keyType, valueType)
      convert(m, dataType)
    case _ => throw new IllegalStateException(s"Unsupported value: $value")
  }

  private def convert(value: Any, dataType: DataType): Expression = (value, dataType) match {
    case (Some(v), t) if t.isPrimitive => Literal(v, t)
    case (None, t) if t.isPrimitive => Null
    case (v, t) if t.isPrimitive => Literal(v, t)
    case (v: Array[_], ArrayType(elementType)) =>
      val elements = v.map { e => convert(e, elementType) }.toList
      ArrayExpr(elements, dataType)
    case (v: Seq[_], ArrayType(elementType)) =>
      val elements = v.map { e => convert(e, elementType) }.toList
      ArrayExpr(elements, dataType)
    case (v: Map[_, _], MapType(keyType, valueType)) =>
      val map = v.map { case (k, v) => convert(k, keyType) -> convert(v, valueType) }
      MapExpr(map, dataType)
    case _ =>
      throw new IllegalStateException(s"Unsupported value: $value and dataType: $dataType")
  }

  private[this] def componentTypeToDataType(clz: Class[_]): DataType = clz match {
    // primitive types
    case java.lang.Short.TYPE => ShortType
    case java.lang.Integer.TYPE => IntegerType
    case java.lang.Long.TYPE => LongType
    case java.lang.Double.TYPE => DoubleType
    case java.lang.Byte.TYPE => byteType
    case java.lang.Float.TYPE => FloatType
    case java.lang.Boolean.TYPE => BooleanType
    case java.lang.Character.TYPE => StringType

    // java classes
    case _ if clz == classOf[java.sql.Date] => DateType
    case _ if clz == classOf[java.time.LocalDate] => DateType
    case _ if clz == classOf[java.time.Instant] => TimestampType
    case _ if clz == classOf[java.sql.Timestamp] => TimestampType
    case _ if clz == classOf[java.time.LocalDateTime] => TimestampNTZType
    case _ if clz == classOf[java.time.Duration] => DayTimeIntervalType
    case _ if clz == classOf[java.time.Period] => YearMonthIntervalType
    case _ if clz == classOf[java.math.BigDecimal] => defaultDecimal
    case _ if clz == classOf[Array[Byte]] => BinaryType
    case _ if clz == classOf[Array[Char]] => StringType
    case _ if clz == classOf[java.lang.Short] => ShortType
    case _ if clz == classOf[java.lang.Integer] => IntegerType
    case _ if clz == classOf[java.lang.Long] => LongType
    case _ if clz == classOf[java.lang.Double] => DoubleType
    case _ if clz == classOf[java.lang.Byte] => byteType
    case _ if clz == classOf[java.lang.Float] => FloatType
    case _ if clz == classOf[java.lang.Boolean] => BooleanType

    // other scala classes
    case _ if clz == classOf[String] => StringType
    case _ if clz == classOf[BigInt] => defaultDecimal
    case _ if clz == classOf[BigDecimal] => defaultDecimal
    case _ if clz == classOf[CalendarInterval] => CalendarIntervalType

    case _ if clz.isArray => ArrayType(componentTypeToDataType(clz.getComponentType))

    case _ =>
      throw new IllegalStateException(s"Unsupported type: $clz")
  }

  // TODO: validate the value and dataType
}

case class ArrayExpr(children: Seq[Expression], dataType: DataType) extends Expression

case class MapExpr(map: Map[Expression, Expression], dataType: DataType) extends Expression {
  override def children: Seq[Expression] = (map.keys ++ map.values).toList
}

object NumericLiteral {
  def apply(v: String): Literal = convert(BigDecimal(v))
  def apply(v: Double): Literal = convert(BigDecimal(v))
  def apply(v: Float): Literal = apply(v.toString)

  private def convert(d: BigDecimal): Literal = d match {
    case d if d.isValidInt => Literal(d.toInt, IntegerType)
    case d if d.isValidLong => Literal(d.toLong, LongType)
    case d if d.isDecimalFloat || d.isExactFloat => Literal(d.toFloat, FloatType)
    case d if d.isDecimalDouble || d.isExactDouble => Literal(d.toDouble, DoubleType)
    case d => DecimalLiteral.auto(d)
  }
}

object DecimalLiteral {
  private[intermediate] def auto(d: BigDecimal): Literal = Literal(d, DecimalType.fromBigDecimal(d))
  def apply(v: Long): Literal = auto(BigDecimal(v))
  def apply(v: Double): Literal = auto(BigDecimal(v))
  def apply(v: String): Literal = auto(BigDecimal(v))
  def unapply(e: Expression): Option[BigDecimal] = e match {
    case Literal(v: BigDecimal, _: DecimalType) => Some(v)
    case _ => None
  }
}

object FloatLiteral {
  def apply(f: Float): Literal = Literal(f, FloatType)
  def unapply(a: Any): Option[Float] = a match {
    case Literal(a: Float, FloatType) => Some(a)
    case _ => None
  }
}

object DoubleLiteral {
  def apply(d: Double): Literal = Literal(d, DoubleType)
  def unapply(a: Any): Option[Double] = a match {
    case Literal(a: Double, DoubleType) => Some(a)
    case Literal(a: Float, FloatType) => Some(a.toDouble)
    case _ => None
  }
}

object IntLiteral {
  def apply(i: Int): Literal = Literal(i, IntegerType)
  def unapply(a: Any): Option[Int] = a match {
    case Literal(a: Int, IntegerType) => Some(a)
    case Literal(a: Short, ShortType) => Some(a.toInt)
    case _ => None
  }
}

object LongLiteral {
  def apply(l: Long): Literal = Literal(l, LongType)
  def apply(i: Int): Literal = Literal(i.toLong, LongType)
  def apply(s: Short): Literal = Literal(s.toLong, LongType)
  def unapply(a: Any): Option[Long] = a match {
    case Literal(a: Long, LongType) => Some(a)
    case Literal(a: Int, IntegerType) => Some(a.toLong)
    case Literal(a: Short, ShortType) => Some(a.toLong)
    case _ => None
  }
}

object StringLiteral {
  def apply(s: String): Literal = Literal(s, StringType)
  def unapply(a: Any): Option[String] = a match {
    case Literal(s: String, StringType) => Some(s)
    case _ => None
  }
}

object BooleanLiteral {
  def apply(b: Boolean): Literal = if (b) Literal.True else Literal.False
  def unapply(a: Any): Option[Boolean] = a match {
    case Literal(true, BooleanType) => Some(true)
    case _ => Some(false)
  }
}
