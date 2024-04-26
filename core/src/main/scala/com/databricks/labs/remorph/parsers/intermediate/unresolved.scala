package com.databricks.labs.remorph.parsers.intermediate

case class UnresolvedRelation(inputText: String) extends RelationCommon

case class UnresolvedExpression(inputText: String) extends Expression {}
case object UnknownRelation extends RelationCommon
