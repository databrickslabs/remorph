package com.databricks.labs.remorph.preprocessors.jinja

import com.databricks.labs.remorph.intermediate.Origin

sealed trait TemplateElement {
  def origin: Origin
  def text: String
  def regex: String

  def appendText(text: String): TemplateElement = {
    this match {
      case s: StatementElement => s.copy(text = this.text + text)
      case e: ExpressionElement => e.copy(text = this.text + text)
      case c: CommentElement => c.copy(text = this.text + text)
      case l: LineElement => l.copy(text = this.text + text)
      case ls: LineStatementElement => ls.copy(text = this.text + text)
      case lc: LineCommentElement => lc.copy(text = this.text + text)
    }
  }
}

case class StatementElement(origin: Origin, text: String, regex: String) extends TemplateElement

case class ExpressionElement(origin: Origin, text: String, regex: String) extends TemplateElement

case class CommentElement(origin: Origin, text: String, regex: String) extends TemplateElement

// TODO: We don't support # line elements yet
case class LineElement(origin: Origin, text: String, regex: String) extends TemplateElement

// TODO: We don't support # line statements yet
case class LineStatementElement(origin: Origin, text: String, regex: String) extends TemplateElement

// TODO: We don't support # line comment elements yet
case class LineCommentElement(origin: Origin, text: String, regex: String) extends TemplateElement
