package com.databricks.labs.remorph.generators.py
import com.databricks.labs.remorph.{intermediate => ir}
import com.databricks.labs.remorph.generators.GeneratorContext
import com.databricks.labs.remorph.intermediate.{Expression, Name}

class StatementGenerator(val exprs: ExpressionGenerator) extends BasePythonGenerator[Statement] {
  override def generate(ctx: GeneratorContext, tree: Statement): Python = tree match {
    case Module(children) => py"${children map generate(ctx, _)}"
    case FunctionDef(name, args, children, decorators) =>
      functionDef(ctx, name, args, children, decorators)
    case ClassDef(name, bases, children, decorators) =>
      classDef(ctx, name, bases, children, decorators)
    case Assign(targets, value) => py"${exprs.many(ctx, targets)} = ${exprs.generate(ctx, value)}"
    case For(target, iter, body, orElse) =>
      forStmt(ctx, target, iter, body, orElse)
    case While(test, body, orElse) =>
      whileStmt(ctx, test, body, orElse)
    case If(test, body, orElse) =>
      ifStmt(ctx, test, body, orElse)
    case With(context, vars, children) =>
      withStmt(ctx, context, vars, children)
    case TryExcept(body, handlers, orElse) =>
      tryExcept(ctx, body, handlers, orElse)
    case ExceptHandler(expr, name, children) =>
      exceptHandler(ctx, expr, name, children)
    case Return(value) => py"return ${value map exprs.generate(ctx, _)}"
    case Delete(targets) => py"del ${exprs.many(ctx, targets)}"
    case Pass => py"pass"
    case Break => py"break"
    case Continue => py"continue"
    case _ => partialResult(tree)
  }

  private def exceptHandler(
      ctx: GeneratorContext,
      expr: Option[Expression],
      name: Option[Name],
      children: Seq[Statement]): Python = {
    val exprStr = expr.map(exprs.generate(ctx, _)).mkString
    val nameStr = name.map(exprs.generate(ctx, _)).mkString
    val childrenStr = children map generate(ctx.nest, _)
    py"except $exprStr as $nameStr:\n$childrenStr"
  }

  private def tryExcept(
      ctx: GeneratorContext,
      body: Seq[Statement],
      handlers: Seq[ExceptHandler],
      orElse: Seq[Statement]): Python = {
    val bodyStr = body map generate(ctx.nest, _)
    val handlersStr = handlers map generate(ctx.nest, _)
    val orElseStr = orElse map generate(ctx.nest, _)
    py"try:\n$bodyStr\n$handlersStr\n$orElseStr"
  }

  private def withStmt(
      ctx: GeneratorContext,
      context: Expression,
      vars: Option[Expression],
      children: Seq[Statement]): Python = {
    val varsStr = vars.map(exprs.generate(ctx, _)).mkString
    val childrenStr = children map generate(ctx.nest, _)
    py"with ${exprs.generate(ctx, context)}$varsStr:\n$childrenStr"
  }

  private def ifStmt(ctx: GeneratorContext, test: Expression, body: Seq[Statement], orElse: Seq[Statement]): Python = {
    val bodyStr = body map generate(ctx.nest, _)
    val orElseStr = orElse map generate(ctx.nest, _)
    py"if ${exprs.generate(ctx, test)}:\n$bodyStr\n$orElseStr"
  }

  private def whileStmt(
      ctx: GeneratorContext,
      test: Expression,
      body: Seq[Statement],
      orElse: Seq[Statement]): Python = {
    val bodyStr = body map generate(ctx.nest, _)
    val orElseStr = orElse map generate(ctx.nest, _)
    py"while ${exprs.generate(ctx, test)}:\n$bodyStr\n$orElseStr"
  }

  private def forStmt(
      ctx: GeneratorContext,
      target: Expression,
      iter: Expression,
      body: Seq[Statement],
      orElse: Seq[Statement]): Python = {
    val bodyStr = body map generate(ctx.nest, _)
    val orElseStr = orElse map generate(ctx.nest, _)
    py"for ${exprs.generate(ctx, target)} in ${exprs.generate(ctx, iter)}:\n$bodyStr\n$orElseStr"
  }

  private def classDef(
      ctx: GeneratorContext,
      name: ir.Name,
      bases: Seq[ir.Expression],
      children: Seq[Statement],
      deco: Seq[ir.Expression]): Python = {
    val extend = bases.map(exprs.generate(ctx, _)).maybeMkPython("(", ", ", ")")
    val members = children map generate(ctx.nest, _)
    py"${decorators(ctx, deco)}class $name$extend:\n$members"
  }

  private def functionDef(
      ctx: GeneratorContext,
      name: ir.Name,
      args: Arguments,
      children: Seq[Statement],
      deco: Seq[ir.Expression]): Python = {
    val decoratorsStr = decorators(ctx, deco)
    val childrenStr = children map py"${generate(ctx.nest, _)}"
    py"${decoratorsStr}def $name(${exprs.arguments(ctx, args)}):\n$childrenStr"
  }

  private def decorators(ctx: GeneratorContext, decorators: Seq[Expression]): Python = {
    decorators map py"@${exprs.generate(ctx, _)}\n"
  }
}
