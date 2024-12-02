package com.databricks.labs.remorph.intermediate

import com.databricks.labs.remorph.Phase
import com.databricks.labs.remorph.utils.Strings

sealed trait RemorphError {
  def msg: String
}

sealed trait SingleError extends RemorphError

sealed trait MultipleErrors extends RemorphError {
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
    message: String,
    offendingTokenWidth: Int,
    offendingTokenText: String,
    offendingTokenName: String,
    ruleName: String)
    extends RemorphError
    with SingleError {
  override def msg: String =
    s"Parsing error starting at $line:$charPositionInLine involving rule '$ruleName' and" +
      s" token '$offendingTokenText'($offendingTokenName): $message"
}

case class ParsingErrors(errors: Seq[ParsingError]) extends RemorphError with MultipleErrors {
  override def msg: String = s"Parsing errors: ${errors.map(_.msg).mkString(", ")}"
}

// TODO: If we wish to preserve the whole node in say JSON output, we will need to accept TreeNodew[_] and deal with
//       implicits for TreeNode[_] as well
case class UnexpectedNode(offendingNode: String) extends RemorphError with SingleError {
  override def msg: String = s"Unexpected node of class ${offendingNode}"
}

case class UnexpectedTableAlteration(offendingTableAlteration: String) extends RemorphError with SingleError {
  override def msg: String = s"Unexpected table alteration $offendingTableAlteration"
}

case class UnsupportedGroupType(offendingGroupType: String) extends RemorphError with SingleError {
  override def msg: String = s"Unsupported group type $offendingGroupType"
}

case class UnsupportedDataType(offendingDataType: String) extends RemorphError with SingleError {
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

case class PlanGenerationFailure(exception: Throwable) extends RemorphError with SingleError {
  override def msg: String = s"PlanGenerationFailure: ${exception.getClass.getSimpleName}, ${exception.getMessage}"
}

case class TranspileFailure(exception: Throwable) extends RemorphError with SingleError {
  override def msg: String = s"TranspileFailure: ${exception.getClass.getSimpleName}, ${exception.getMessage}"
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

case class IncoherentState(currentPhase: Phase, expectedPhase: Class[_]) extends RemorphError with SingleError {
  override def msg: String =
    s"Incoherent state: current phase is ${currentPhase.getClass.getSimpleName} but should be ${expectedPhase.getSimpleName}"
}
