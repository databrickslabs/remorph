// MIT License
//
// Copyright (c) 2004-2024 Jim Idle
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.

// The TSQL SELECT statement
//
parser grammar USqlSelect;

///////////////////////////////////////////////////////////
// SELECT statements
selectStatement
		: 	qe=queryExpression
			ob=orderByClause?
			cc=computeClause*
			fc=forClause?
			(oc=optionClause)?
			SEMI?
		;

// Note that the following rules may also be used by other statements such as INSERT/UPDATE/DELETE
//
queryExpression
		:  querySpecification
			(
				(
			  	 	  UNION ALL?
					| EXCEPT
					| INTERSECT
		  		) (
		  			  querySpecification
		  		  )
		  	)*
		;

// TODO: Why did I comment this out without saying why?
//parenQuerySpecification
//   : LPAREN selectStatement RPAREN
//  ;

querySpecification
		: SELECT
			(ALL | DISTINCT)?
			(     topClause selectList?
                | selectList
            )
			ic=intoClause?
			fc=fromClause?
			wc=whereClause?
			gb=groupByClause?
			hc=havingClause?
        | parenSubQuery
		;

havingClause
		: HAVING searchCondition
		;

whereClause
		: WHERE searchCondition
		;

fromClause
		: FROM tableSourceList
		;

intoClause
		: INTO keywId
		;

topClause
		: TOP
            topExpression
            PERCENT? (WITH TIES)?
		;

topExpression
        : LPAREN expression RPAREN
        | (INTEGER| funcKeywId)
        ;

selectList
		: se+=selectElement (COMMA se+=selectElement)*
		;

selectElement
		: OPMUL									// Simply select all columns in the 'table'
		| funcKeywId OPEQ expression		    // Assignment of column alias to something
		| expression                     		// Your semantic phase should validate the expression and OPEQ etc
			(
				  ( ac=asClause) 			    // A function such as an aggregate or OVER functions
				| DOT OPMUL				        // All columns at a level such as table, view, table alias
				| c=COLON COLON f=funcKeywId	// Means we were actually parsing a udt CLR routine
				|
			)
		;

asClause
		: // Watch out for SELECT 'x'\n Label, as may be ambiguous in parse
            AS? (funcKeywId | SQ_LITERAL |DQ_LITERAL)
		;

optAs
		: AS
		|
		;

tableSourceList
		: tableSource (COMMA tableSource)*
		;

// ------------------
// This is the definitive definition of all things that
// are or can act as, a table source for T-SQL, which
// is quite a collection these days. Anyone think that SQL
// has rather got out of hand? ;-)
//
tableSource
		: t=tableSourceElement
		;

tableSourceElement
    :   tableSourcePrimitive

        (     // Cross joins
              //

                  (   CROSS (JOIN|APPLY)
                    | OUTER APPLY
                  )
                    tableSourceElement

              // INNER or OUTER JOINS
              //
            | joinTypePrefix JOIN tableSourceElement onJoin
        
              // PIVOT Tables
              //
            |      PIVOT pivotClause

              // UNPIVOTED tables
              //
            |    UNPIVOT unpivotClause
        )*
    ;

onJoin
    : ON searchCondition
    ;


joinTypePrefix
		: (     (LEFT | RIGHT | FULL) OUTER?

				| INNER
			)?
			joinHint?
		;

pivotClause
		:   LPAREN

                expression
                forColumn
                KIN cteColList

            RPAREN
                optAs funcKeywId	// Pivot table alias
		;

forColumn
        :   FOR columnName
        ;

unpivotClause
		:   LPAREN

                f1=funcKeywId
                forColumn
                KIN cteColList

            RPAREN

                oa=optAs f2=funcKeywId	// Pivot table alias
		;

joinHint
		: LOOP
		| HASH
		| MERGE
		| REMOTE
		;

tableSourcePrimitive
		: pt=primitiveTable
		;

primitiveTable
		: ki=keywId (COMMA keywId (COMMA keywId)?)?			// Table specifier or @variable, or possibly user function
			(
					LPAREN pl=paramList? RPAREN			// User defined table function or @variable.functionCall
				    asClause?
					(ca=columnAliases)?	// Column aliases within table

				| asClause?										// Table alias
				  tsc=tablesampleClause?					// Tables sampling limiters
				  (th=tableHints)?	// Optimizaton hints
			)

		| rf=rowsetFunction	// T-SQL built in rowset functions

		 		asClause?											// Table alias
				ca=columnAliases?		// Column aliases for BULK operations

		| LPAREN
			(

                  dt=derivableTable							// Sub query, creates a derived table

					(	  RPAREN
						  asClause?		// Table alias
						  columnAliases?	// Column aliases within table

						| asClause?		// Table alias
						  columnAliases?	// Column aliases within table
						  RPAREN
					)

				| ts=tableSource  RPAREN						// A parenthesized table source
			)
		;

derivableTable
    : insertUpdateTargetValues   // Table value constructor, as from 2008R2
    | mergeStatement               // 2008R2
    | selectStatement              // 2005/ANSI
    ;

tableHints
		: (
			  WITH? LPAREN thl=tableHintList RPAREN
			//| thl=tableHintList
		  )

		;

