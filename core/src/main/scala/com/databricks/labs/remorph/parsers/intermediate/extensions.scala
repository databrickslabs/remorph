package com.databricks.labs.remorph.parsers.intermediate

trait AstExtension

abstract class ToRefactor extends LeafExpression {
  override def dataType: DataType = UnresolvedType
}

case class Id(id: String, caseSensitive: Boolean = false) extends ToRefactor

case class ObjectReference(head: Id, tail: Id*) extends ToRefactor

case class Column(tableNameOrAlias: Option[ObjectReference], columnName: Id) extends ToRefactor with AstExtension {}
case class Identifier(name: String, isQuoted: Boolean) extends ToRefactor with AstExtension {}
case class DollarAction() extends ToRefactor with AstExtension {}
case class Distinct(expression: Expression) extends ToRefactor

abstract class Unary(child: Expression) extends Expression {
  override def children: Seq[Expression] = Seq(child)
}

abstract class Binary(left: Expression, right: Expression) extends Expression {
  override def children: Seq[Expression] = Seq(left, right)
}

trait Predicate extends AstExtension {
  def dataType: DataType = BooleanType
}

case class And(left: Expression, right: Expression) extends Binary(left, right) with Predicate {}
case class Or(left: Expression, right: Expression) extends Binary(left, right) with Predicate {}
case class Not(pred: Expression) extends Unary(pred) with Predicate {}

case class Equals(left: Expression, right: Expression) extends Binary(left, right) with Predicate {}
case class NotEquals(left: Expression, right: Expression) extends Binary(left, right) with Predicate {}
case class GreaterThan(left: Expression, right: Expression) extends Binary(left, right) with Predicate {}
case class LesserThan(left: Expression, right: Expression) extends Binary(left, right) with Predicate {}
case class GreaterThanOrEqual(left: Expression, right: Expression) extends Binary(left, right) with Predicate {}
case class LesserThanOrEqual(left: Expression, right: Expression) extends Binary(left, right) with Predicate {}

case object Noop extends LeafExpression {
  override def dataType: DataType = UnresolvedType
}

case object NoopNode extends LeafNode {
  override def output: Seq[Attribute] = Seq.empty
}

case class WithCTE(ctes: Seq[LogicalPlan], query: LogicalPlan) extends RelationCommon {
  override def output: Seq[Attribute] = query.output
  override def children: Seq[LogicalPlan] = ctes :+ query
}

case class CTEDefinition(tableName: String, columns: Seq[Expression], cte: LogicalPlan) extends RelationCommon {
  override def output: Seq[Attribute] = columns.map(c => AttributeReference(c.toString, c.dataType))
  override def children: Seq[LogicalPlan] = Seq(cte)
}

case class Star(objectName: Option[ObjectReference]) extends LeafExpression {
  override def dataType: DataType = UnresolvedType
}
case class Inserted(selection: Expression) extends Unary(selection) {
  override def dataType: DataType = selection.dataType
}
case class Deleted(selection: Expression) extends Unary(selection) {
  override def dataType: DataType = selection.dataType
}

case class WhenBranch(condition: Expression, expression: Expression) extends Binary(condition, expression) {
  override def dataType: DataType = expression.dataType
}

case class Case(expression: Option[Expression], branches: Seq[WhenBranch], otherwise: Option[Expression])
    extends Expression {
  override def children: Seq[Expression] = expression.toSeq ++
    branches.flatMap(b => Seq(b.condition, b.expression)) ++ otherwise
  override def dataType: DataType = branches.head.dataType
}

case class Exists(relation: LogicalPlan) extends ToRefactor

case class IsInRelation(relation: LogicalPlan, expression: Expression) extends ToRefactor
case class IsInCollection(collection: Seq[Expression], expression: Expression) extends ToRefactor

// TODO: convert into Like
case class LikeSnowflake(
    expression: Expression,
    patterns: Seq[Expression],
    escape: Option[Expression],
    caseSensitive: Boolean)
    extends ToRefactor

/**
 * str like pattern[ ESCAPE escape] - Returns true if str matches `pattern` with `escape`, null if any arguments are
 * null, false otherwise.
 */
case class Like(left: Expression, right: Expression, escapeChar: Char = '\\') extends Binary(left, right) {
  override def dataType: DataType = BooleanType
}

// Operators, in order of precedence

// Bitwise NOT is highest precedence after parens '(' ')'
case class BitwiseNot(expression: Expression) extends Unary(expression) {
  override def dataType: DataType = expression.dataType
}

// Unary arithmetic expressions
case class UMinus(expression: Expression) extends Unary(expression) {
  override def dataType: DataType = expression.dataType
}
case class UPlus(expression: Expression) extends Unary(expression) {
  override def dataType: DataType = expression.dataType
}

