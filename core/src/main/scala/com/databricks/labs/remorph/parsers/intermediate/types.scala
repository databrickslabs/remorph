package com.databricks.labs.remorph.parsers.intermediate

abstract class DataType
case object NullType extends DataType
case object BooleanType extends DataType
case object BinaryType extends DataType

// Numeric types
case class ByteType(size: Option[Int]) extends DataType
case object ShortType extends DataType
case object IntegerType extends DataType
case object LongType extends DataType

case object FloatType extends DataType
case object DoubleType extends DataType
case class DecimalType(precision: Option[Int], scale: Option[Int]) extends DataType

// String types
case object StringType extends DataType
case class CharType(size: Option[Int]) extends DataType
case class VarCharType(size: Option[Int]) extends DataType

// Datatime types
case object DateType extends DataType
case object TimeType extends DataType
case object TimestampType extends DataType
case object TimestampNTZType extends DataType

// Interval types
case object IntervalType extends DataType
case object CalendarIntervalType extends DataType
case object YearMonthIntervalType extends DataType
case object DayTimeIntervalType extends DataType

// Complex types
case class ArrayType(elementType: DataType) extends DataType
case class StructType() extends DataType
case class MapType(keyType: DataType, valueType: DataType) extends DataType

// UserDefinedType
case class UDTType() extends DataType

// UnparsedDataType
case class UnparsedType() extends DataType

case object UnresolvedType extends DataType