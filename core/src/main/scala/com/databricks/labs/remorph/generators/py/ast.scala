package com.databricks.labs.remorph.generators.py

import com.databricks.labs.remorph.intermediate.{Binary, DataType, Expression, Name, Plan, StringType, UnresolvedType, Attribute => IRAttribute}

// this is a subset of https://docs.python.org/3/library/ast.html

abstract class Statement extends Plan[Statement] {
  override def output: Seq[IRAttribute] = Nil
}

abstract class LeafStatement extends Statement {
  override final def children: Seq[Statement] = Nil
}

case class Comment(child: Expression, text: String) extends Expression {
  override def children: Seq[Expression] = Seq(child)
  override def dataType: DataType = child.dataType
}

// see https://docs.python.org/3/library/ast.html#ast.Module
case class Module(children: Seq[Statement]) extends Statement

case class Arguments(
    args: Seq[Expression] = Seq.empty,
    vararg: Option[Name] = None,
    kwargs: Option[Name] = None,
    defaults: Seq[Expression] = Seq.empty) {
  def expression: Seq[Expression] = args ++ vararg ++ kwargs ++ defaults
}

// keyword arguments supplied to call
case class Keyword(arg: Name, value: Expression) extends Binary(arg, value) {
  override def dataType: DataType = UnresolvedType
}

case class Decorator(expr: Expression) extends LeafStatement

// see https://docs.python.org/3/library/ast.html#ast.FunctionDef
case class FunctionDef(name: Name, args: Arguments, children: Seq[Statement], decorators: Seq[Decorator] = Seq.empty)
    extends Statement

// see https://docs.python.org/3/library/ast.html#ast.ClassDef
case class ClassDef(
    name: Name,
    bases: Seq[Expression] = Seq.empty,
    children: Seq[Statement] = Seq.empty,
    decorators: Seq[Decorator] = Seq.empty)
    extends Statement

case class Return(value: Option[Expression] = None) extends LeafStatement
case class Delete(targets: Seq[Expression]) extends LeafStatement
case class Assign(targets: Seq[Expression], value: Expression) extends LeafStatement

// see https://docs.python.org/3/library/ast.html#ast.For
case class For(target: Expression, iter: Expression, body: Seq[Statement], orElse: Seq[Statement] = Seq.empty)
    extends Statement {
  override def children: Seq[Statement] = body ++ orElse
}

// see https://docs.python.org/3/library/ast.html#ast.While
case class While(test: Expression, body: Seq[Statement], orElse: Seq[Statement] = Seq.empty) extends Statement {
  override def children: Seq[Statement] = body ++ orElse
}

// see https://docs.python.org/3/library/ast.html#ast.If
case class If(test: Expression, body: Seq[Statement], orElse: Seq[Statement] = Seq.empty) extends Statement {
  override def children: Seq[Statement] = body ++ orElse
}

// see https://docs.python.org/3/library/ast.html#ast.With
case class With(context: Seq[Alias], body: Seq[Statement]) extends Statement {
  override def children: Seq[Statement] = context ++ body
}

// see https://docs.python.org/3/library/ast.html#ast.Raise
case class Raise(exc: Option[Expression] = None, cause: Option[Expression] = None) extends LeafStatement

// see https://docs.python.org/3/library/ast.html#ast.Try
case class Try(
    body: Seq[Statement],
    handlers: Seq[Except] = Seq.empty,
    orElse: Seq[Statement] = Seq.empty,
    orFinally: Seq[Statement] = Seq.empty)
    extends Statement {
  override def children: Seq[Statement] = body ++ handlers ++ orElse ++ orFinally
}

// see https://docs.python.org/3/library/ast.html#ast.ExceptHandler
case class Except(exception: Option[Alias] = None, children: Seq[Statement]) extends Statement

// see https://docs.python.org/3/library/ast.html#ast.Assert
case class Assert(test: Expression, msg: Option[Expression] = None) extends LeafStatement

case class Alias(name: Expression, alias: Option[Name] = None) extends LeafStatement

// see https://docs.python.org/3/library/ast.html#ast.Import
case class Import(names: Seq[Alias]) extends LeafStatement

// see https://docs.python.org/3/library/ast.html#ast.ImportFrom
case class ImportFrom(module: Option[Name], names: Seq[Alias] = Seq.empty, level: Option[Int] = None)
    extends LeafStatement

// see https://docs.python.org/3/library/ast.html#ast.Global
case class Global(names: Seq[Name]) extends LeafStatement

case object Pass extends LeafStatement
case object Break extends LeafStatement
case object Continue extends LeafStatement

case class ExprStatement(expr: Expression) extends LeafStatement

// see https://docs.python.org/3/library/ast.html#ast.Call
case class Call(func: Expression, args: Seq[Expression] = Seq.empty, keywords: Seq[Keyword] = Seq.empty)
    extends Expression {
  override def children: Seq[Expression] = Seq(func) ++ args ++ keywords
  override def dataType: DataType = UnresolvedType
}

