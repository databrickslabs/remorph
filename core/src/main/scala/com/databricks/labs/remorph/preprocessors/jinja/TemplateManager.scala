package com.databricks.labs.remorph.preprocessors.jinja

import scala.collection.mutable

class TemplateManager {
  private val templates = mutable.Map[String, TemplateElement]()
  private var counter = 0

  def add(template: TemplateElement): String = {
    counter += 1
    val key = f"_!Jinja$counter%04d"
    templates(key) = template
    key
  }

  def get(key: String): Option[TemplateElement] = {
    templates.get(key)
  }
}
