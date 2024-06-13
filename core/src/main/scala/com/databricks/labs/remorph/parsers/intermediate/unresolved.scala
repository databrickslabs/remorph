package com.databricks.labs.remorph.parsers.intermediate

case class UnresolvedRelation(inputText: String) extends RelationCommon

case class UnresolvedExpression(inputText: String) extends Expression {}
case class UnresolvedCommand(inputText: String) extends Command {}
case class UnresolvedCatalog(inputText: String) extends Catalog {}
case object UnknownRelation extends RelationCommon
