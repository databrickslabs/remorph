package com.databricks.labs.remorph.generators.py
import com.databricks.labs.remorph.generators.{GeneratorContext, TBAInterpolator}
import com.databricks.labs.remorph.intermediate.Expression

class StatementGenerator(private val exprs: ExpressionGenerator) extends BasePythonGenerator[Statement] {
  override def generate(ctx: GeneratorContext, tree: Statement): Python = code"${ctx.ws}${statement(ctx, tree)}"

  private def statement(ctx: GeneratorContext, tree: Statement): Python = tree match {
    case Module(children) => lines(ctx, children)
    case Alias(name, None) => e(ctx, name)
    case ExprStatement(expr) => e(ctx, expr)
    case FunctionDef(name, args, children, decorators) =>
      code"${decorate(ctx, decorators)}def ${name.name}(${exprs.arguments(ctx, args)}):\n${lines(ctx.nest, children)}"
    case ClassDef(name, bases, children, decorators) =>
      code"${decorate(ctx, decorators)}class ${name.name}${parents(ctx, bases)}:\n${lines(ctx.nest, children)}"
    case Alias(name, Some(alias)) =>
      code"${e(ctx, name)} as ${e(ctx, alias)}"
    case Import(names) =>
      code"import ${commas(ctx, names)}"
    case ImportFrom(Some(module), names, _) =>
      code"from ${e(ctx, module)} import ${commas(ctx, names)}"
    case Assign(targets, value) =>
      code"${exprs.commas(ctx, targets)} = ${e(ctx, value)}"
    case Decorator(expr) =>
      code"@${e(ctx, expr)}"
    case For(target, iter, body, orElse) =>
      code"for ${e(ctx, target)} in ${e(ctx, iter)}:\n${lines(ctx.nest, body)}${elseB(ctx, orElse)}"
    case While(test, body, orElse) =>
      code"while ${e(ctx, test)}:\n${lines(ctx.nest, body)}${elseB(ctx, orElse)}"
    case If(test, body, orElse) =>
      code"if ${e(ctx, test)}:\n${lines(ctx.nest, body)}${elseB(ctx, orElse)}"
    case With(context, body) =>
      code"with ${commas(ctx, context)}:\n${lines(ctx.nest, body)}"
    case Raise(None, None) =>
      code"raise"
    case Raise(Some(exc), None) =>
      code"raise ${e(ctx, exc)}"
    case Raise(Some(exc), Some(cause)) =>
      code"raise ${e(ctx, exc)} from ${e(ctx, cause)}"
    case Try(body, handlers, orElse, orFinally) =>
      code"try:\n${lines(ctx.nest, body)}${lines(ctx, handlers)}${elseB(ctx, orElse)}${elseB(ctx, orFinally, "finally")}"
    case Except(None, children) =>
      code"except:\n${lines(ctx.nest, children, finish = "")}"
    case Except(Some(alias), children) =>
      code"except ${generate(ctx, alias)}:\n${lines(ctx.nest, children, finish = "")}"
    case Assert(test, None) =>
      code"assert ${e(ctx, test)}"
    case Assert(test, Some(msg)) =>
      code"assert ${e(ctx, test)}, ${e(ctx, msg)}"
    case Return(None) => code"return"
    case Return(Some(value)) => code"return ${e(ctx, value)}"
    case Delete(targets) => code"del ${exprs.commas(ctx, targets)}"
    case Pass => code"pass"
    case Break => code"break"
    case Continue => code"continue"
    case _ => partialResult(tree)
  }

  private def e(ctx: GeneratorContext, expr: Expression): Python = exprs.generate(ctx, expr)

  private def lines(ctx: GeneratorContext, statements: Seq[Statement], finish: String = "\n"): Python = {
    if (statements.isEmpty) {
      code""
    } else {
      val body = statements.map(generate(ctx, _))
      val separatedItems = body.tail.foldLeft[Python](body.head) { case (agg, item) =>
        code"$agg\n$item"
      }
      code"$separatedItems$finish"
    }
  }

  // decorators need their leading whitespace trimmed and get followed by a trailing whitespace
  private def decorate(ctx: GeneratorContext, decorators: Seq[Decorator]): Python = {
    lines(ctx, decorators).map {
      case "" => ""
      case some => s"${some.trim}\n${ctx.ws}"
    }

  }

  private def elseB(ctx: GeneratorContext, orElse: Seq[Statement], branch: String = "else"): Python = orElse match {
    case Nil => code""
    case some => code"${ctx.ws}$branch:\n${lines(ctx.nest, some)}"
  }

  private def parents(ctx: GeneratorContext, names: Seq[Expression]): Python = names match {
    case Nil => code""
    case some => code"(${exprs.commas(ctx, some)})"
  }
}
