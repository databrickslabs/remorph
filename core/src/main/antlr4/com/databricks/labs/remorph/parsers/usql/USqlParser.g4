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

parser grammar USqlParser;

options
{
	// Import the lexers token numbering scheme.
	//
	tokenVocab	= USqlLexer;
}

 
// Import the grammar for the million SQL statements
//
import USqlCommon, USqlExpression, USqlSelect, USqlAlter, USqlCreate, USqlPermissions, USQlCursors, USqlMisc, USqlMisc2, USqlDrop;

aaaTranslationUnit
        : b=batchStatements EOF
        ;

batchStatements
	    :	 firstExec*
            (     statements
                | (SEMI)
            )*
	    ;

firstExec
    :  execSp (SEMI)*
    ;
///////////////////////////////////////////////////
// Statements
//

statementBlock
        : s+=statements+
        |
        ;

statements
		: ddlStatements
		| sqlStatements
        | executeStatement ( fe+=firstExec)*
        | GO (SEMI)*
                    (firstExec)*
		;
		
ddlStatements
		: addStatement
		| alterStatement
        | createStatement
		| backupStatement
		| bulkStatement
        | cursorDdl
        | permissionsDdl
        | dropStatement
		;
		
sqlStatements
		: selectStatement
		| useStatement
		| withCommonTable
        | miscellaneousStatements
        | cursorStatements
		;

///////////////////////////////////////////////////////////
// useStatement statements
//
useStatement 
	: USE keywId SEMI?
	;
// End: useStatement
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// WITH common table expression
//
withCommonTable
		: WITH commonTableExpressionList
			(
				  selectStatement
                | deleteStatement
                | insertStatement
                | updateStatement
                | mergeStatement
			)
			SEMI?
		;
		
commonTableExpressionList
		: ce+=commonTableExpression (COMMA ce+=commonTableExpression)*
		;

commonTableExpression
		: tn=funcKeywId ccl=cteColList?
			AS 	LPAREN
					cqd=cteQueryDefinition
				RPAREN
		;
				
cteColList
		: LPAREN
			cn+=columnName (COMMA cn+=columnName)*
		  RPAREN
		;

cteQueryDefinition
		: selectStatement
		;
// End: WITH common table expression
///////////////////////////////////////////////////////////


///////////////////////////////////////////////////////////
// ADD statements...
//
addStatement
		: KADD COUNTER? SIGNATURE TO module BY cryptoList SEMI?
		;

module	: moduleClass? moduleName
		;
		
moduleClass
		: (keywId COLON COLON)
		;
		
moduleName
		: keywId
		;
		
cryptoList
		: cryptoOptions (COMMA cryptoOptions)*
		;
		
cryptoOptions
		: CERTIFICATE keywId		passSigOpts?
		| ASYMMETRIC KEY keywId 	passSigOpts?
		;
		
passSigOpts
		:  WITH  (
		  			  PASSWORD OPEQ SQ_LITERAL
		  			| SIGNATURE OPEQ keywId
		  		)
		;
// End: ADD statement
///////////////////////////////////////////////////////////

	
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////
// Common syntactical elements, shared between two or more rules.
//
notForReplication
	: KNOT FOR REPLICATION
	;

keywIdParenList
	: LPAREN keywIdList RPAREN
	;
	
keywIdList
	: k+=keywId (COMMA k+=keywId)*
	;
	
///////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////
	
///////////////////////////////////////////////////////////
// Definition of a search condition
//
searchCondition
    : LPAREN searchCondition RPAREN            #scPrec
    | KNOT searchCondition                     #scNot
    | searchCondition KAND searchCondition    #scAnd
    | searchCondition KOR searchCondition     #scOr
    | predicate                                 #scPredicate
    ;

