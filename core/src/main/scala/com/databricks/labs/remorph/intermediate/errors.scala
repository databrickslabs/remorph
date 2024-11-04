package com.databricks.labs.remorph.intermediate

import com.databricks.labs.remorph.Phase
import com.databricks.labs.remorph.utils.Strings
import upickle.default._

import java.io.{PrintWriter, StringWriter}

sealed trait RemorphError {
  def msg: String
}

sealed trait SingleError extends RemorphError

sealed trait MultipleErrors extends RemorphError {
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
  implicit val singleErrorSeqRW: ReadWriter[Seq[SingleError]] = upickle.default.readwriter[Seq[SingleError]]
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

case class ParsingErrors(errors: Seq[ParsingError]) extends RemorphError with MultipleErrors {
  override def msg: String = s"Parsing errors: ${errors.map(_.msg).mkString(", ")}"
}

object ParsingErrors {
  implicit val rw: ReadWriter[ParsingErrors] = macroRW
}

// TODO: If we wish to preserve the whole node in say JSON output, we will need to accept TreeNodew[_] and deal with
//       implicits for TreeNode[_] as well
case class UnexpectedNode(offendingNode: String) extends RemorphError with SingleError {
  override def msg: String = s"Unexpected node of class ${offendingNode}"
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

case class WrongNumberOfArguments(functionName: String, got: Int, expectationMessage: String)
    extends RemorphError
    with SingleError {
  override def msg: String =
    s"Wrong number of arguments for $functionName: got $got, expected $expectationMessage"
}

object WrongNumberOfArguments {
  implicit val rw: ReadWriter[WrongNumberOfArguments] = macroRW
}

case class UnsupportedArguments(functionName: String, arguments: Seq[Expression])
    extends RemorphError
    with SingleError {
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

case class PlanGenerationFailure(exception: Throwable) extends RemorphError with SingleError {
  override def msg: String = s"PlanGenerationFailure: ${exception.getClass.getSimpleName}, ${exception.getMessage}"
}
object PlanGenerationFailure {
  implicit val rw: ReadWriter[PlanGenerationFailure] = macroRW
  implicit val rwExcept: ReadWriter[Throwable] = upickle.default
    .readwriter[ujson.Value]
    .bimap[Throwable](
      e => {
        val sw = new StringWriter
        e.printStackTrace(new PrintWriter(sw))
        ujson.Str(
          s"Plan generation failure with exception: ${e.getClass.getSimpleName} - ${e.getMessage}\n${sw.toString}")
      },
      _ => null.asInstanceOf[Throwable] // Deserialize to null
    )
}

case class TranspileFailure(exception: Throwable) extends RemorphError with SingleError {
  override def msg: String = s"TranspileFailure: ${exception.getClass.getSimpleName}, ${exception.getMessage}"
}

object TranspileFailure {
  implicit val rw: ReadWriter[TranspileFailure] = macroRW
  implicit val rwExcept: ReadWriter[Throwable] = upickle.default
    .readwriter[ujson.Value]
    .bimap[Throwable](
      e => {
        val sw = new StringWriter
        e.printStackTrace(new PrintWriter(sw))
        ujson.Str(
          s"Transpilation failure with exception: ${e.getClass.getSimpleName} - ${e.getMessage}\n${sw.toString}")
      },
      _ => null.asInstanceOf[Throwable] // Deserialize to null
    )
}

case class UncaughtException(exception: Throwable) extends RemorphError with SingleError {
  override def msg: String = exception.getMessage
}

object UncaughtException {
  implicit val rw: ReadWriter[UncaughtException] = macroRW
  implicit val rwExcept: ReadWriter[Throwable] = upickle.default
    .readwriter[ujson.Value]
    .bimap[Throwable](
      e => {
        val sw = new StringWriter
        e.printStackTrace(new PrintWriter(sw))
        ujson.Str(s"Exception: ${e.getClass.getSimpleName}, ${e.getMessage}, ${sw.toString}")
      },
      _ => null.asInstanceOf[Throwable] // Deserialize to null
    )
}

case class UnexpectedOutput(expected: String, actual: String) extends RemorphError with SingleError {
  override def msg: String =
    s"""
       |=== Unexpected output (expected vs actual) ===
       |${Strings.sideBySide(expected, actual).mkString("\n")}
       |""".stripMargin
}

object UnexpectedOutput {
  implicit val rw: ReadWriter[UnexpectedOutput] = macroRW
}

case class IncoherentState(currentPhase: Phase, expectedPhase: Class[_]) extends RemorphError with SingleError {
  override def msg: String =
    s"Incoherent state: current phase is ${currentPhase.getClass.getSimpleName} but should be ${expectedPhase.getSimpleName}"
}

object IncoherentState {
  implicit val rw: ReadWriter[IncoherentState] = upickle.default
    .readwriter[ujson.Value]
    .bimap[IncoherentState](
      is => ujson.Str(is.msg),
      _ => null.asInstanceOf[IncoherentState] // Deserialize to null, we don't expect to deserialize errors
    )
}
