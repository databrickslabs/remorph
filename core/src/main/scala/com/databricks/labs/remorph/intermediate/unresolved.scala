package com.databricks.labs.remorph.intermediate

trait UnwantedInGeneratorInput

trait Unresolved[T] {
  def ruleText: String
  def message: String
  def ruleName: String
  def tokenName: Option[String]

  def annotate(newRuleName: String, newTokenName: Option[String]): T
}
case class UnresolvedRelation(
    ruleText: String,
    message: String = "",
    ruleName: String = "rule name undetermined",
    tokenName: Option[String] = None)
    extends LeafNode
    with UnwantedInGeneratorInput
    with Unresolved[UnresolvedRelation] {
  override def output: Seq[Attribute] = Seq.empty

  override def annotate(newRuleName: String, newTokenName: Option[String]): UnresolvedRelation =
    copy(ruleName = newRuleName, tokenName = newTokenName)
}

case class UnresolvedExpression(
    ruleText: String,
    message: String,
    ruleName: String = "rule name undetermined",
    tokenName: Option[String] = None)
    extends LeafExpression
    with UnwantedInGeneratorInput
    with Unresolved[UnresolvedExpression] {
  override def dataType: DataType = UnresolvedType

  override def annotate(newRuleName: String, newTokenName: Option[String]): UnresolvedExpression =
    copy(ruleName = newRuleName, tokenName = newTokenName)
}

case class UnresolvedAttribute(
    unparsed_identifier: String,
    plan_id: Long = 0,
    is_metadata_column: Boolean = false,
    ruleText: String = "",
    message: String = "",
    ruleName: String = "rule name undetermined",
    tokenName: Option[String] = None)
    extends LeafExpression
    with Unresolved[UnresolvedAttribute] {
  override def dataType: DataType = UnresolvedType

  override def annotate(newRuleName: String, newTokenName: Option[String]): UnresolvedAttribute =
    copy(ruleName = newRuleName, tokenName = newTokenName)
}

case class UnresolvedFunction(
    function_name: String,
    arguments: Seq[Expression],
    is_distinct: Boolean,
    is_user_defined_function: Boolean,
    has_incorrect_argc: Boolean = false,
    ruleText: String,
    message: String,
    ruleName: String = "rule name undetermined",
    tokenName: Option[String] = None)
    extends Expression
    with Unresolved[UnresolvedFunction] {
  override def children: Seq[Expression] = arguments
  override def dataType: DataType = UnresolvedType

  override def annotate(newRuleName: String, newTokenName: Option[String]): UnresolvedFunction =
    copy(ruleName = newRuleName, tokenName = newTokenName)
}

case class UnresolvedStar(
    unparsed_target: String,
    ruleText: String,
    message: String,
    ruleName: String = "rule name undetermined",
    tokenName: Option[String] = None)
    extends LeafExpression
    with Unresolved[UnresolvedStar] {
  override def dataType: DataType = UnresolvedType

  override def annotate(newRuleName: String, newTokenName: Option[String]): UnresolvedStar =
    copy(ruleName = newRuleName, tokenName = newTokenName)
}

case class UnresolvedRegex(
    col_name: String,
    plan_id: Long,
    ruleText: String,
    message: String,
    ruleName: String = "rule name undetermined",
    tokenName: Option[String] = None)
    extends LeafExpression
    with Unresolved[UnresolvedRegex] {
  override def dataType: DataType = UnresolvedType

  override def annotate(newRuleName: String, newTokenName: Option[String]): UnresolvedRegex =
    copy(ruleName = newRuleName, tokenName = newTokenName)
}

case class UnresolvedExtractValue(
    child: Expression,
    extraction: Expression,
    ruleText: String,
    message: String,
    ruleName: String = "rule name undetermined",
    tokenName: Option[String] = None)
    extends Expression
    with Unresolved[UnresolvedExtractValue] {
  override def children: Seq[Expression] = child :: extraction :: Nil
  override def dataType: DataType = UnresolvedType

  override def annotate(newRuleName: String, newTokenName: Option[String]): UnresolvedExtractValue =
    copy(ruleName = newRuleName, tokenName = newTokenName)
}

case class UnresolvedCommand(
    ruleText: String,
    message: String,
    ruleName: String = "rule name undetermined",
    tokenName: Option[String] = None)
    extends Catalog
    with Command
    with UnwantedInGeneratorInput
    with Unresolved[UnresolvedCommand] {
  override def output: Seq[Attribute] = Seq.empty
  override def children: Seq[LogicalPlan] = Seq.empty

  override def annotate(newRuleName: String, newTokenName: Option[String]): UnresolvedCommand =
    copy(ruleName = newRuleName, tokenName = newTokenName)
}

case class UnresolvedCatalog(
    ruleText: String,
    message: String,
    ruleName: String = "rule name undetermined",
    tokenName: Option[String] = None)
    extends Catalog
    with UnwantedInGeneratorInput
    with Unresolved[UnresolvedCatalog] {
  override def output: Seq[Attribute] = Seq.empty
  override def children: Seq[LogicalPlan] = Seq.empty

  override def annotate(newRuleName: String, newTokenName: Option[String]): UnresolvedCatalog =
    copy(ruleName = newRuleName, tokenName = newTokenName)
}

case class UnresolvedCTAS(
    ruleText: String,
    message: String,
    ruleName: String = "rule name undetermined",
    tokenName: Option[String] = None)
    extends Catalog
    with Command
    with UnwantedInGeneratorInput
    with Unresolved[UnresolvedCTAS] {
  override def output: Seq[Attribute] = Seq.empty
  override def children: Seq[LogicalPlan] = Seq.empty

  override def annotate(newRuleName: String, newTokenName: Option[String]): UnresolvedCTAS =
    copy(ruleName = newRuleName, tokenName = newTokenName)
}

case class UnresolvedModification(
    ruleText: String,
    message: String,
    ruleName: String = "rule name undetermined",
    tokenName: Option[String] = None)
    extends Modification
    with UnwantedInGeneratorInput
    with Unresolved[UnresolvedModification] {
  override def output: Seq[Attribute] = Seq.empty
  override def children: Seq[LogicalPlan] = Seq.empty

  override def annotate(newRuleName: String, newTokenName: Option[String]): UnresolvedModification =
    copy(ruleName = newRuleName, tokenName = newTokenName)
}
