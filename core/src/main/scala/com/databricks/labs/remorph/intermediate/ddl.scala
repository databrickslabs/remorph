package com.databricks.labs.remorph.intermediate

abstract class DataType {
  def isPrimitive: Boolean = this match {
    case BooleanType => true
    case ByteType(_) => true
    case ShortType => true
    case IntegerType => true
    case LongType => true
    case FloatType => true
    case DoubleType => true
    case StringType => true
    case _ => false
  }
}

case object NullType extends DataType
case object BooleanType extends DataType
case object BinaryType extends DataType

// Numeric types
case class ByteType(size: Option[Int]) extends DataType
case object ShortType extends DataType
case object TinyintType extends DataType
case object IntegerType extends DataType
case object LongType extends DataType

case object FloatType extends DataType
case object DoubleType extends DataType

object DecimalType {
  def apply(): DecimalType = DecimalType(None, None)
  def apply(precision: Int, scale: Int): DecimalType = DecimalType(Some(precision), Some(scale))
  def fromBigDecimal(d: BigDecimal): DecimalType = DecimalType(Some(d.precision), Some(d.scale))
}

case class DecimalType(precision: Option[Int], scale: Option[Int]) extends DataType

// String types
case object StringType extends DataType
case class CharType(size: Option[Int]) extends DataType
case class VarcharType(size: Option[Int]) extends DataType

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
case class StructField(name: String, dataType: DataType, nullable: Boolean = true, metadata: Option[Metadata] = None)
case class StructType(fields: Seq[StructField]) extends DataType
case class MapType(keyType: DataType, valueType: DataType) extends DataType
case object VariantType extends DataType
case class Metadata(comment: Option[String])
// While Databricks SQl does not DIRECTLY support IDENTITY in the way some other dialects do, it does support
// Id BIGINT GENERATED ALWAYS AS IDENTITY
case class IdentityType(start: Option[Int], increment: Option[Int]) extends DataType

// UserDefinedType
case class UDTType() extends DataType

case class UnparsedType(text: String) extends DataType

case object UnresolvedType extends DataType

// These are likely to change in a not-so-remote future. Spark SQL does not have constraints
// as it is not a database in its own right. Databricks SQL supports Key constraints and
// also allows the definition of CHECK constraints via ALTER table after table creation. Spark
// does support nullability but stores that as a boolean in the column definition, as well as an
// expression for default values.
//
// So we will store the column constraints with the column definition and then use them to generate
// Databricks SQL CHECK constraints where we can, and comment the rest.
sealed trait Constraint
sealed trait UnnamedConstraint extends Constraint
case class Unique(options: Seq[GenericOption] = Seq.empty, columns: Option[Seq[String]] = None)
    extends UnnamedConstraint
// Nullability is kept in case the NOT NULL constraint is named and we must generate a CHECK constraint
case class Nullability(nullable: Boolean) extends UnnamedConstraint
case class PrimaryKey(options: Seq[GenericOption] = Seq.empty, columns: Option[Seq[String]] = None)
    extends UnnamedConstraint
case class ForeignKey(tableCols: String, refObject: String, refCols: String, options: Seq[GenericOption])
    extends UnnamedConstraint
case class DefaultValueConstraint(value: Expression) extends UnnamedConstraint
case class CheckConstraint(expression: Expression) extends UnnamedConstraint
// ExtendedBased on https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-ddl-create-table-using.html#syntax
case class IdentityConstraint(
    start: Option[String] = None,
    increment: Option[String] = None,
    always: Boolean = false,
    default: Boolean = false)
    extends UnnamedConstraint
case class NamedConstraint(name: String, constraint: UnnamedConstraint) extends Constraint
case class UnresolvedConstraint(inputText: String) extends UnnamedConstraint
case class GeneratedAlways(expression: Expression) extends UnnamedConstraint

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

// TODO Need to introduce TableSpecBase, TableSpec and UnresolvedTableSpec

case class ReplaceTableCommand(name: String, columns: Seq[ColumnDeclaration], orCreate: Boolean) extends Catalog

case class ReplaceTableAsSelect(
    table_name: String,
    query: LogicalPlan,
    writeOptions: Map[String, String],
    orCreate: Boolean,
    isAnalyzed: Boolean = false)
    extends Catalog

sealed trait TableAlteration
case class AddColumn(columnDeclaration: Seq[ColumnDeclaration]) extends TableAlteration
case class AddConstraint(columnName: String, constraint: Constraint) extends TableAlteration
case class ChangeColumnDataType(columnName: String, newDataType: DataType) extends TableAlteration
case class UnresolvedTableAlteration(
    ruleText: String,
    message: String,
    ruleName: String = "rule name undetermined",
    tokenName: Option[String] = None)
    extends TableAlteration
    with UnwantedInGeneratorInput
    with Unresolved[UnresolvedTableAlteration] {
  override def annotate(newRuleName: String, newTokenName: Option[String]): UnresolvedTableAlteration =
    copy(ruleName = newRuleName, tokenName = newTokenName)
}

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
    description: Option[String],
    override val schema: DataType)
    extends Catalog {}

// As per Spark v2Commands
case class CreateTable(
    table_name: String,
    path: Option[String],
    source: Option[String],
    description: Option[String],
    override val schema: DataType)
    extends Catalog {}

// As per Spark v2Commands
case class CreateTableAsSelect(
    table_name: String,
    query: LogicalPlan,
    path: Option[String],
    source: Option[String],
    description: Option[String])
    extends Catalog {}

case class DropTempView(view_name: String) extends Catalog {}
case class DropGlobalTempView(view_name: String) extends Catalog {}
case class RecoverPartitions(table_name: String) extends Catalog {}
case class IsCached(table_name: String) extends Catalog {}
case class CacheTable(table_name: String, storage_level: StorageLevel) extends Catalog {}
case class UncachedTable(table_name: String) extends Catalog {}
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
