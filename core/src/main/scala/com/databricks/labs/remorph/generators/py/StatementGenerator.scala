package com.databricks.labs.remorph.generators.py
import com.databricks.labs.remorph.generators.{CodeInterpolator, TBASeqOps}
import com.databricks.labs.remorph.intermediate.Expression

class StatementGenerator(private val exprs: ExpressionGenerator) extends BasePythonGenerator[Statement] {
  override def generate(tree: Statement): Python = {
    withGenCtx { ctx =>
      code"${ctx.ws}${statement(tree)}"
    }
  }

  private def statement(tree: Statement): Python = tree match {
    case Module(children) => lines(children)
    case Alias(name, None) => e(name)
    case ExprStatement(expr) => e(expr)
    case FunctionDef(name, args, children, decorators) =>
      withIndentedBlock(code"${decorate(decorators)}def ${name.name}(${exprs.arguments(args)}):", lines(children))
    case ClassDef(name, bases, children, decorators) =>
      withIndentedBlock(code"${decorate(decorators)}class ${name.name}${parents(bases)}:", lines(children))
    case Alias(name, Some(alias)) =>
      code"${e(name)} as ${e(alias)}"
    case Import(names) =>
      code"import ${commas(names)}"
    case ImportFrom(Some(module), names, _) =>
      code"from ${e(module)} import ${commas(names)}"
    case Assign(targets, value) =>
      code"${exprs.commas(targets)} = ${e(value)}"
    case Decorator(expr) =>
      code"@${e(expr)}"
    case For(target, iter, body, orElse) =>
      Seq(withIndentedBlock(code"for ${e(target)} in ${e(iter)}:", lines(body)), elseB(orElse)).mkCode
    case While(test, body, orElse) =>
      Seq(withIndentedBlock(code"while ${e(test)}:", lines(body)), elseB(orElse)).mkCode
    case If(test, body, orElse) =>
      Seq(withIndentedBlock(code"if ${e(test)}:", lines(body)), elseB(orElse)).mkCode
    case With(context, body) =>
      withIndentedBlock(code"with ${commas(context)}:", lines(body))
    case Raise(None, None) =>
      code"raise"
    case Raise(Some(exc), None) =>
      code"raise ${e(exc)}"
    case Raise(Some(exc), Some(cause)) =>
      code"raise ${e(exc)} from ${e(cause)}"
    case Try(body, handlers, orElse, orFinally) =>
      Seq(
        withIndentedBlock(code"try:", code"${lines(body)}"),
        lines(handlers),
        elseB(orElse),
        elseB(orFinally, "finally")).mkCode
    case Except(None, children) =>
      withIndentedBlock(code"except:", lines(children, finish = ""))
    case Except(Some(alias), children) =>
      withIndentedBlock(code"except ${generate(alias)}:", lines(children, finish = ""))
    case Assert(test, None) =>
      code"assert ${e(test)}"
    case Assert(test, Some(msg)) =>
      code"assert ${e(test)}, ${e(msg)}"
    case Return(None) => code"return"
    case Return(Some(value)) => code"return ${e(value)}"
    case Delete(targets) => code"del ${exprs.commas(targets)}"
    case Pass => code"pass"
    case Break => code"break"
    case Continue => code"continue"
    case _ => partialResult(tree)
  }

  private def e(expr: Expression): Python = exprs.generate(expr)

  private def lines(statements: Seq[Statement], finish: String = "\n"): Python = {
    val body = statements.map(generate)
    val separatedItems = body.reduceLeftOption[Python] { case (agg, item) => code"$agg\n$item" }
    separatedItems.map(items => code"$items$finish").getOrElse(code"")
  }

  // decorators need their leading whitespace trimmed and get followed by a trailing whitespace
  private def decorate(decorators: Seq[Decorator]): Python = {
    withGenCtx { ctx =>
      lines(decorators).map {
        case "" => ""
        case some => s"${some.trim}\n${ctx.ws}"
      }
    }
  }

  private def elseB(orElse: Seq[Statement], branch: String = "else"): Python = orElse match {
    case Nil => code""
    case some =>
      withGenCtx { ctx =>
        withIndentedBlock(code"${ctx.ws}$branch:", lines(some))
      }
  }

  private def parents(names: Seq[Expression]): Python = names match {
    case Nil => code""
    case some => code"(${exprs.commas(some)})"
  }
}
