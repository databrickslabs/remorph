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

case class UnparsedType() extends DataType

case object UnresolvedType extends DataType

sealed trait Constraint
sealed trait UnnamedConstraint extends Constraint
case object Unique extends UnnamedConstraint
case class Nullability(nullable: Boolean) extends UnnamedConstraint
case object PrimaryKey extends UnnamedConstraint
case class ForeignKey(references: String) extends UnnamedConstraint
case class NamedConstraint(name: String, constraint: UnnamedConstraint) extends Constraint
case class UnresolvedConstraint(inputText: String) extends UnnamedConstraint

// This, and the above, are likely to change in a not-so-remote future.
// There's already a CreateTable case defined in catalog.scala but its structure seems too different from
// the information Snowflake grammar carries.
// In future changes, we'll have to reconcile this CreateTableCommand with the "Sparkier" CreateTable somehow.
case class ColumnDeclaration(
    name: String,
    dataType: DataType,
    virtualColumnDeclaration: Option[Expression] = Option.empty,
    constraints: Seq[Constraint] = Seq.empty)

case class CreateTableCommand(name: String, columns: Seq[ColumnDeclaration]) extends Catalog {}

sealed trait TableAlteration
case class AddColumn(columnDeclaration: ColumnDeclaration) extends TableAlteration
case class AddConstraint(columnName: String, constraint: Constraint) extends TableAlteration
case class ChangeColumnDataType(columnName: String, newDataType: DataType) extends TableAlteration
case class UnresolvedTableAlteration(inputText: String) extends TableAlteration
case class DropConstraintByName(constraintName: String) extends TableAlteration
// When constraintName is None, drop the constraint on every relevant column
case class DropConstraint(columnName: Option[String], constraint: Constraint) extends TableAlteration
case class DropColumns(columnNames: Seq[String]) extends TableAlteration
case class RenameConstraint(oldName: String, newName: String) extends TableAlteration
case class RenameColumn(oldName: String, newName: String) extends TableAlteration

case class AlterTableCommand(tableName: String, alterations: Seq[TableAlteration]) extends Catalog {}

// Catalog API (experimental / unstable)
abstract class Catalog extends LeafNode {
  override def output: Seq[Attribute] = Seq.empty
}

case class SetCurrentDatabase(db_name: String) extends Catalog {}
case class ListDatabases(pattern: Option[String]) extends Catalog {}
case class ListTables(db_name: Option[String], pattern: Option[String]) extends Catalog {}
case class ListFunctions(db_name: Option[String], pattern: Option[String]) extends Catalog {}
case class ListColumns(table_name: String, db_name: Option[String]) extends Catalog {}
case class GetDatabase(db_name: String) extends Catalog {}
case class GetTable(table_name: String, db_name: Option[String]) extends Catalog {}
case class GetFunction(function_name: String, db_name: Option[String]) extends Catalog {}
case class DatabaseExists(db_name: String) extends Catalog {}
case class TableExists(table_name: String, db_name: Option[String]) extends Catalog {}
case class FunctionExists(function_name: String, db_name: Option[String]) extends Catalog {}
case class CreateExternalTable(
    table_name: String,
    path: Option[String],
    source: Option[String],
    schema: Option[DataType],
    options: Map[String, String])
    extends Catalog {}
case class CreateTable(
    table_name: String,
    path: Option[String],
    source: Option[String],
    description: Option[String],
    schema: Option[DataType],
    options: Map[String, String])
    extends Catalog {}
case class DropTempView(view_name: String) extends Catalog {}
case class DropGlobalTempView(view_name: String) extends Catalog {}
case class RecoverPartitions(table_name: String) extends Catalog {}
case class IsCached(table_name: String) extends Catalog {}
case class CacheTable(table_name: String, storage_level: StorageLevel) extends Catalog {}
case class UncacheTable(table_name: String) extends Catalog {}
case class ClearCache() extends Catalog {}
case class RefreshTable(table_name: String) extends Catalog {}
case class RefreshByPath(path: String) extends Catalog {}
case class SetCurrentCatalog(catalog_name: String) extends Catalog {}
case class ListCatalogs(pattern: Option[String]) extends Catalog {}

case class TableIdentifier(table: String, database: Option[String])
case class CatalogTable(
    identifier: TableIdentifier,
    schema: StructType,
    partitionColumnNames: Seq[String],
    viewText: Option[String],
    comment: Option[String],
    unsupportedFeatures: Seq[String])