// Binary Arithmetic expressions
case class Multiply(left: Expression, right: Expression) extends Binary(left, right) {
  override def dataType: DataType = left.dataType
}
case class Divide(left: Expression, right: Expression) extends Binary(left, right) {
  override def dataType: DataType = left.dataType
}
case class Mod(left: Expression, right: Expression) extends Binary(left, right) {
  override def dataType: DataType = left.dataType
}
case class Add(left: Expression, right: Expression) extends Binary(left, right) {
  override def dataType: DataType = left.dataType
}
case class Subtract(left: Expression, right: Expression) extends Binary(left, right) {
  override def dataType: DataType = left.dataType
}

// Binary bitwise expressions
case class BitwiseAnd(left: Expression, right: Expression) extends Binary(left, right) {
  override def dataType: DataType = left.dataType
}
case class BitwiseOr(left: Expression, right: Expression) extends Binary(left, right) {
  override def dataType: DataType = left.dataType
}
case class BitwiseXor(left: Expression, right: Expression) extends Binary(left, right) {
  override def dataType: DataType = left.dataType
}

// Assignment operators
case class Assign(left: Expression, right: Expression) extends Binary(left, right) {
  override def dataType: DataType = UnresolvedType
}

// Some statements, such as SELECT, do not require a table specification
case class NoTable() extends LeafNode {
  override def output: Seq[Attribute] = Seq.empty
}
case class LocalVarTable(id: Id) extends LeafNode {
  override def output: Seq[Attribute] = Seq.empty
}

// Table hints are not directly supported in Databricks SQL, but at least some of
// them will have direct equivalents for the Catalyst optimizer. Hence they are
// included in the AST for the code generator to use them if it can. At worst,
// a comment can be generated with the hint text to guide the conversion.
abstract class TableHint
case class FlagHint(name: String) extends TableHint
case class IndexHint(indexes: Seq[Expression]) extends TableHint
case class ForceSeekHint(index: Option[Expression], indexColumns: Option[Seq[Expression]]) extends TableHint

// It was not clear whether the NamedTable options should be used for the alias. I'm assuming it is not what
// they are for.
case class TableAlias(child: LogicalPlan, alias: String, columns: Seq[Id] = Seq.empty) extends UnaryNode {
  override def output: Seq[Attribute] = columns.map(c => AttributeReference(c.id, StringType))
}

// TODO: remove this and replace with Hint(Hint(...), ...)
case class TableWithHints(child: LogicalPlan, hints: Seq[TableHint]) extends UnaryNode {
  override def output: Seq[Attribute] = child.output
}

case class Batch(children: Seq[LogicalPlan]) extends LogicalPlan {
  override def output: Seq[Attribute] = Seq.empty
}

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
case class Dot(left: Expression, right: Expression) extends Binary(left, right) {
  override def dataType: DataType = UnresolvedType
}

// Specialized function calls, such as XML functions that usually apply to columns
case class XmlFunction(function: CallFunction, column: Expression) extends Binary(function, column) {
  override def dataType: DataType = UnresolvedType
}

case class NextValue(sequenceName: String) extends LeafExpression {
  override def dataType: DataType = LongType
}
case class ArrayAccess(array: Expression, index: Expression) extends Binary(array, index) {
  override def dataType: DataType = array.dataType
}

case class JsonAccess(json: Expression, path: Expression) extends Binary(json, path) {
  override def dataType: DataType = UnresolvedType
}

case class Collate(string: Expression, specification: String) extends Unary(string) {
  override def dataType: DataType = StringType
}
case class Iff(condition: Expression, thenBranch: Expression, elseBranch: Expression) extends Expression {
  override def children: Seq[Expression] = Seq(condition, thenBranch, elseBranch)
  override def dataType: DataType = thenBranch.dataType
}

case class ScalarSubquery(relation: LogicalPlan) extends ToRefactor

case class Timezone(expression: Expression, timeZone: Expression) extends Binary(expression, timeZone) {
  override def dataType: DataType = expression.dataType
}

case class Money(value: Literal) extends Unary(value) {
  override def dataType: DataType = UnresolvedType
}

case class WithinGroup(expression: Expression, order: Seq[SortOrder]) extends Unary(expression) {
  override def dataType: DataType = expression.dataType
}

sealed trait SamplingMethod
case class RowSamplingProbabilistic(probability: BigDecimal) extends SamplingMethod
case class RowSamplingFixedAmount(amount: BigDecimal) extends SamplingMethod
case class BlockSampling(probability: BigDecimal) extends SamplingMethod

case class TableSample(input: LogicalPlan, samplingMethod: SamplingMethod, seed: Option[BigDecimal]) extends UnaryNode {
  override def child: LogicalPlan = input
  override def output: Seq[Attribute] = input.output
}