tableHintList
		: th+=tableHint (COMMA th+=tableHint)*


		;

tableHint
		: NOEXPAND?

        (
              NOLOCK
            | READUNCOMMITTED
            | UPDLOCK
            | REPEATABLEREAD
            | SERIALIZABLE
            | HOLDLOCK
            | READCOMMITTED
            | READCOMMITTEDLOCK
            | FASTFIRSTROW
            | TABLOCK
            | TABLOCKX
            | PAGLOCK
            | ROWLOCK
            | NOWAIT
            | READPAST
            | XLOCK
            | KEEPIDENTITY
            | KEEPDEFAULTS
            | IGNORE_CONSTRAINTS
            | IGNORE_TRIGGERS
            | KINDEX
                    (
                          LPAREN (INTEGER | funcKeywId) (COMMA (INTEGER | funcKeywId))* RPAREN
                        | OPEQ (INTEGER | funcKeywId)
                    )
         )
		;

tablesampleClause
		: TABLESAMPLE SYSTEM?
			LPAREN
				expression (PERCENT | ROWS)?
			RPAREN
				(REPEATABLE LPAREN expression RPAREN)?
		;

derivedTable
		: queryExpression
		;

columnAliases
		:
			LPAREN
				fki+=funcKeywId (COMMA fki+=funcKeywId)*
			RPAREN
		;

computeClause
		: COMPUTE
			computeFunctionList
			computeBy?
		;

computeBy
		: BY expression (COMMA expressionList)?
		;

computeFunctionList
		: computeFunction (COMMA computeFunction)*
		;

computeFunction
		:	computeFunctionName
			LPAREN
				expression
			RPAREN
		;

computeFunctionName
    : AVG
    | COUNT
    | KMAX
    | KMIN
    | STDEV
    | STDEVP
    | VAR
    | VARP
    | SUM
    ;

forClause
		: FOR
			(
				  BROWSE
				| forXmlClause
			)
		;

forXmlClause
		: XML
			(
			  (
				  RAW (LPAREN SQ_LITERAL RPAREN)?
				| AUTO
			  )
			  	forXmlCommonDirectives*
				(COMMA
					(
						  XMLDATA
						| XMLSCHEMA (LPAREN SQ_LITERAL RPAREN)?
					)
				)?
				(COMMA ELEMENTS ((XSINIL | ABSENT))?)?

			| EXPLICIT
				forXmlCommonDirectives*
				(COMMA XMLDATA)?

			| PATH
				(LPAREN SQ_LITERAL RPAREN)?
				forXmlCommonDirectives*
				(COMMA? ELEMENTS ((XSINIL | ABSENT))?)?
			)

		;

forXmlCommonDirectives
		: 	(COMMA BINARY BASE64)
		|	(COMMA TYPE)
		|	(COMMA ROOT ( LPAREN SQ_LITERAL RPAREN)?)
		;

optionClause
		: OPTION LPAREN queryHintList RPAREN
		;

queryHintList
		: qh+=queryHint (COMMA qh+=queryHint)*
		;

queryHint
		: qhs=queryHintSet
		;

queryHintSet
		: ( HASH | ORDER )  GROUP
		| ( CONCAT | HASH | MERGE ) UNION
  		| ( LOOP | MERGE | HASH ) JOIN
  		| FAST INTEGER
  		| FORCE ORDER
  		| MAXDOP INTEGER
  		| OPTIMIZE FOR
  				LPAREN
  					optimizeHintList
  				RPAREN
  		| PARAMETERIZATION ( SIMPLE | FORCED )
  		| RECOMPILE
  		| ROBUST PLAN
  		| KEEP PLAN
  		| KEEPFIXED PLAN
  		| EXPAND VIEWS
  		| MAXRECURSION INTEGER
  		| USE PLAN SQ_LITERAL
		;

optimizeHintList
		: oh+=optimizeHint (COMMA oh+=optimizeHint)*
		;

optimizeHint
		: ohs=optimizeHintSet
		;

optimizeHintSet
		: (funcKeywId OPEQ SQ_LITERAL)
		;

groupByClause
		:  GROUP BY
		    (
		         ALL? expressionList (WITH (CUBE | ROLLUP))?
			    | mdSets
			)
		;

mdSets
    : (ROLLUP | CUBE | GROUPING SETS)
        LPAREN
            (
                  expression
                | (LPAREN expressionList? RPAREN COMMA?)+
            )
        RPAREN
    ;

// End: SELECT statements
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// subquery definition
subQuery
		: selectStatement
		;

// All the keyword and element strings that gurantee that what comes next
// is a subquery. Essentially SELECT, UPDATE etc. This predicate stops
// the parenthesised expression or predicate from being mistaken as a
// subquery.
//
predForSubq
		: WITH		// WITH common table expression
		| SELECT 	// statement
		;


parenSubQuery
		: LPAREN subQuery RPAREN
		;

predicatedSubQuery
		: subQuery
		;

predicatedParenSubQuery
		:  LPAREN subQuery RPAREN
		;
// End: subquery definition
///////////////////////////////////////////////////////////