predicate
	: expression
		(
			  (KNOT)?
				(
					  LIKE expression (ESCAPE SQ_LITERAL)?
					| BETWEEN expression KAND expression
					| KIN
						LPAREN
						(
		  					  psq=predicatedSubQuery
							| el=expressionList
						)
  						RPAREN
				)
			| IS KNOT? KNULL
            |
		)
	| CONTAINS
		LPAREN
            (
                  columnListNp (COMMA SQ_LITERAL)?
                | OPMUL COMMA (SQ_LITERAL|keywId)
            )
		RPAREN
	| FREETEXT
		LPAREN
			(
                  columnListNp (COMMA SQ_LITERAL)?
                | OPMUL COMMA (SQ_LITERAL|keywId)
            )
		RPAREN
	| EXISTS parenSubQuery
	;

someAllAny
	: (SOME | ALL | ANY)
	;
	    
columnListNp
	: columnName (COMMA columnName)*
	;

columnList
	: LPAREN columnListNp RPAREN
	| OPMUL
	;
// End: Search Condition
///////////////////////////////////////////////////////////

// Expression parser, with implicit precedence.
//
expressionList
		: expression (COMMA expression)*
		;

// --------------------------
// Generic function handler. Because some of the functions are without
// parameters and the () are optional for these, we basically just track everything here and then
// rewrite to the tree based on what we can make sense of here syntactically. The
// tree parsing phase should verify the semantic of everything else based on declarations
// and so on. Most functions are not declared as keywords here as they are just the same pattern
// of keyword followed by a parenthesised list. Some functions, such as rowset or ranking
// functions have specific syntax that does make sense to actually parse rather than conduct
// only semantic analysis.
//
functionsAndVars
	: aggregateWindowedFunctions
    | rankingFunctions
    | function
	;

function
    : CONVERT LPAREN dt=dataType COMMA e=expression (COMMA i2=expression)? RPAREN
    | CAST LPAREN e=expression AS dt=dataType RPAREN
    | funcName
        (
            functionArgs
        )
    ;

funcName
    : keywIdForFunc

    // Some functions, if listed in the keyword as var list, will cause massive ambiguity
    // so
    | UPDATE
    | RIGHT
    | LEFT
    | IDENTITY
    ;

functionArgs
	: LPAREN paramListOrAll? RPAREN
	;
	
paramListOrAll
	: paramList
	| OPMUL
	;
	
paramList
	: p+=paramListEl (COMMA p+=paramListEl)*
	;

paramListEl
    : expression // 2008 R2 table constructor looks like precedence
    | LPAREN RPAREN
    | DEFAULT
    ;
	
rowsetFunction
	: CONTAINSTABLE 	fcTableClause			// Precise and fuzzy matching
	| FREETEXTTABLE	fcTableClause			// Freetext column searching
	| OPENDATASOURCE							// Connect to OLEDB data sink
		LPAREN
			SQ_LITERAL							// PROGID of the OLE DB provider
            COMMA
			SQ_LITERAL							// Connection/Initialization string
		RPAREN
		
			DOT keywId							// Navigation to a specific table in the OLEDB connection
			
	| OPENQUERY
		LPAREN
			keywIdPart						// Handle variable for the linked OLE DB provider
            COMMA
			SQ_LITERAL							// Connection/Initialization string
		RPAREN
			
	| OPENROWSET
		LPAREN
		  (
			  oledbProvider
			  
			| bulkRows
		  )
		RPAREN
	
	| OPENXML 			openxmlClause			// XML table source
	;

bulkRows
	: BULK										// BULK import option from data files
				SQ_LITERAL									// Path to the import data file
                COMMA
				(
					  FORMATFILE OPEQ SQ_LITERAL 				// Path to definition file describing the import data
									bulkOptions?				// Possible option list
					| SINGLE_BLOB
					| SINGLE_CLOB
					| SINGLE_NCLOB
				)
	;
	
oledbProvider
	: sl=SQ_LITERAL								// OLE DB provider name
			  (
				COMMA 
					cs=connectionString
				COMMA
					(keywId | SQ_LITERAL)
			  )?					// IF omitted then the string is assumed to be a passthru query
			  

	;
	
connectionString
	: s1=SQ_LITERAL								// Connection/Initialization string
		(SEMI s2=SQ_LITERAL SEMI s3=SQ_LITERAL)?		// Connection string is optionally 3 params ds, user, passwd
	;
	
