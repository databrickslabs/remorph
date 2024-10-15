package com.databricks.labs.remorph.intermediate

import com.databricks.labs.remorph.utils.Strings
import upickle.default._

sealed trait RemorphError {
  def msg: String
}

trait SingleError extends RemorphError

trait MultipleErrors extends RemorphError {
  def errors: Seq[SingleError]
}

object RemorphError {
  implicit val remorphErrorRW: ReadWriter[RemorphError] = macroRW

  def merge(l: RemorphError, r: RemorphError): RemorphError = (l, r) match {
    case (ls: MultipleErrors, rs: MultipleErrors) => RemorphErrors(ls.errors ++ rs.errors)
    case (ls: MultipleErrors, r: SingleError) => RemorphErrors(ls.errors :+ r)
    case (l: SingleError, rs: MultipleErrors) => RemorphErrors(l +: rs.errors)
    case (l: SingleError, r: SingleError) => RemorphErrors(Seq(l, r))
  }
}

case class RemorphErrors(errors: Seq[SingleError]) extends RemorphError with MultipleErrors {
  override def msg: String = s"Multiple errors: ${errors.map(_.msg).mkString(", ")}"
}

object RemorphErrors {
  implicit val rw: ReadWriter[RemorphErrors] = macroRW
}

case class ParsingError(
    line: Int,
    charPositionInLine: Int,
    msg: String,
    offendingTokenWidth: Int,
    offendingTokenText: String,
    offendingTokenName: String,
    ruleName: String)
    extends RemorphError
    with SingleError

object ParsingError {
  implicit val errorDetailRW: ReadWriter[ParsingError] = macroRW
}

case class ParsingErrors(errors: Seq[ParsingError]) extends RemorphError with MultipleErrors {
  override def msg: String = s"Parsing errors: ${errors.map(_.msg).mkString(", ")}"
}

case class VisitingError(cause: Throwable) extends RemorphError with SingleError {
  override def msg: String = s"Visiting error: ${cause.getMessage}"
}

case class OptimizingError(cause: Throwable) extends RemorphError with SingleError {
  override def msg: String = s"Optimizing error: ${cause.getMessage}"
}

case class UnexpectedNode(offendingNode: TreeNode[_]) extends RemorphError with SingleError {
  override def msg: String = s"Unexpected node of class ${offendingNode.getClass.getSimpleName}"
}

object UnexpectedNode {
  implicit val unexpectedNodeRW: ReadWriter[UnexpectedNode] = macroRW
  implicit val treeNodeRW: ReadWriter[TreeNode[_]] = upickle.default.readwriter[TreeNode[_]]
}

case class UnexpectedTableAlteration(offendingTableAlteration: TableAlteration) extends RemorphError with SingleError {
  override def msg: String = s"Unexpected table alteration $offendingTableAlteration"
}

object UnexpectedTableAlteration {
  implicit val unexpectedTableAlterationRW: ReadWriter[UnexpectedTableAlteration] = macroRW
  implicit val tableAlterationRW: ReadWriter[TableAlteration] = upickle.default.readwriter[TableAlteration]
}

case class UnsupportedGroupType(offendingGroupType: GroupType) extends RemorphError with SingleError {
  override def msg: String = s"Unsupported group type $offendingGroupType"
}

object UnsupportedGroupType {
  implicit val unsupportedGroupTypeRW: ReadWriter[UnsupportedGroupType] = macroRW
  implicit val groupTypeRW: ReadWriter[GroupType] = upickle.default.readwriter[GroupType]
}

case class UnsupportedDataType(offendingDataType: DataType) extends RemorphError with SingleError {
  override def msg: String = s"Unsupported data type $offendingDataType"
}

object UnsupportedDataType {
  implicit val unsupportedDataTypeRW: ReadWriter[UnsupportedDataType] = macroRW
  implicit val dataTypeRW: ReadWriter[DataType] = upickle.default.readwriter[DataType]
}

case class WrongNumberOfArguments(functionName: String, got: Int, expectationMessage: String) extends RemorphError with SingleError {
  override def msg: String =
    s"Wrong number of arguments for $functionName: got $got, expected $expectationMessage"
}

object WrongNumberOfArguments {
  implicit val wrongNumberOfArgumentsRW: ReadWriter[WrongNumberOfArguments] = macroRW
}

case class UnsupportedArguments(functionName: String, arguments: Seq[Expression]) extends RemorphError with SingleError {
  override def msg: String = s"Unsupported argument(s) to $functionName"
}

object UnsupportedArguments {
  implicit val unsupportedArgumentsRW: ReadWriter[UnsupportedArguments] = macroRW
  implicit val expressionRW: ReadWriter[Expression] = upickle.default.readwriter[Expression]
}

case class UnsupportedDateTimePart(expression: Expression) extends RemorphError with SingleError {
  override def msg: String = s"Unsupported date/time part specification: $expression"
}

object UnsupportedDateTimePart {
  implicit val unsupportedDateTimePartRW: ReadWriter[UnsupportedDateTimePart] = macroRW
  implicit val expressionRW: ReadWriter[Expression] = upickle.default.readwriter[Expression]
}

case class PlanGenerationFailure(exception: String, msg: String) extends RemorphError

object PlanGenerationFailure {
  implicit val planGenerationFailureRW: ReadWriter[PlanGenerationFailure] = macroRW
}

case class TranspileFailure(exception: String, msg: String) extends RemorphError

object TranspileFailure {
  implicit val transpileFailureRW: ReadWriter[TranspileFailure] = macroRW
}

case class UncaughtException(exception: Throwable) extends RemorphError with SingleError {
  override def msg: String = exception.getMessage
}

case class UnexpectedOutput(expected: String, actual: String) extends RemorphError with SingleError {
  override def msg: String =
    s"""
       |=== Unexpected output (expected vs actual) ===
       |${Strings.sideBySide(expected, actual).mkString("\n")}
       |""".stripMargin
}
