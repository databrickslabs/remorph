package com.databricks.labs.remorph.generators.py.rules

import com.databricks.labs.remorph.{intermediate => ir}
import com.databricks.labs.remorph.generators.py

case class ImportAliasSideEffect(expr: ir.Expression, module: String, alias: Option[String] = None)
    extends ir.Expression {
  override def children: Seq[ir.Expression] = Seq(expr)
  override def dataType: ir.DataType = ir.UnresolvedType
}

case class ImportClassSideEffect(expr: ir.Expression, module: String, klass: String) extends ir.Expression {
  override def children: Seq[ir.Expression] = Seq(expr)
  override def dataType: ir.DataType = ir.UnresolvedType
}

// to be called after PySparkExpressions
class ImportClasses extends ir.Rule[py.Statement] {
  override def apply(plan: py.Statement): py.Statement = plan match {
    case py.Module(children) =>
      var imports = Seq.empty[py.Import]
      var importsFrom = Seq.empty[py.ImportFrom]
      val body = children map { statement =>
        statement transformAllExpressions {
          case ImportAliasSideEffect(expr, module, alias) =>
            imports = imports :+ py.Import(Seq(py.Alias(ir.Name(module), alias.map(ir.Name))))
            expr
          case ImportClassSideEffect(expr, module, klass) =>
            importsFrom = importsFrom :+ py.ImportFrom(Some(ir.Name(module)), Seq(py.Alias(ir.Name(klass))))
            expr
        }
      }
      py.Module(imports.distinct ++ importsFrom.distinct ++ body)
  }
}