bulkOptions
	: (COMMA boe+=bulkOptionsEnts)+
	;
	
bulkOptionsEnts
	: CODEPAGE 			OPEQ SQ_LITERAL
	| ERRORFILE 		OPEQ SQ_LITERAL
	| FIRSTROW			OPEQ INTEGER
	| LASTROW 			OPEQ INTEGER
	| MAXERRORS 		OPEQ INTEGER
	| ROWS_PER_BATCH	OPEQ INTEGER
	;
		
fcTableClause
	: LPAREN
	  	keywId				// Table name
	  	COMMA
	  		(
	  			  funcKeywId		// Column name in the contains table
	  			| columnList		// List of columns in the contains table
	  		)
	  	COMMA SQ_LITERAL			// The contains condition, which is a thing unto itself
	  	(COMMA LANGUAGE
	  			(
	  				  INTEGER		// Language identifier (LCID)
	  				| SQ_LITERAL	// Alias in syslanguages table
	  				| HEXNUM		// HEx representation of the LCID
	  			)
	  	)?
	  	(COMMA expression)?			// Ranking limiter - probably literal or @var only, but it isn't the job of the
	  								// parser to work that out yet.	
	  RPAREN
	;
	
openxmlClause
	: LPAREN
		
		funcKeywId			// Document handle

		COMMA expression		// XPATH Pattern into the doc. Expression is allowed here but it must
								// of course yield a string, or semantics will throw it out.
			
		(COMMA INTEGER)?		// Mapping flags

      RPAREN
		(


                WITH LPAREN
				(
					  schemaDeclaration
					| keywId
				)
				RPAREN
		)?
										
	  
	;

schemaDeclaration
	: scd+=schemaColDef (COMMA scd+=schemaColDef)*
	;

schemaColDef
	: scd=schemaColDefSet
	;

schemaColDefSet
	: funcKeywId ctDataType
			  SQ_LITERAL?			// XPath column pattern or XML meta property mp:xxxx
	;
	
rankingFunctions
	: 	(
			  ROW_NUMBER	(LPAREN RPAREN)?
			| RANK			(LPAREN RPAREN)?
			| DENSE_RANK	(LPAREN RPAREN)?
			| NTILE			LPAREN INTEGER RPAREN
	  	)
	  		rankingOver
	;

rankingOver
	: OVER
		LPAREN
			partitionByClause?
			orderByClause
		RPAREN
	;
	
aggregateWindowedFunctions
	:	(
			  (AVG | CHECKSUM_AGG | KMAX | KMIN | SUM | STDEV | STDEVP | VAR | VARP)
			  			LPAREN  (ALL | DISTINCT)? expression RPAREN					// No sub queries and no agg funcs allowed, semantics will check this
			| (COUNT	| COUNT_BIG)
						LPAREN ((ALL | DISTINCT)? expression | OPMUL) RPAREN			// No sub queries and no agg funcs allowed, semantics will check this
			| GROUPING
                (
					  LPAREN  columnName RPAREN									// OVER clause was removed from SQL Server 2003 online books example
                    | SETS functionArgs
                )

		)
		groupingOver?
	;
	
groupingOver
	: OVER					// This is an optional clause for some functions, semantics should catch use or not
		LPAREN
			partitionByClause?
		RPAREN
	;
	
partitionByClause
	: PARTITION BY partitionByExpressionList
	;
	
partitionByExpressionList
	: partitionByExpression (COMMA partitionByExpression)*
	;
	
partitionByExpression
	: expression
	;
		
orderByClause
	: ORDER BY ob=orderByExpressionList
	;

orderByExpressionList
	: ob+=orderByExpression (COMMA ob+=orderByExpression)*
	;
	
orderByExpression
	: expression orderByCollate? (ASC | DESC)?
	;

orderByCollate
	: COLLATE funcKeywId
	;
	
// Columns are {x.y.}z reference, the alias name, or the INTEGER
// position of the column in the SELECT list
//
columnName
	: keywId
	| INTEGER
	;

uniqueidentifier
	: SQ_LITERAL
	| HEXNUM
	;	

