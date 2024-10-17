package com.databricks.labs.remorph.intermediate

import com.databricks.labs.remorph.utils.Strings
import upickle.default._

trait RemorphError {
  def msg: String
}

trait SingleError extends RemorphError

trait MultipleErrors extends RemorphError {
  def errors: Seq[SingleError]
}

object RemorphError {
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

case class UnexpectedTableAlteration(offendingTableAlteration: TableAlteration) extends RemorphError with SingleError {
  override def msg: String = s"Unexpected table alteration $offendingTableAlteration"
}

case class UnsupportedGroupType(offendingGroupType: GroupType) extends RemorphError with SingleError {
  override def msg: String = s"Unsupported group type $offendingGroupType"
}

case class UnsupportedDataType(offendingDataType: DataType) extends RemorphError with SingleError {
  override def msg: String = s"Unsupported data type $offendingDataType"
}

case class WrongNumberOfArguments(functionName: String, got: Int, expectationMessage: String)
    extends RemorphError
    with SingleError {
  override def msg: String =
    s"Wrong number of arguments for $functionName: got $got, expected $expectationMessage"
}

case class UnsupportedArguments(functionName: String, arguments: Seq[Expression])
    extends RemorphError
    with SingleError {
  override def msg: String = s"Unsupported argument(s) to $functionName"
}

case class UnsupportedDateTimePart(expression: Expression) extends RemorphError with SingleError {
  override def msg: String = s"Unsupported date/time part specification: $expression"
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
