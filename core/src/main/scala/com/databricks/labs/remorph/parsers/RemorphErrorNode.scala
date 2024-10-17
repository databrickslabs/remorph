package com.databricks.labs.remorph.parsers

import org.antlr.v4.runtime.Token
import org.antlr.v4.runtime.tree.{ErrorNodeImpl, ParseTree, ParseTreeVisitor}

import java.util

class RemorphErrorNode(token: Token) extends ErrorNodeImpl(token) {
  private val children: util.List[ParseTree] = new util.ArrayList[ParseTree]()

  def addChild(child: ParseTree): Unit = {
    children.add(child)
  }

  override def accept[T](visitor: ParseTreeVisitor[_ <: T]): T = {
    visitor.visitErrorNode(this)
  }

  override def getChildCount: Int = {
    children.size()
  }

  override def getChild(i: Int): ParseTree = {
    children.get(i)
  }
}