////////////////////////////////////////////////////////////////////////////////////////////
// Identifier handling...
//
// T-SQL allow lots of keywords (but not all) to be an identifier and relies on context
// to interpret the keyword as if it were an identifier, so we allow
// a standard ID token, and just about any of the keywords to be used as identifiers
// Note that the SQL Server 2005/2008 T-SQl Online reference says that keywords are reserved
// and must be enclosed in [ ] if it is a keyword. However, do not believe that claim.
//
keywIdForFunc
    : keywIdOrcc ((DOT)+ keywIdPart)*
    ;

keywIdOrcc
    : keywIdPart
    ;

keywId
	: keywIdPart ((DOT)+ keywIdPart)*
    | ((DOT)+ keywIdPart)+
	;

keywIdPart
	: funcKeywId | DQ_LITERAL 
	;
	
funcKeywId
	: ID
    | BR_LITERAL
	| keywords
	;

// Literals that can be bracketed or single quoted
//
sqBrLiteral
    : SQ_LITERAL
    | BR_LITERAL
    ;

// Literals that can be bracketed, double quoted or single quoted
//
dqSqBrLiteral
    : SQ_LITERAL
    | BR_LITERAL
    | DQ_LITERAL
    ;

// Literal that can be keyword enclosed or double quoted
//
dqBrLiteral
    : DQ_LITERAL
    | BR_LITERAL
    ;

// Keywords allowed as IDs. This is an optional thing in TSQL, though why you woula allow it
// is beyond me. It is a bit of a pain to parse, but it is allowed.
//
keywords	
	:ABSENT							
	|ACTIVE							
	|ACTIVATION
	|ACCENT_SENSITIVITY
	|KADD
	|ADDRESS				
	|AFTER
	|ALGORITHM						
	|ALL
	|ALLOW_ROW_LOCKS
	|ALLOW_PAGE_LOCKS
	|ALLOW_SNAPSHOT_ISOLATION		
	|ALL_RESULTS						
	|ALTER
	|ANONYMOUS
	|ANSI_NULL_DEFAULT 				
	|ANSI_NULLS						
	|ANSI_PADDING					
	|ANSI_WARNINGS					
	|ANY
	|APPLICATION						
	|APPLY							
	|ARITHABORT
    |AT
	|AS
	|ASC
	|ASSEMBLY						
	|ASYMMETRIC						
	|AUTHENTICATION					
	|AUTHORIZATION
	|AUTH_REALM						
	|AUTO							
	|AUTO_CLOSE 						
	|AUTO_CREATE_STATISTICS 			
	|AUTO_UPDATE_STATISTICS_ASYNC	
	|AUTO_UPDATE_STATISTICS			
	|AVG								
	|BASE64							
	|BASIC							
	|BATCHES	
	|BATCHSIZE
    |BEGIN
	|BEGIN_DIALOG					
	|BETWEEN
	|BINARY							
	|BINDING							
	|BLOCKSIZE
	|BREAK
	|BROKER_INSTANCE
	|BROWSE
	|BULK
	|BUFFERCOUNT						
	|BULK_LOGGED						
	|BY
	|CASCADE						
	|CATALOG							
	|CATCH
	|CERTIFICATE						
	|CHANGE_TRACKING
	|CHARACTER_SET		
	|CHECK
	|CHECK_EXPIRATION	
	|CHECK_CONSTRAINTS
	|CHECK_POLICY
	|CHECKSUM_AGG					
	|CHECKSUM
    |CLEANUP
	|CLEAR							
	|CLEAR_PORT	
	|CLUSTERED
	|CODEPAGE						
	|COLLATE
	|COLLECTION
	|COLUMNS
	|COMPRESSION						
	|COMPUTE
	|CONCAT							
	|CONCAT_NULL_YIELDS_NULL
	|CONTAINS
	|CONTAINSTABLE
	|CONTINUE
	|CONTINUE_AFTER_ERROR	
	|CONTENT				
	|CONTRACT
    |CONTROL
	|CONVERSATION
	|CONSTRAINT
    |COOKIE
	|COPY					
	|COUNT_BIG						
	|COUNT							
	|COUNTER							
	|CREDENTIAL						
	|CROSS
	|CUBE
	|CURSOR
	|CURSOR_CLOSE_ON_COMMIT			
	|CURSOR_DEFAULT
    |CURRENT
    |DATABASE
	|DATABASE_MIRRORING
    |DATABASE_SNAPSHOT
	|DATA		
	|DATAFILETYPE					
	|DATE_CORRELATION_OPTIMIZATION	
	|DB_CHAINING						
	|DECRYPTION						
