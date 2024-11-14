package com.databricks.labs.remorph.preprocessor.jinga

import com.databricks.labs.remorph.intermediate.Origin

sealed trait TemplateElement {
  def origin: Origin
  def text: String
  def hasPrecedingWS: Boolean
  def hasTrailingWS: Boolean

  def appendText(text: String): TemplateElement = {
    this match {
      case s: StatementElement => s.copy(text = this.text + text)
      case e: ExpressionElement => e.copy(text = this.text + text)
      case c: CommentElement => c.copy(text = this.text + text)
      case l: LineElement => l.copy(text = this.text + text)
      case ls: LineStatementElement => ls.copy(text = this.text + text)
      case lc: LineCommonElement => lc.copy(text = this.text + text)
    }
  }
}

case class StatementElement(
    origin: Origin,
    text: String,
    hasPrecedingWS: Boolean = false,
    hasTrailingWS: Boolean = false)
    extends TemplateElement

case class ExpressionElement(
    origin: Origin,
    text: String,
    hasPrecedingWS: Boolean = false,
    hasTrailingWS: Boolean = false)
    extends TemplateElement

case class CommentElement(origin: Origin, text: String, hasPrecedingWS: Boolean = false, hasTrailingWS: Boolean = false)
    extends TemplateElement

case class LineElement(origin: Origin, text: String, hasPrecedingWS: Boolean = false, hasTrailingWS: Boolean = false)
    extends TemplateElement

case class LineStatementElement(
    origin: Origin,
    text: String,
    hasPrecedingWS: Boolean = false,
    hasTrailingWS: Boolean = false)
    extends TemplateElement

case class LineCommonElement(
    origin: Origin,
    text: String,
    hasPrecedingWS: Boolean = false,
    hasTrailingWS: Boolean = false)
    extends TemplateElement
