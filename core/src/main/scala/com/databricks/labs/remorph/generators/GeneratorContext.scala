package com.databricks.labs.remorph.generators

import com.databricks.labs.remorph.{intermediate => ir}

case class GeneratorContext(
    // needed for sql"EXISTS (${ctx.logical.generate(ctx, subquery)})" in SQLGenerator
    logical: Generator[ir.LogicalPlan, String],
    maxLineWidth: Int = 120,
    private val indent: Int = 0,
    private val layer: Int = 0,
    private val joins: Int = 0,
    wrapLiteral: Boolean = true) {
  def nest: GeneratorContext =
    GeneratorContext(logical, maxLineWidth = maxLineWidth, joins = joins, layer = layer, indent = indent + 1)

  def unnest: GeneratorContext =
    GeneratorContext(
      logical,
      maxLineWidth = maxLineWidth,
      joins = joins,
      layer = layer,
      indent = Math.max(0, indent - 1))

  def ws: String = "  " * indent

  def subQuery: GeneratorContext =
    GeneratorContext(logical, maxLineWidth = maxLineWidth, joins = joins, layer = layer + 1, indent = indent + 1)

  def layerName: String = s"layer_$layer"

  def withRawLiteral: GeneratorContext =
    GeneratorContext(
      logical,
      maxLineWidth = maxLineWidth,
      joins = joins,
      indent = indent,
      layer = layer,
      wrapLiteral = false)

  def hasJoins: Boolean = joins > 0
}