//	|DEFAULT
	|DEFAULT_DATABASE
	|DEFAULT_LANGUAGE	
	|DEFAULT_LOGON_DOMAIN			
	|DEFAULT_SCHEMA
    |DEFINITION
	|KDELETE
	|DENSE_RANK
	|DESCRIPTION
	|DESC
	|DIALOG					
	|DIFFERENTIAL
	|DIGEST							
	|DISABLE_BROKER
	|DISABLE
	|DISABLED	
	|DISTRIBUTED					
	|DISK
	|DISTINCT
	|DOCUMENT					
	|DROP
	|ELEMENTS						
	|EMERGENCY						
	|ENABLE
	|ENABLE_BROKER			    	
	|ENABLED							
	|ENCRYPTION				
	|END
	|ENDPOINT		
	|EMPTY
    |ERROR
	|ERROR_BROKER_CONVERSATIONS		
	|ERRORFILE						
	|ESCAPE
	|EXCEPT
    |EVENT
    |EVENTDATA
	|EXPAND
	|EXPIREDATE
	|EXPLICIT				
	|EXTERNAL		
	|EXTERNAL_ACCESS					
	|FAILOVER			    		
	|FAST							
	|FASTFIRSTROW					
//	|KFILE
	|FIELDTERMINATOR			
	|FILLFACTOR
	|FILEGROUP						
	|FILEGROWTH						
	|FILENAME		
	|FIRE_TRIGGERS	    		
	|FIRSTROW
	|FOREIGN						
	|FORCED			    			
	|FORCE							
	|FORCE_SERVICE_ALLOW_DATA_LOSS	
//	|FOR								
	|FORMATFILE						
	|FORMAT
//  |FREE
//	|FREETEXT						
//	|FREETEXTTABLE					
//	|FROM							
//	|FULL			    			
	|FULLTEXT						
//	|FUNCTION						
	|GB								
	|GLOBAL			    			
//	|GO								
//	|GROUP							
	|GROUPING			
	|HASHED			
//	|HASH
//	|HAVING							
	|HEADER_LIMIT					
//	|HOLDLOCK
    |HIGH
	|HTTP							
//	|IDENTITY
	|IGNORE_CONSTRAINTS				
	|IGNORE_DUP_KEY
	|IDENTITY_INSERT
	|IGNORE_TRIGGERS					
	|IMMEDIATE
    |IMPERSONATE
//	|INNER
	|INCREMENT	
	|INIT
//	|INSERT
	|INSTEAD						
	|INTEGRATED						
//	|INTERSECT						
//	|INTO
    |IO
    |JOB
//	|IS								
//	|JOIN							
//	|KAND							
	|KB								
	|KEEPDEFAULTS					
	|KEEPFIXED						
	|KEEPIDENTITY					
	|KEEP							
	|KEEPNULLS
	|KERBEROS	
	|KEYS					
//	|KEY		
	|KILOBYTES_PER_BATCH
//	|KINDEX							
//	|KIN								
//	|KNOT							
//	|KNULL							
//	|KOR								
	|LANGUAGE						
	|LASTROW
//    |LEFT
    |LEVEL
	|LIFETIME
//	|LIKE							
	|LISTENER_IP					
	|LOB_COMPACTION	
	|LOCAL			    			
	|LOGON
	|LOGIN							
	|LOGIN_TYPE						
	|LOG
    |LOW
	//|LOOP
	|MACHINE
	|MANUAL				
	|KMARK
	|MASTER							
	|MAXDOP							
	|MAXERRORS						
	|KMAX
	|MAXRECURSION		
	|MAXTRANSFERSIZE
	|MAX_QUEUE_READERS			
	|MAXSIZE							
	|MB								
	|MEDIADESCRIPTION
	|MEDIAPASSWORD
	|MEDIANAME
