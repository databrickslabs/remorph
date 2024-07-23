package com.databricks.labs.remorph.parsers.intermediate

case class UnresolvedRelation(inputText: String) extends LeafNode {
  override def output: Seq[Attribute] = Seq.empty
}


case class UnresolvedStatement(inputText: String) extends Statement {}

case class UnresolvedExpression(inputText: String) extends LeafExpression {
  override def dataType: DataType = UnresolvedType
}

case class UnresolvedCommand(inputText: String) extends LeafNode with Command {
  override def output: Seq[Attribute] = Seq.empty
  override def children: Seq[LogicalPlan] = Seq.empty
}

case class UnresolvedCatalog(inputText: String) extends Catalog {
  override def output: Seq[Attribute] = Seq.empty
  override def children: Seq[LogicalPlan] = Seq.empty
}