// Note that Databricks SQL supports FILTER() used as an expression.
case class FilterExpr(input: Seq[Expression], lambdaFunction: LambdaFunction) extends Expression {
  override def children: Seq[Expression] = input :+ lambdaFunction
  override def dataType: DataType = UnresolvedType
}

case class ValueArray(expressions: Seq[Expression]) extends Expression {
  override def children: Seq[Expression] = expressions
  override def dataType: DataType = UnresolvedType
}

case class NamedStruct(keys: Seq[Expression], values: Seq[Expression]) extends Expression {
  override def children: Seq[Expression] = keys ++ values
  override def dataType: DataType = UnresolvedType
}

case class FilterStruct(input: NamedStruct, lambdaFunction: LambdaFunction) extends Expression {
  override def children: Seq[Expression] = Seq(input, lambdaFunction)
  override def dataType: DataType = UnresolvedType
}

case class Options(
    expressionOpts: Map[String, Expression],
    stringOpts: Map[String, String],
    boolFlags: Map[String, Boolean],
    autoFlags: List[String])
    extends Expression {
  override def children: Seq[Expression] = expressionOpts.values.toSeq
  override def dataType: DataType = UnresolvedType
}

case class BackupDatabase(
    databaseName: String,
    disks: Seq[String],
    flags: Map[String, Boolean],
    autoFlags: Seq[String],
    values: Map[String, Expression])
    extends LeafNode
    with Command {}

case class Output(target: LogicalPlan, outputs: Seq[Expression], columns: Option[Seq[Column]]) extends RelationCommon {
  override def output: Seq[Attribute] = outputs.map(e => AttributeReference(e.toString, e.dataType))
  override def children: Seq[LogicalPlan] = Seq(target)
}

// Used for DML other than SELECT
abstract class Modification extends LogicalPlan

case class InsertIntoTable( // TODO: fix it
    target: LogicalPlan,
    columns: Option[Seq[Id]],
    values: LogicalPlan,
    outputRelation: Option[LogicalPlan],
    options: Option[Expression],
    overwrite: Boolean)
    extends Modification {
  override def children: Seq[LogicalPlan] = Seq(target, values, outputRelation.getOrElse(NoopNode))
  override def output: Seq[Attribute] = target.output
}

case class DerivedRows(rows: Seq[Seq[Expression]]) extends LeafNode {
  override def output: Seq[Attribute] = rows.flatten.map(e => AttributeReference(e.toString, e.dataType))
}

case class DefaultValues() extends LeafNode {
  override def output: Seq[Attribute] = Seq.empty
}

// The default case for the expression parser needs to be explicitly defined to distinguish [DEFAULT]
case class Default() extends LeafExpression {
  override def dataType: DataType = UnresolvedType
}

// TSQL has some join types that are not natively supported in Databricks SQL, but can possibly be emulated
// using LATERAL VIEW and an explode function. Some things like functions are translatable at IR production
// time, but complex joins are probably/possibly better done at the translation from IR as they are more involved
// than some simple prescribed action.
case object CrossApply extends JoinType
case object OuterApply extends JoinType

case class ColumnAliases(input: LogicalPlan, aliases: Seq[Id]) extends RelationCommon {
  override def output: Seq[Attribute] = aliases.map(a => AttributeReference(a.id, StringType))
  override def children: Seq[LogicalPlan] = Seq(input)
}

case class TableFunction(functionCall: Expression) extends LeafNode {
  override def output: Seq[Attribute] = Seq.empty
}
case class Lateral(expr: LogicalPlan) extends UnaryNode {
  override def child: LogicalPlan = expr
  override def output: Seq[Attribute] = expr.output
}

case class DeleteFromTable(
    target: LogicalPlan,
    source: Option[LogicalPlan],
    where: Option[Expression],
    outputRelation: Option[LogicalPlan],
    options: Option[Expression])
    extends Modification {
  override def children: Seq[LogicalPlan] = Seq(target, source.getOrElse(NoopNode), outputRelation.getOrElse(NoopNode))
  override def output: Seq[Attribute] = target.output
}

case class UpdateTable(
    target: LogicalPlan,
    source: Option[LogicalPlan],
    set: Seq[Expression],
    where: Option[Expression],
    outputRelation: Option[LogicalPlan],
    options: Option[Expression])
    extends Modification {
  override def children: Seq[LogicalPlan] = Seq(target, source.getOrElse(NoopNode), outputRelation.getOrElse(NoopNode))
  override def output: Seq[Attribute] = target.output
}

case class MergeTables(
    target: LogicalPlan,
    source: Option[LogicalPlan],
    conditions: Option[Expression],
    outputRelation: Option[LogicalPlan],
    options: Option[Expression])
    extends Modification {
  override def children: Seq[LogicalPlan] = Seq(target, source.getOrElse(NoopNode), outputRelation.getOrElse(NoopNode))
  override def output: Seq[Attribute] = target.output
}