//	|MERGE
	|MESSAGE_FORWARDING				
	|MESSAGE_FORWARD_SIZE			
	|MESSAGE							
	|KMIN
	|MIRROR
	|MIRROR_ADDRESS							
	|MIXED							
	|MODIFY		
//	|MOVE
	|MULTI_USE						
	|MULTI_USER						
	|MUST_CHANGE
	|NAME							
	|NAMESPACE						
	|NEGOTIATE	
	|NEW_ACCOUNT					
	|NEW_BROKER	
	|NEW_PASSWORD					
	|NEWNAME			
//	|NEXT
	|NO	
	|NO_LOG
	|NOACTION
	|NO_CHECKSUM
//	|NOCHECK		
	|NOINIT
	|NOUNLOAD
	|NODE							
	|NOEXPAND						
	|NOFORMAT
	|NOLOCK							
	|NONE							
//	|NONCLUSTERED
	|NOREWIND
	|NOSKIP
	|NO_TRUNCATE
	|NO_WAIT
	|NORECOVERY							
	|NOWAIT							
//	|NTILE
	|NTLM
	|NRA
	|OBJECT
	|OF						
	|OFFLINE			    			
//	|OFF			
	|OLD_ACCOUNT
	|OLD_PASSWORD					
	|ONLINE
	|ONLY			    			
//	|ON								
//	|OPENDATASOURCE					
//	|OPENQUERY						
//	|OPENROWSET						
//	|OPENXML							
	|OPTIMIZE						
//	|OPTION							
//	|ORDER		
	|KOUT
//	|OUTPUT
//	|OUTER							
//	|OVER
    |OVERRIDE
	|OWNER
    |OWNERSHIP
	|PAD_INDEX					
	|PAGE_VERIFY						
	|PAGLOCK							
	|PARAMETERIZATION				
	|PARTITION						
	|PARTNER			    			
	|PASSWORD						
	|PATH
	|PAUSE							
//	|PERCENT							
	|PERMISSION_SET					
	|PERSISTED
//	|PIVOT							
//	|PLAN					
	|POPULATION		
	|PORTS							
	|PRIVATE		
	|PRIMARY		
	|PROCEDURE_NAME			
//	|PROCEDURE
    |PROFILE
    |KQUERY
	|QUEUE							
	|QUOTED_IDENTIFIER
	|RANGE		
	|RANK
	|RAW								
//	|RC4
	|READCOMMITTEDLOCK				
	|READCOMMITTED					
	|READ_COMMITTED_SNAPSHOT			
	|READ_ONLY						
	|READPAST						
	|READUNCOMMITTED					
	|READ_WRITE						
	|READ_WRITE_FILEGROUPS
	|REBUILD
	|RECOMPILE						
	|RECOVERY
    |RECONFIGURE
	|RECURSIVE_TRIGGERS			
//	|REFERENCES
	|REGENERATE	
	|RELATED_CONVERSATION
	|RELATED_CONVERSATION_GROUP
//	|REMOTE
	|REMOVE				
	|REORGANIZE			
	|REPEATABLEREAD					
	|REPEATABLE						
	|REPLICATION
	|REQUIRED			
	|RESTART			
	|RESTRICTED_USE			    	
	|RESTRICTED_USER					
	|RESUME		
	|RETAINDAYS
	|RETENTION
//	|RETURN
	|RETURNS
	|KREWIND	    			
//	|RIGHT							
	|ROBUST							
	|ROLE							
//	|ROLLBACK						
	|ROLLUP							
	|ROOT							
	|ROUTE		
//	|ROWGUIDCOL
    |ROWCOUNT
	|ROWLOCK		
	|ROWTERMINATOR					
    |ROW_NUMBER
	|ROWSETS_ONLY					
	|ROWS_PER_BATCH					
	|ROWS							
	|SAFE							
	|SAFETY		
	|SCHEME	    			
