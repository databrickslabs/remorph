package com.databricks.labs.remorph.intermediate

import com.databricks.labs.remorph.utils.Strings
import upickle.default._

sealed trait RemorphError {
  def msg: String
}

object RemorphError {
  implicit val remorphErrorRW: ReadWriter[RemorphError] = macroRW
  // implicit val remorphErrorListRW: ReadWriter[List[RemorphError]] = upickle.default.readwriter[List[RemorphError]]
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

object ParsingError {
  implicit val errorDetailRW: ReadWriter[ParsingError] = macroRW
}

case class ParsingErrors(errors: Seq[ParsingError]) extends RemorphError {
  override def msg: String = s"Parsing errors: ${errors.map(_.msg).mkString(", ")}"
}

case class VisitingError(cause: Throwable) extends RemorphError {
  override def msg: String = s"Visiting error: ${cause.getMessage}"
}

case class OptimizingError(cause: Throwable) extends RemorphError {
  override def msg: String = s"Optimizing error: ${cause.getMessage}"
}

case class UnexpectedNode(offendingNode: TreeNode[_]) extends RemorphError {
  override def msg: String = s"Unexpected node of class ${offendingNode.getClass.getSimpleName}"
}

object UnexpectedNode {
  implicit val unexpectedNodeRW: ReadWriter[UnexpectedNode] = macroRW
  implicit val treeNodeRW: ReadWriter[TreeNode[_]] = upickle.default.readwriter[TreeNode[_]]
}

case class UnexpectedTableAlteration(offendingTableAlteration: TableAlteration) extends RemorphError {
  override def msg: String = s"Unexpected table alteration $offendingTableAlteration"
}

object UnexpectedTableAlteration {
  implicit val unexpectedTableAlterationRW: ReadWriter[UnexpectedTableAlteration] = macroRW
  implicit val tableAlterationRW: ReadWriter[TableAlteration] = upickle.default.readwriter[TableAlteration]
}

case class UnsupportedGroupType(offendingGroupType: GroupType) extends RemorphError {
  override def msg: String = s"Unsupported group type $offendingGroupType"
}

object UnsupportedGroupType {
  implicit val unsupportedGroupTypeRW: ReadWriter[UnsupportedGroupType] = macroRW
  implicit val groupTypeRW: ReadWriter[GroupType] = upickle.default.readwriter[GroupType]
}

case class UnsupportedDataType(offendingDataType: DataType) extends RemorphError {
  override def msg: String = s"Unsupported data type $offendingDataType"
}

object UnsupportedDataType {
  implicit val unsupportedDataTypeRW: ReadWriter[UnsupportedDataType] = macroRW
  implicit val dataTypeRW: ReadWriter[DataType] = upickle.default.readwriter[DataType]
}

case class WrongNumberOfArguments(functionName: String, got: Int, expectationMessage: String) extends RemorphError {
  override def msg: String =
    s"Wrong number of arguments for $functionName: got $got, expected $expectationMessage"
}

object WrongNumberOfArguments {
  implicit val wrongNumberOfArgumentsRW: ReadWriter[WrongNumberOfArguments] = macroRW
}

case class UnsupportedArguments(functionName: String, arguments: Seq[Expression]) extends RemorphError {
  override def msg: String = s"Unsupported argument(s) to $functionName"
}

object UnsupportedArguments {
  implicit val unsupportedArgumentsRW: ReadWriter[UnsupportedArguments] = macroRW
  implicit val expressionRW: ReadWriter[Expression] = upickle.default.readwriter[Expression]
}

case class UnsupportedDateTimePart(expression: Expression) extends RemorphError {
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

case class UncaughtException(exception: Throwable) extends RemorphError {
  override def msg: String = exception.getMessage
}

case class UnexpectedOutput(expected: String, actual: String) extends RemorphError {
  override def msg: String =
    s"""
       |=== Unexpected output (expected vs actual) ===
       |${Strings.sideBySide(expected, actual).mkString("\n")}
       |""".stripMargin
}
