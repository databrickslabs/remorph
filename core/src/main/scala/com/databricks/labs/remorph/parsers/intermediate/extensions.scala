package com.databricks.labs.remorph.parsers.intermediate

trait AstExtension

case class Id(id: String, caseSensitive: Boolean = false) extends Expression {}

case class ObjectReference(head: Id, tail: Id*) extends Expression {}

case class Column(tableNameOrAlias: Option[ObjectReference], columnName: Id) extends Expression with AstExtension {}
case class Identifier(name: String, isQuoted: Boolean) extends Expression with AstExtension {}
case class DollarAction() extends Expression with AstExtension {}
case class Distinct(expression: Expression) extends Expression

abstract class Unary(pred: Expression) extends Expression {}
abstract class Binary(left: Expression, right: Expression) extends Expression {}

trait Predicate extends AstExtension

case class And(left: Expression, right: Expression) extends Binary(left, right) with Predicate {}
case class Or(left: Expression, right: Expression) extends Binary(left, right) with Predicate {}
case class Not(pred: Expression) extends Unary(pred) with Predicate {}

case class Equals(left: Expression, right: Expression) extends Binary(left, right) with Predicate {}
case class NotEquals(left: Expression, right: Expression) extends Binary(left, right) with Predicate {}
case class GreaterThan(left: Expression, right: Expression) extends Binary(left, right) with Predicate {}
case class LesserThan(left: Expression, right: Expression) extends Binary(left, right) with Predicate {}
case class GreaterThanOrEqual(left: Expression, right: Expression) extends Binary(left, right) with Predicate {}
case class LesserThanOrEqual(left: Expression, right: Expression) extends Binary(left, right) with Predicate {}

case object Noop extends Expression
case object RowNumber extends Expression {}
case class NTile(expression: Expression) extends Expression {}

case class WithCTE(ctes: Seq[Relation], query: Relation) extends RelationCommon {}
case class CTEDefinition(tableName: String, columns: Seq[Expression], cte: Relation) extends RelationCommon {}

case class Star(objectName: Option[ObjectReference]) extends Expression {}
case class Inserted(selection: Expression) extends Expression()
case class Deleted(selection: Expression) extends Expression()

case class WhenBranch(condition: Expression, expression: Expression) extends Expression
case class Case(expression: Option[Expression], branches: Seq[WhenBranch], otherwise: Option[Expression])
    extends Expression {}

case class Exists(relation: Relation) extends Expression {}

case class IsIn(relation: Relation, expression: Expression) extends Expression {}

case class Like(expression: Expression, patterns: Seq[Expression], escape: Option[Expression], caseSensitive: Boolean)
    extends Expression {}

case class RLike(expression: Expression, pattern: Expression) extends Expression {}

case class IsNull(expression: Expression) extends Expression {}

// TODO: TSQL grammar has a number of operators not yet supported - add them here, if not already supported

// Operators, in order of precedence

// Bitwise NOT is highest precedence after parens '(' ')'
case class BitwiseNot(expression: Expression) extends Unary(expression) {}

// Unary arithmetic expressions
case class UMinus(expression: Expression) extends Unary(expression) {}
case class UPlus(expression: Expression) extends Unary(expression) {}

// Binary Arithmetic expressions
case class Multiply(left: Expression, right: Expression) extends Binary(left, right) {}
case class Divide(left: Expression, right: Expression) extends Binary(left, right) {}
case class Mod(left: Expression, right: Expression) extends Binary(left, right) {}

case class Add(left: Expression, right: Expression) extends Binary(left, right) {}
case class Subtract(left: Expression, right: Expression) extends Binary(left, right) {}

// Binary bitwise expressions
case class BitwiseAnd(left: Expression, right: Expression) extends Binary(left, right) {}
case class BitwiseOr(left: Expression, right: Expression) extends Binary(left, right) {}
case class BitwiseXor(left: Expression, right: Expression) extends Binary(left, right) {}

// Other binary expressions
case class Concat(left: Expression, right: Expression) extends Binary(left, right) {}

// Assignment operators
case class Assign(left: Expression, right: Expression) extends Binary(left, right) {}

// Some statements, such as SELECT, do not require a table specification
case class NoTable() extends Relation {}

// It was not clear whether the NamedTable options should be used for the alias. I'm assuming it is not what
// they are for.
case class TableAlias(relation: Relation, alias: String) extends Relation {}

case class Batch(statements: Seq[Plan]) extends Plan

case class FunctionParameter(name: String, dataType: DataType, defaultValue: Option[Expression])

sealed trait UDFRuntimeInfo
case class JavaUDFInfo(runtimeVersion: Option[String], imports: Seq[String], handler: String) extends UDFRuntimeInfo
case class PythonUDFInfo(runtimeVersion: Option[String], packages: Seq[String], handler: String) extends UDFRuntimeInfo
case object JavascriptUDFInfo extends UDFRuntimeInfo
case class ScalaUDFInfo(runtimeVersion: Option[String], imports: Seq[String], handler: String) extends UDFRuntimeInfo
case class SQLUDFInfo(memoizable: Boolean) extends UDFRuntimeInfo

case class CreateInlineUDF(
    name: String,
    returnType: DataType,
    parameters: Seq[FunctionParameter],
    runtimeInfo: UDFRuntimeInfo,
    acceptsNullParameters: Boolean,
    comment: Option[String],
    body: String)
    extends Catalog {}

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

// Used for raw expressions that have no context
case class Dot(left: Expression, right: Expression) extends Binary(left, right) {}

// Specialized function calls, such as XML functions that usually apply to columns
case class XmlFunction(function: CallFunction, column: Expression) extends Expression {}

case class NextValue(sequenceName: String) extends Expression {}
case class ArrayAccess(array: Expression, index: Expression) extends Expression {}
case class JsonAccess(json: Expression, path: Seq[String]) extends Expression {}
case class Collate(string: Expression, specification: String) extends Expression {}
case class Iff(condition: Expression, thenBranch: Expression, elseBranch: Expression) extends Expression {}

case class ScalarSubquery(relation: Relation) extends Expression {}

case class Timezone(expression: Expression, timeZone: Expression) extends Expression {}

case class Money(value: Literal) extends Expression {}

case class WithinGroup(expression: Expression, order: Seq[SortOrder]) extends Expression {}

sealed trait SamplingMethod
case class RowSamplingProbabilistic(probability: BigDecimal) extends SamplingMethod
case class RowSamplingFixedAmount(amount: BigDecimal) extends SamplingMethod
case class BlockSampling(probability: BigDecimal) extends SamplingMethod

case class TableSample(input: Relation, samplingMethod: SamplingMethod, seed: Option[BigDecimal]) extends Relation {}

// Note that Databricks SQL supports FILTER() used as an expression.
case class FilterExpr(input: Seq[Expression], lambdaFunction: LambdaFunction) extends Expression {}
case class ValueArray(expressions: Seq[Expression]) extends Expression {}

case class NamedStruct(keys: Seq[Expression], values: Seq[Expression]) extends Expression {}
case class FilterStruct(input: NamedStruct, lambdaFunction: LambdaFunction) extends Expression {}

case class BackupDatabase(
    databaseName: String,
    disks: Seq[String],
    flags: Map[String, Boolean],
    autoFlags: Seq[String],
    values: Map[String, Expression])
    extends Command {}

case class ArrayAgg(values: Expression, sort: Seq[SortOrder]) extends Expression {}