//	|SCHEMA		
	|SCHEMABINDING					
	|SECONDS							
	|SECRET							
//	|SELECT		
	|SELF					
	|SERIALIZABLE
	|SERVER
	|SERVICE_BROKER					
	|SERVICE			
	|SERVICE_NAME				
	|SESSIONS						
	|SESSION_TIMEOUT					
//	|SET
	|SIGNATURE						
	|SIMPLE			    			
	|SINGLE_BLOB						
	|SINGLE_CLOB						
	|SINGLE_NCLOB					
	|SINGLE_USER						
	|SINGLE_USE						
	|SITE							
	|SIZE	
	|KSKIP
    |SHOWPLAN
	|SOAP			
	|SORT_IN_TEMPDB
    |SOURCE
	|SPLIT
//	|SOME							
	|SQL								
	|SSL_PORT						
	|SSL								
	|STANDARD
	|STANDBY						
	|START
    |START_DATE
	|STARTED							
	|STATE	
	|STATS
	|KSTATUS
    |STATUSONLY
	|STATISTICS_NORECOMPUTE				
	|STDEVP							
	|STDEV	
	|STOP
	|STOP_ON_ERROR						
	|STOPPED
    |SUBJECT
    |SUBSCRIPTION
	|SUM								
	|SUPPORTED						
	|SUSPEND			    
	|SWITCH			
	|SYMMETRIC
	|SYS
	|SYSTEM							
//	|TABLESAMPLE						
//	|TABLE							
	|TABLOCK							
	|TABLOCKX						
	|TAPE
    |TARGET
    |TAKE
	|TB								
	|TCP								
	|TIES
	|TIMER						
	|TIMEOUT			    			
//	|TOP								
	|TORN_PAGE_DETECTION				
///	|TO		
	|TRANSACTION			
	|TRANSFER			
//	|TRIGGER	
	|TRUNCATE_ONLY						
	|TRUSTWORTHY						
	|TRY
    |TSQL
	|TYPE							
	|UNCHECKED	
//	|UNIQUE
//	|UNION							
	|UNLIMITED
	|UNLOAD	
	|UNLOCK									
//	|UNPIVOT							
	|UNSAFE							
	|UPDLOCK			
	|USED				
	|USER							
//	|USE			
	|VALID_XML
	|VALIDATION
	|VALUE
	|VALUES					
	|VARP							
	|VAR				
	|VARYING				
	|VIEWS							
	|VIEW		
	|VIEW_METADATA					
	|VISIBILITY						
	|WEBMETHOD						
	|WELL_FORMED_XML
//	|WHERE							
	|WINDOWS							
//	|WITH							
	|WITNESS			    			
	|WSDL							
	|XLOCK							
	|XMLDATA							
	|XMLSCHEMA						
	|XML								
	|XSINIL
    | FILELISTONLY
    | HEADERONLY
    | LABELONLY
    | REWINDONLY
    | VERIFYONLY
    | CHECKALLOC
    | CHECKCATALOG
    | CHECK_CONSTRAINTS
    | CHECKDB
    | CHECKFILEGROUP
    | CHECKIDENT
    | CHECKTABLE
    | CLEANTABLE
    | CONCURRENCYVIOLATION
    | DBREINDEX
    | DBREPAIR
    | DROPCLEANBUFFERS
    | FREEPROCCACHE
    | FREESESSIONCACHE
    | FREESYSTEMCACHE
    | HELP
    | INDEXDEFRAG
    | INPUTBUFFER
    | OPENTRAN
    | OUTPUTBUFFER
    | PINTABLE
    | PROCCACHE
    | SHOW_STATISTICS
    | SHOWCONTIG
    | SHRINKDATABASE
    | SHRINKFILE
    | SID
    | SPARSE
    | SQLPERF
    | TRACEOFF
    | TRACEON
    | TRACESTATUS
    | UNPINTABLE
    | UPDATEUSAGE
    | USEROPTIONS
    | FIRST
    | LAST
    | RELATIVE
    | ABSOLUTE
    | NEXT
    | PRIOR
	;
