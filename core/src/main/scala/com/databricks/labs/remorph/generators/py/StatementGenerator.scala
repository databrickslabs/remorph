package com.databricks.labs.remorph.generators.py
import com.databricks.labs.remorph.OkResult
import com.databricks.labs.remorph.generators.GeneratorContext
import com.databricks.labs.remorph.intermediate.Expression

class StatementGenerator(private val exprs: ExpressionGenerator) extends BasePythonGenerator[Statement] {
  override def generate(ctx: GeneratorContext, tree: Statement): Python = py"${ctx.ws}${statement(ctx, tree)}"

  private def statement(ctx: GeneratorContext, tree: Statement): Python = tree match {
    case Module(children) => lines(ctx, children)
    case Alias(name, None) => e(ctx, name)
    case FunctionDef(name, args, children, decorators) =>
      py"${decorate(ctx, decorators)}def ${name.name}(${exprs.arguments(ctx, args)}):\n${lines(ctx.nest, children)}"
    case ClassDef(name, bases, children, decorators) =>
      py"${decorate(ctx, decorators)}class ${name.name}${parents(ctx, bases)}:\n${lines(ctx.nest, children)}"
    case Alias(name, Some(alias)) =>
      py"${e(ctx, name)} as ${e(ctx, alias)}"
    case Import(names) =>
      py"import ${commas(ctx, names)}"
    case ImportFrom(Some(module), names, _) =>
      py"from ${e(ctx, module)} import ${commas(ctx, names)}"
    case Assign(targets, value) =>
      py"${exprs.commas(ctx, targets)} = ${e(ctx, value)}"
    case Decorator(expr) =>
      py"@${e(ctx, expr)}"
    case For(target, iter, body, orElse) =>
      py"for ${e(ctx, target)} in ${e(ctx, iter)}:\n${lines(ctx.nest, body)}${elseB(ctx, orElse)}"
    case While(test, body, orElse) =>
      py"while ${e(ctx, test)}:\n${lines(ctx.nest, body)}${elseB(ctx, orElse)}"
    case If(test, body, orElse) =>
      py"if ${e(ctx, test)}:\n${lines(ctx.nest, body)}${elseB(ctx, orElse)}"
    case With(context, body) =>
      py"with ${commas(ctx, context)}:\n${lines(ctx.nest, body)}"
    case Raise(None, None) =>
      py"raise"
    case Raise(Some(exc), None) =>
      py"raise ${e(ctx, exc)}"
    case Raise(Some(exc), Some(cause)) =>
      py"raise ${e(ctx, exc)} from ${e(ctx, cause)}"
    case Try(body, handlers, orElse, orFinally) =>
      py"try:\n${lines(ctx.nest, body)}${lines(ctx, handlers)}${elseB(ctx, orElse)}${elseB(ctx, orFinally, "finally")}"
    case Except(None, children) =>
      py"except:\n${lines(ctx.nest, children, finish = "")}"
    case Except(Some(alias), children) =>
      py"except ${generate(ctx, alias)}:\n${lines(ctx.nest, children, finish = "")}"
    case Assert(test, None) =>
      py"assert ${e(ctx, test)}"
    case Assert(test, Some(msg)) =>
      py"assert ${e(ctx, test)}, ${e(ctx, msg)}"
    case Return(None) => py"return"
    case Return(Some(value)) => py"return ${e(ctx, value)}"
    case Delete(targets) => py"del ${exprs.commas(ctx, targets)}"
    case Pass => py"pass"
    case Break => py"break"
    case Continue => py"continue"
    case _ => partialResult(tree)
  }

  private def e(ctx: GeneratorContext, expr: Expression): Python = exprs.generate(ctx, expr)

  private def lines(ctx: GeneratorContext, statements: Seq[Statement], finish: String = "\n"): Python = {
    if (statements.isEmpty) {
      py""
    } else {
      val body = statements.map(generate(ctx, _))
      val separatedItems = body.tail.foldLeft[Python](body.head) {
        case (agg, item) => py"$agg\n$item"
      }
      py"$separatedItems$finish"
    }
  }

  // decorators need their leading whitespace trimmed and get followed by a trailing whitespace
  private def decorate(ctx: GeneratorContext, decorators: Seq[Decorator]): Python = {
    lines(ctx, decorators) match {
      case OkResult(output) => output match {
        case "" => OkResult("")
        case some => OkResult(s"${some.trim}\n${ctx.ws}")
      }
      case nok: Python => nok
    }
  }

  private def elseB(ctx: GeneratorContext, orElse: Seq[Statement], branch: String = "else"): Python = orElse match {
    case Nil => py""
    case some => py"${ctx.ws}$branch:\n${lines(ctx.nest, some)}"
  }

  private def parents(ctx: GeneratorContext, names: Seq[Expression]): Python = names match {
    case Nil => py""
    case some => py"(${exprs.commas(ctx, some)})"
  }
}
