# Implementing Snowflake AST -> Intermediate Representation

Here's a guideline for incrementally improving the Snowflake -> IR translation in `SnowflakeAstBuilder`.

## Step 1: add a test

Let say we want to add support for a new type of query, for the sake of simplicity we'll take `SELECT a FROM b` as an example (even though this type of query is already supported).

The first thing to do is to add an example in `SnowflakeAstBuilderSpec`:

```scala
"translate my query" in { // find a better test name
  example(
    query = "SELECT a FROM b",
    expectedAst = ???
  )
}
```

## Step 2: figure out the expected IR

Next we need to figure out the intermediate AST we want to produce for this specific type of query. In this simple example, the expected output would be `Project(NamedTable("b", Map.empty, is_streaming = false), Seq(Column("a")))` so we update our test with:

```scala
// ...
    expectedAst = Project(NamedTable("b", Map.empty, is_streaming = false), Seq(Column("a")))
// ...
```

Less trivial cases may require careful exploration of the available data types in `com.databricks.labs.remorph.parsers.intermediate` to find to proper output structure.

It may also happen that the desired structure is missing in `com.databricks.labs.remorph.parsers.intermediate`. In such a case, **we should not add/modify anything to/in the existing AST**, as it will eventually be generated from an external definition. Instead, we should add our new AST node as an extension in `src/main/scala/com/databricks/labs/remorph/parsers/intermediate/extensions.scala`.

## Step 3: run the test

Our new test is now ready to be run (we expect it to fail). But before running it, you may want to uncomment the `println(tree.toStringTree(parser))` line in the `parseString` method of `SnowflakeAstBuilderSpec`.

It will print out the parser's output for your query in a LISP-like format:

```
(snowflake_file (batch (sql_command (dml_command (query_statement (select_statement (select_clause SELECT (select_list_no_top (select_list (select_list_elem (column_elem (column_name (id_ a))))))) (select_optional_clauses (from_clause FROM (table_sources (table_source (table_source_item_joined (object_ref (object_name (id_ b))))))))))))) <EOF>)
```

This will be useful to know which methods in `SnowflakeAstBuilder` you need to override/modify.
Note however, that ANTLR4 generated parser tree visitors automatically call accept on nodes,
so you do not always need to override some intermediate method, just to call accept() yourself.


## Step 4: modify SnowflakeAstBuilder

Method names in `SnowflakeAstBuilder` follow the names that appear in the parser's output above. For example, one would realize that the content of the `column_name` node is what will ultimately get translated as an IR `Column`. To do so, they therefore need to override the `visitColumn_name` method of `SnowflakeAstBuilder`.

The AST builder has one `visit*` method for every possible node in the parser's output. Methods that are not overridden simply return the result of visiting children nodes. So in our example, even though we haven't overridden the `visitColumn_elem` method, our `visitColumn_name` method will get called as expected. 

A rule of thumb for picking the right method to override is therefore to look for the narrowest node (in the parser's output) that contains all the information we need. 

Here, the `(id_ a)` node is "too narrow" as `id_` appears in many different places where it could be translated as something else than a `Column` so we go for the parent `column_name` instead.

Moving forward, we may realize that there are more ways to build a `Column` than we initially expected so we may have to override the `visitColumn_elem` as well, but we will still be able to reuse our `visitColumn_name` method.

## Step 5: test, commit, improve

At this point, we should have come up with an implementation of `SnowflakeAstBuilder` that makes our new test pass. It is a good time for committing our changes. 

It isn't the end of the story though. We should add more tests with slight variations of our initial query (like `SELECT a AS aa FROM b` for example) and see how our new implementation behaves. This may in turn make us change our implementation a bit, repeating the above steps a few times more.

## Caveat

The grammar definition in `src/main/antlr4/com/databricks/labs/remorph/parsers/snowflake/SnowflakeParser.g4` is still a work-in-progress and, a such, it may contain rule that are either incorrect or simply "get in the way" of implementing the Snowflake->IR translation. 

When stumbling upon such case, one should:
- materialize the problem in a (failing) test in `SnowflakeAstBuilderSpec`, flagged as `ignored` until the problem is solved
- shallowly investigate the problem in the grammar and raise an Github issue with a problem statement
- add a `TODO` comment on top of the failing test with a link to said issue
- move on with implementing something else



