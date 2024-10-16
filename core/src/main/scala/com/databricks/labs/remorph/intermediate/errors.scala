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
  implicit val rw: ReadWriter[RemorphError] = ReadWriter.merge(
    ParsingError.rw,
    ParsingErrors.rw,
    UnexpectedNode.rw,
    UnexpectedTableAlteration.rw,
    UnsupportedGroupType.rw,
    UnsupportedDataType.rw,
    WrongNumberOfArguments.rw,
    UnsupportedArguments.rw,
    UnsupportedDateTimePart.rw,
    PlanGenerationFailure.rw,
    TranspileFailure.rw)

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
  implicit val rw: ReadWriter[ParsingError] = macroRW
}

case class ParsingErrors(errors: Seq[ParsingError]) extends RemorphError {
  override def msg: String = s"Parsing errors: ${errors.map(_.msg).mkString(", ")}"
}

object ParsingErrors {
  implicit val rw: ReadWriter[ParsingErrors] = macroRW
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
  implicit val rw: ReadWriter[UnexpectedNode] = macroRW
}

case class UnexpectedTableAlteration(offendingTableAlteration: String) extends RemorphError with SingleError {
  override def msg: String = s"Unexpected table alteration $offendingTableAlteration"
}

object UnexpectedTableAlteration {
  implicit val rw: ReadWriter[UnexpectedTableAlteration] = macroRW
}

case class UnsupportedGroupType(offendingGroupType: String) extends RemorphError with SingleError {
  override def msg: String = s"Unsupported group type $offendingGroupType"
}

object UnsupportedGroupType {
  implicit val rw: ReadWriter[UnsupportedGroupType] = macroRW
}

case class UnsupportedDataType(offendingDataType: String) extends RemorphError with SingleError {
  override def msg: String = s"Unsupported data type $offendingDataType"
}
object UnsupportedDataType {
  implicit val rw: ReadWriter[UnsupportedDataType] = macroRW
}

case class WrongNumberOfArguments(functionName: String, got: Int, expectationMessage: String) extends RemorphError with SingleError {
  override def msg: String =
    s"Wrong number of arguments for $functionName: got $got, expected $expectationMessage"
}

object WrongNumberOfArguments {
  implicit val rw: ReadWriter[WrongNumberOfArguments] = macroRW
}

case class UnsupportedArguments(functionName: String, arguments: Seq[Expression]) extends RemorphError with SingleError {
  override def msg: String = s"Unsupported argument(s) to $functionName"
}

@upickle.implicits.serializeDefaults(false)
object UnsupportedArguments {
  // NOte that we don't serialize all the arguments because we would have to adorn the Expression trait with a RW
  // including all its sub classes
  implicit val rw: ReadWriter[UnsupportedArguments] = macroRW
  implicit val rwE: ReadWriter[Expression] = readwriter[ujson.Value].bimap[Expression](
    _ => ujson.Null, // Serialize to "null" as we don't need to serialize the arguments right now
    _ => null.asInstanceOf[Expression] // Deserialize to null
  )
}

case class UnsupportedDateTimePart(expression: Expression) extends RemorphError with SingleError {
  override def msg: String = s"Unsupported date/time part specification: $expression"
}
object UnsupportedDateTimePart {
  implicit val rw: ReadWriter[UnsupportedDateTimePart] = macroRW
  implicit val expressionRW: ReadWriter[Expression] = upickle.default.readwriter[Expression]
}

case class PlanGenerationFailure(exception: String, messsage: String) extends RemorphError {
  override def msg: String = s"PlanGenerationFailure: $exception, $messsage"
}
object PlanGenerationFailure {
  implicit val rw: ReadWriter[PlanGenerationFailure] = macroRW
}

case class TranspileFailure(exception: String, message: String) extends RemorphError {
  override def msg: String = s"TranspileFailure: $exception, $message"
}
object TranspileFailure {
  implicit val rw: ReadWriter[TranspileFailure] = macroRW
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
