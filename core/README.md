# Implementing Snowflake and Other SQL Dialects AST -> Intermediate Representation

Here's a guideline for incrementally improving the Snowflake -> IR translation in `SnowflakeAstBuilder`, et al., 
and the equivalent builders for additional dialects.

## Table of Contents
1. [Changing the ANTLR grammars](#changing-the-antlr-grammars)
2. [Conversion of AST to IR](#converting-to-ir-in-the-dialectthingbuilder-classes)
   1. [Step 1: add a test](#step-1-add-a-test)
   2. [Step 2: figure out the expected IR](#step-2-figure-out-the-expected-ir)
   3. [Step 3: run the test](#step-3-run-the-test)
   4. [Step 4: modify <Dialect><thing>Builder](#step-4-modify-dialectthingbuilder)
   5. [Step 5: test, commit, improve](#step-5-test-commit-improve)
   6. [Caveat](#caveat)

## Changing the ANTLR grammars

Changing the ANTLR grammars is a specialized task, and only a few team members have permission to do so.
Do not attempt to change the grammars unless you have been given explicit permission to do so. 

It is unfortunately, easy to add parser rules without realizing the full implications of the change, 
and this can lead to performance problems. Performance problems usually come from the fact that ANTLR will manage 
to make a working parser out of almost any input specification. However, the parser may be very slow, 
or may not be able to handle certain edge cases.

After a grammar change is made, the .g4 files must be reformatted to stay in line with the guidelines. We use (for now
at least) the [antlr-format](https://github.com/mike-lischke/antlr-format) tool to do this. The tool was written
in typescript, so it does not easily run as a maven task. For the moment, please run it manually on the .g4 files
in each of the dialects we support under `src/main/antlr4/../parsers`

### Installing antlr-format

The antlr-format tool will run as part of the maven build process and so there is no need to install it locally.
But you can do so using the instructions below.

In order to run the tool, you have to install Node.js. You can download it from [here](https://nodejs.org/en/download/),
or more simply install it with `brew install node` if you are on a Mac.

Once node is installed you can install the formatter with:

```bash
npm install -g antlr-format
npm install -g antlr-format-cli
```

### Running antlr-format

The formatter is trivial to run from the directory containing your changed grammar: 

```bash
~/databricks/remorph/core/src/main/antlr4/../parsers/tsql (feature/antlrformatdocs ✘)✹ ᐅ antlr-format *.g4

antlr-format, processing options...

formatting 2 file(s)...

done [82 ms]
```

### Caveat

Some of the grammar definitions (`src/main/antlr4/com/databricks/labs/remorph/parsers/<dialect>/<dialect>Parser.g4`)
may still be works-in-progress and, as such, may contain rules that are either incorrect or simply 
_get in the way_ of implementing the Snowflake->IR translation.

When stumbling upon such a case, one should:
- materialize the problem in a (failing) test in `<Dialect><something>BuilderSpec`, flagged as `ignored` until the problem is solved
- shallowly investigate the problem in the grammar and raise a Github issue with a problem statement
- add a `TODO` comment on top of the failing test with a link to said issue
- point out the issue to someone tasked with changing/fixing grammars
- move on with implementing something else

## Converting to IR in the <Dialect><thing>Builder classes

Here is methodolgy used to effect changes to IR generation.

### Step 1: add a test

Let say we want to add support for a new type of query, for the sake of simplicity we'll take 
`SELECT a FROM b` in SnowFlake, as an example (even though this type of query is already supported).

The first thing to do is to add an example in `SnowflakeAstBuilderSpec`:

```scala
"translate my query" in { // find a better test name
  example(
    query = "SELECT a FROM b",
    expectedAst = ir.Noop
  )
}
```

### Step 2: figure out the expected IR

Next we need to figure out the intermediate AST we want to produce for this specific type of query. 
In this simple example, the expected output would be 
`Project(NamedTable("b", Map.empty, is_streaming = false), Seq(Column("a")))` 
so we update our test with:

```scala
// ...
    expectedAst = Project(NamedTable("b", Map.empty, is_streaming = false), Seq(Column("a")))
// ...
```

Less trivial cases may require careful exploration of the available data types in 
`com.databricks.labs.remorph.parsers.intermediate` to find to proper output structure.

It may also happen that the desired structure is missing in `com.databricks.labs.remorph.parsers.intermediate`. 
In such a case, **we should not add/modify anything to/in the existing AST**, as it will eventually be generated 
from an external definition. Instead, we should add our new AST node as an extension in `src/main/scala/com/databricks/labs/remorph/parsers/intermediate/extensions.scala`.

### Step 3: run the test

Our new test is now ready to be run (we expect it to fail). But before running it, you may want to uncomment the 
`println(tree.toStringTree(parser))` line in the `parseString` method of `SnowflakeAstBuilderSpec`.

It will print out the parser's output for your query in a LISP-like format:

```
(snowflake_file (batch (sql_command (dml_command (query_statement (select_statement (select_clause SELECT (select_list_no_top (select_list (select_list_elem (column_elem (column_name (id_ a))))))) (select_optional_clauses (from_clause FROM (table_sources (table_source (table_source_item_joined (object_ref (object_name (id_ b))))))))))))) <EOF>)
```

This will be useful to know which methods in `SnowflakeAstBuilder` you need to override/modify.
Note however, that ANTLR4 generated parser tree visitors automatically call accept on nodes,
so you do not always need to override some intermediate method, just to call accept() yourself.

### Step 4: modify <Dialect><thing>Builder

Method names in `<Dialect><something>Builder` follow the names that appear in the parser's output above. For example, 
one would realize that the content of the `columnName` node is what will ultimately get translated as an IR `Column`. 
To do so, they therefore need to override the `visitColumnName` method of `SnowflakeExpressionBuilder`.

Rather than have a single big visitor for every possible node in the parser's output, the nodes are handled by
specialized visitors. For instance `TSqlExpressionBuilder` and `SnowflakeExpressionBuilder`. An instance of the `<dialect>ExpressionBuilder`
is injected into the `<dialect>AstBuilder`, which in turn calls accept using the expressionBuilder on a node that 
will be an expression within a larger production, such as visitSelect. 

The <something> builders have one `visit*` method for every node in the parser's output that the builder is responsible
for handling. Methods that are not overridden simply return the result of visiting children nodes. So in our example, 
even though we haven't overridden the `visitColumnElem` method, our `visitColumnName` method will get called as expected
because ANTLR creates a default implementation of `visitColumnElem` tha that calls `accept(this)` on the `columnName` node.

However, note that if a rule can produce multiple children using the default `visit`, you will need to override the 
method that corresponds to that rule and produce the single IR node that represents that production.

A rule of thumb for picking the right method to override is therefore to look for the narrowest node (in the parser's output) 
that contains all the information we need. Once you override a `visit` function, you are then responsible for either
calling `accept(<visitor>)` on its child nodes or otherwise processing them using a specialized `build<something>` method. 

Here, the `(id_ a)` node is "too narrow" as `id_` appears in many different places where it could be translated as 
something else than a `Column` so we go for the parent `columnName` instead.

Moving forward, we may realize that there are more ways to build a `Column` than we initially expected so we may 
have to override the `visitColumnElem` as well, but we will still be able to reuse our `visitColumnName` method, and
have `visitColumnElem` call `accept(expressionBuilder)` on the `columnName` node.

### Step 5: test, commit, improve

At this point, we should have come up with an implementation of `<Dialect><something>Builder` that makes our new test pass. 
It is a good time for committing our changes. 

It isn't the end of the story though. We should add more tests with slight variations of our initial query 
(like `SELECT a AS aa FROM b` for example) and see how our new implementation behaves. This may in turn make us 
change our implementation, repeating the above steps a few times more.