// see https://docs.python.org/3/library/ast.html#ast.NamedExpr
case class NamedExpr(target: Expression, value: Expression) extends Binary(target, value) {
  override def dataType: DataType = UnresolvedType
}

// see https://docs.python.org/3/library/ast.html#ast.Lambda
case class Lambda(args: Arguments, body: Expression) extends Expression {
  override def children: Seq[Expression] = args.expression ++ Seq(body)
  override def dataType: DataType = UnresolvedType
}

// see https://docs.python.org/3/library/ast.html#ast.IfExp
case class IfExp(test: Expression, body: Expression, orElse: Expression) extends Expression {
  override def children: Seq[Expression] = Seq(test, body, orElse)
  override def dataType: DataType = UnresolvedType
}

// see https://docs.python.org/3/library/ast.html#ast.Dict
case class Dict(keys: Seq[Expression], values: Seq[Expression]) extends Expression {
  override def children: Seq[Expression] = keys ++ values
  override def dataType: DataType = UnresolvedType
}

// see https://docs.python.org/3/library/ast.html#ast.Set
case class Set(elts: Seq[Expression]) extends Expression {
  override def children: Seq[Expression] = elts
  override def dataType: DataType = UnresolvedType
}

// see https://docs.python.org/3/library/ast.html#ast.comprehension
case class Comprehension(target: Expression, iter: Expression, ifs: Seq[Expression]) extends Expression {
  override def children: Seq[Expression] = target +: iter +: ifs
  override def dataType: DataType = UnresolvedType
}

// see https://docs.python.org/3/library/ast.html#ast.ListComp
case class ListComp(elt: Expression, generators: Seq[Comprehension]) extends Expression {
  override def children: Seq[Expression] = elt +: generators
  override def dataType: DataType = UnresolvedType
}

// see https://docs.python.org/3/library/ast.html#ast.SetComp
case class SetComp(elt: Expression, generators: Seq[Comprehension]) extends Expression {
  override def children: Seq[Expression] = elt +: generators
  override def dataType: DataType = UnresolvedType
}

// see https://docs.python.org/3/library/ast.html#ast.DictComp
case class DictComp(key: Expression, value: Expression, generators: Seq[Comprehension]) extends Expression {
  override def children: Seq[Expression] = key +: value +: generators
  override def dataType: DataType = UnresolvedType
}

// see https://docs.python.org/3/library/ast.html#ast.GeneratorExp
case class GeneratorExp(elt: Expression, generators: Seq[Comprehension]) extends Expression {
  override def children: Seq[Expression] = elt +: generators
  override def dataType: DataType = UnresolvedType
}

// see https://docs.python.org/3/library/ast.html#ast.FormattedValue
case class FormattedValue(value: Expression, conversion: Int, formatSpec: Option[Expression] = None)
    extends Expression {
  override def children: Seq[Expression] = value +: formatSpec.toList
  override def dataType: DataType = UnresolvedType
}

// see https://docs.python.org/3/library/ast.html#ast.JoinedStr
case class JoinedStr(children: Seq[Expression]) extends Expression {
  override def dataType: DataType = StringType
}

// see https://docs.python.org/3/library/ast.html#ast.Attribute
case class Attribute(value: Expression, attr: Expression, ctx: ExprContext = Load) extends Expression {
  def this(value: Expression, name: String) = this(value, Name(name), Load)
  override def children: Seq[Expression] = Seq(value, attr)
  override def dataType: DataType = UnresolvedType
}

// see https://docs.python.org/3/library/ast.html#subscripting
case class Subscript(value: Expression, slice: Expression, ctx: ExprContext = Load) extends Expression {
  override def children: Seq[Expression] = Seq(value, slice)
  override def dataType: DataType = UnresolvedType
}

// see https://docs.python.org/3/library/ast.html#subscripting
case class Slice(lower: Option[Expression] = None, upper: Option[Expression] = None, step: Option[Expression] = None)
    extends Expression {
  override def children: Seq[Expression] = Nil ++ lower ++ upper ++ step
  override def dataType: DataType = UnresolvedType
}

// see https://docs.python.org/3/library/ast.html#ast.Starred
case class Starred(value: Expression, ctx: ExprContext = Store) extends Expression {
  override def children: Seq[Expression] = Seq(value)
  override def dataType: DataType = UnresolvedType
}

// see https://docs.python.org/3/library/ast.html#ast.List
case class List(children: Seq[Expression], ctx: ExprContext = Load) extends Expression {
  override def dataType: DataType = UnresolvedType
}

// see https://docs.python.org/3/library/ast.html#ast.Tuple
case class Tuple(children: Seq[Expression], ctx: ExprContext = Load) extends Expression {
  override def dataType: DataType = UnresolvedType
}

sealed trait ExprContext
case object Load extends ExprContext
case object Store extends ExprContext
case object Delete extends ExprContext
