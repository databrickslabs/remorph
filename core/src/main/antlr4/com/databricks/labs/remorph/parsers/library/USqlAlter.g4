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

parser grammar USqlAlter;

///////////////////////////////////////////////////////////
// ALTER statements
alterStatement
		: ALTER
			(
				  alterApplication
				| alterAssembly
				| alterAsymmetric
				| alterAuthorization
				| alterCertificate
				| alterCredential
				| alterDatabase
				| alterEndpoint
				| alterFulltext
				| alterFunction
				| alterIndex
				| alterLogin
				| alterMaster
				| alterMessage
				| alterPartition
				| alterProcedure
				| alterQueue
				| alterRemote
				| alterRole
				| alterRoute
				| alterSchema
				| alterService
				| alterSymmetric
				| alterTable
				| alterTrigger
				| alterUser
				| alterView
				| alterXml
			)
		;
// End: ALTER statements
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// alterApplication statements
//
alterApplication
    : createApplication
	;
	
// End: alterApplication
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// alterAssembly statements
//
alterAssembly
    : ASSEMBLY assemblyName
    	assemblyFrom?
    	assemblyWith?
    	assemblyDrop?
    	assemblyAdd?
    	SEMI?
    ;
    	
assemblyDrop
	: DROP KFILE assFileList
	;
	
assFileList
	: ALL
	| a+=assFile (COMMA af+=assFile)
	;
	
assFile
	: SQ_LITERAL
	;
	
assemblyAdd
    : KADD KFILE FROM cfs+=clientFileSpecifier (COMMA cfs+=clientFileSpecifier)*
    ;
    
clientFileSpecifier
	: SQ_LITERAL (AS SQ_LITERAL)?
	| ist AS SQ_LITERAL
	;
    	 
ist
	: binary (COMMA binary)*
	;
	
binary
	: HEXNUM
	;   
    	 

// End: ssembly
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// symmetric statements
//
alterAsymmetric
    : ASYMMETRIC KEY keywId alterOption
    	SEMI?
    ;
    
alterOption
	: REMOVE PRIVATE KEY
	| WITH PRIVATE KEY LPAREN akPasswordOption RPAREN
	;
		
// End: alterAsymmetric
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// alterAuthorization statements
//
alterAuthorization
    : AUTHORIZATION
    	aaOn
    	aaTo
    	SEMI?
    ;

aaOn
	: ON entityType? keywId
	;
	    
aaTo
	: TO
    	(
    		  SCHEMA OWNER
    		| keywId
    	)
	;
	
entityType
	:  	(
			  OBJECT
			| TYPE
			| XML SCHEMA COLLECTION
			| FULLTEXT CATALOG
			| SCHEMA
			| ASSEMBLY
			| ROLE
			| MESSAGE TYPE
			| CONTRACT
			| SERVICE
			| REMOTE SERVICE BINDING
			| ROUTE
			| SYMMETRIC KEY
			| ENDPOINT
			| CERTIFICATE
			| DATABASE
		)
			
			COLON COLON
	;
// End: alterAuthorization
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// alterCertificate statements
//
alterCertificate
    : CERTIFICATE keywId acOpts
    	SEMI?
    ;

acOpts
	: REMOVE PRIVATE KEY
	| WITH
		(
			  PRIVATE KEY LPAREN privateKeyList RPAREN
			| ACTIVE FOR BEGIN_DIALOG OPEQ (ON | OFF)
		)
	;
// End: alterCertificate
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// alterCredential statements
//
alterCredential
	: createCredential
    ;
// End: alterCredential
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// alterDatabase statements
//
alterDatabase
    : DATABASE keywId
    	(
    		  adAddOrModifyFiles
    		| adAddOrModifyFilegroups
    		| adSetDatabaseOptions
    		| adModifyName
    		| adCollate
    	)
    	SEMI?
    ;
    
adCollate
	: COLLATE keywId
	;
	
adModifyName
	: MODIFY NAME OPEQ keywId
	;
	
adAddOrModifyFiles
	: KADD
		(
			  KFILE dbFilespecList
			  	( 	  adfsFilegroup
			  		|
			  	)
			| LOG KFILE dbFilespecList
		)
	| REMOVE KFILE rfid=keywId
	| MODIFY KFILE dbFilespec
	;

adfsFilegroup
    : TO FILEGROUP (keywId|SQ_LITERAL)
    ;

adfsName
	: NAME OPEQ (keywId|SQ_LITERAL)
	;
	
adfsFilegrowth
	: COMMA? FILEGROWTH OPEQ INTEGER (szSuffix | OPMOD)
	;
	
adfsSize
	: COMMA? SIZE OPEQ INTEGER szSuffix
	;
	
adfsFilename
	: COMMA? FILENAME OPEQ (keywId|SQ_LITERAL)
	;
	
adfsNewname
	: COMMA? NEWNAME OPEQ (keywId|SQ_LITERAL)
	;
	
adfsMax
	: COMMA? MAXSIZE OPEQ (UNLIMITED | INTEGER szSuffix)
	;
	
szSuffix
	: KB
	| MB
	| GB
	| TB
	;
	
adAddOrModifyFilegroups
	: KADD FILEGROUP (keywId|SQ_LITERAL)
	| REMOVE FILEGROUP (keywId|SQ_LITERAL)
	| MODIFY FILEGROUP (keywId|SQ_LITERAL)
			(
				  READ_ONLY
				| READ_WRITE
				| DEFAULT
				| NAME OPEQ (keywId|SQ_LITERAL)
			)
	;

adSetDatabaseOptions
	: SET adOptionspecList adWithTermination?
	;
    
adWithTermination
    : WITH adTermination
    ;

adOptionspecList
	: ao+=adOptionspec (COMMA ao+=adOptionspec)*
	;
	
adOptionspec
	: adDbStateOption
	| adDbUaccessOption
	| adDbUpdateOption
	| adExtAccessOption
	| adCursorOption
	| adAutoOption
	| adSqlOption
	| adRecoveryOption
	| adDbMirrorOption
	| adSvcBrkrOption
	| adDateCorOptimOption
	| adParamOption
	| adSnapshotOption
    | adCompatibility
	;

adCompatibility
    : COMPATIBILITY_LEVEL OPEQ INTEGER
    ;

adDbStateOption
	: ONLINE
	| OFFLINE
	| EMERGENCY
	;
	
adDbUaccessOption
	: SINGLE_USER
	| RESTRICTED_USER
	| MULTI_USER
	;

adDbUpdateOption
	: READ_ONLY
	| READ_WRITE
	;

adExtAccessOption 
	: DB_CHAINING (ON | OFF)
	| TRUSTWORTHY (ON | OFF)
	;

adCursorOption
	: CURSOR_CLOSE_ON_COMMIT (ON | OFF)
	| CURSOR_DEFAULT (LOCAL | GLOBAL)
	;

adAutoOption
	: AUTO_CLOSE 						(ON | OFF)
	| AUTO_CREATE_STATISTICS 			(ON | OFF)
	| AUTO_UPDATE_STATISTICS			(ON | OFF)
	| AUTO_UPDATE_STATISTICS_ASYNC		(ON | OFF)
    | AUTO_SHRINK                  	(ON | OFF)
	;

adSqlOption
	: ANSI_NULL_DEFAULT 				(ON | OFF)
	| ANSI_NULLS						(ON | OFF)
	| ANSI_PADDING						(ON | OFF)
	| ANSI_WARNINGS					(ON | OFF)
	| ARITHABORT						(ON | OFF)
	| CONCAT_NULL_YIELDS_NULL			(ON | OFF)
	| NRA           				(ON | OFF)
	| QUOTED_IDENTIFIER				(ON | OFF)
	| RECURSIVE_TRIGGERS				(ON | OFF)
	;

adRecoveryOption
	: RECOVERY 			(FULL | BULK_LOGGED | SIMPLE )
	| TORN_PAGE_DETECTION	(ON | OFF)
	| PAGE_VERIFY			(CHECKSUM | TORN_PAGE_DETECTION | NONE)
	;

adDbMirrorOption
	: PARTNER
		(
			  OPEQ SQ_LITERAL
			| FAILOVER
			| FORCE_SERVICE_ALLOW_DATA_LOSS
			| OFF
			| RESUME
			| SAFETY	(ON | OFF)
			| SUSPEND
			| TIMEOUT INTEGER
		)
	| WITNESS
		(
			  OPEQ SQ_LITERAL
			| OFF
		)
	;

adSvcBrkrOption
	: ENABLE_BROKER
	| DISABLE_BROKER
	| NEW_BROKER
	| ERROR_BROKER_CONVERSATIONS
	;

adDateCorOptimOption
	: DATE_CORRELATION_OPTIMIZATION (ON | OFF)
	;

adParamOption
	: PARAMETERIZATION ( SIMPLE | FORCED )
	;

adSnapshotOption
	: ALLOW_SNAPSHOT_ISOLATION 	(ON | OFF)
	| READ_COMMITTED_SNAPSHOT		(ON | OFF)
	;
		
adTermination
	: ROLLBACK AFTER INTEGER SECONDS?
	| ROLLBACK IMMEDIATE
	| NO_WAIT
	;
// End: alterDatabase
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// alterEndpoint statements
//
alterEndpoint
    : ENDPOINT keywId
    	aeAuth?
    	aeState?
    	aeAs?
    	aeFor
    	SEMI?
    ;

aeState
	: STATE OPEQ
    			(
    				  STARTED
    				| STOPPED
    				| DISABLED
    			)
	;
	
aeAuth
	: AUTHORIZATION keywId
	;
	    
aeAs
	: AS epProtocols
	;
	
aeFor
    : FOR epLanguages
	;
    	
epProtocols
	: HTTP
		LPAREN
			epProtocolsHttpPath?
			epProtocolsHttpPorts
			epProtocolsHttpSite?
			epProtocolsHttpClearPort?
			epProtocolsHttpSslPort?
            epProtocolsHttpAuthentication?
			epProtocolsHttpAuthRealm?
			epProtocolsHttpDefaultLoginDomain?
			epProtocolsHttpCompression?
		RPAREN
	| TCP
		LPAREN
			epProtocolsTcpListenerPort
			epProtocolsTcpListenerIp?
		RPAREN
	;

epProtocolsTcpListenerPort
	: LISTENER_PORT OPEQ INTEGER
	;
	
epProtocolsTcpListenerIp
	: COMMA? LISTENER_IP OPEQ
						(
							  ALL
							| fourPartIp
							| LPAREN DQ_LITERAL RPAREN
						)
	;
	
epProtocolsHttpPath
	: COMMA? PATH OPEQ SQ_LITERAL
	;
	
epProtocolsHttpPorts
	: COMMA? PORTS OPEQ LPAREN ( CLEAR SSL? | SSL CLEAR? ) RPAREN
	;
	
epProtocolsHttpSite
	: COMMA? SITE OPEQ ( OPMUL | OPPLUS | SQ_LITERAL )
	;

epProtocolsHttpClearPort
	: COMMA? CLEAR_PORT OPEQ INTEGER
	;
	
epProtocolsHttpSslPort
	: COMMA? SSL_PORT OPEQ INTEGER
	;
	
epProtocolsHttpAuthentication
	: COMMA? AUTHENTICATION OPEQ
				LPAREN
					epAuthList
				RPAREN
	;
	
epProtocolsHttpAuthRealm
	: COMMA? AUTH_REALM OPEQ (SQ_LITERAL | NONE)
	;
	
epProtocolsHttpDefaultLoginDomain
	: COMMA? DEFAULT_LOGON_DOMAIN OPEQ (SQ_LITERAL | NONE)
	;
	
epProtocolsHttpCompression
	: COMMA? COMPRESSION OPEQ (ENABLED | DISABLED)
	;
	

fourPartIp
	: INTEGER DOT INTEGER DOT INTEGER DOT INTEGER
	;
	
epAuthList
	: epAuth (COMMA epAuth)*
	;
	
epAuth
	: BASIC
	| DIGEST
	| NTLM
	| KERBEROS
	| INTEGRATED
	;
	
epLanguages
	: epSoap
	| epServiceBroker
	| epDatabaseMirroring
	| TSQL
	;

epSoap
	: SOAP
		LPAREN
			epAddWebmethodList?
			epAlterWebmethodList?
			(COMMA? epDropWebmethodList)?
            (COMMA? epSoapOptlist)?
        RPAREN
	;

epSoapOptlist
	: epSoapOpt (COMMA? epSoapOpt)*
	;

epSoapOpt
	: BATCHES 			OPEQ (ENABLED | DISABLED)
	| WSDL 			OPEQ (NODE | DEFAULT| SQ_LITERAL)
	| SESSIONS 		OPEQ (ENABLED | DISABLED)
	| LOGIN_TYPE 		OPEQ (MIXED | WINDOWS)
	| SESSION_TIMEOUT	OPEQ INTEGER
	| DATABASE 		OPEQ (SQ_LITERAL | DEFAULT)
	| NAMESPACE 		OPEQ (SQ_LITERAL | DEFAULT)
	| SCHEMA 			OPEQ (NONE | STANDARD)
	| CHARACTER_SET 	OPEQ (SQL | XML)
	| HEADER_LIMIT 	OPEQ INTEGER
	;

epAddWebmethodList
	: epAddWebmethod (COMMA epAddWebmethod)*
	;

epAddWebmethod
	: KADD WEBMETHOD SQ_LITERAL (DOT SQ_LITERAL)?
		epWmParams
	;
	
epAlterWebmethodList
	: epAlterWebmethod (COMMA epAlterWebmethod)*
	;
	
epAlterWebmethod
	: ALTER WEBMETHOD SQ_LITERAL (DOT SQ_LITERAL)?
		epWmParams
	;
	
epWmParams
	: 	LPAREN
			epWmParamsName
			epWmParamsSchema?
			epWmParamsFormat?
		RPAREN
	;
	
epWmParamsName
	: NAME OPEQ SQ_LITERAL
	;
	
epWmParamsSchema
	: COMMA SCHEMA OPEQ (NONE | STANDARD | DEFAULT)
	;
	
epWmParamsFormat
	: COMMA FORMAT OPEQ (ALL_RESULTS | ROWSETS_ONLY | NONE)
	;
	
epDropWebmethodList
	: epDropWebmethod (COMMA epDropWebmethod)*
	;
	
epDropWebmethod
	: DROP WEBMETHOD SQ_LITERAL (DOT SQ_LITERAL)?
	;
	
epServiceBroker
	: SERVICE_BROKER
		LPAREN
			epSbAuthentication?
			epSbEncryption?
			epSbMessageForwarding?
			epSbMessageForwardSize?
		RPAREN
	;

epSbMessageForwarding
	: COMMA? MESSAGE_FORWARDING OPEQ (ENABLED | DISABLED)
	;

epSbMessageForwardSize
	: COMMA? MESSAGE_FORWARD_SIZE OPEQ INTEGER
	;
	
epSbAuthentication
	: AUTHENTICATION OPEQ
			(
				  w=WINDOWS (n=NTLM | ker=KERBEROS | neg=NEGOTIATE)? (c=CERTIFICATE k=keywId)?
				| c=CERTIFICATE k=keywId  (w=WINDOWS (n=NTLM | ker=KERBEROS | neg=NEGOTIATE)?)?
			)
	;
	
epSbEncryption
	: COMMA? ENCRYPTION OPEQ
					(
						  DISABLED
						| (SUPPORTED | REQUIRED) 
								(ALGORITHM ID )?
					)
	;
				
epDatabaseMirroring
	: DATABASE_MIRRORING
		LPAREN
			epSbAuthentication?
			epSbEncryption?
			epDatabaseMirroringRole
		RPAREN
	;

epDatabaseMirroringRole
	: COMMA? ROLE OPEQ (WITNESS | PARTNER | ALL)
	;
	
// End: alterEndpoint
///////////////////////////////////////////////////////////


///////////////////////////////////////////////////////////
// alterFulltext statements
//
alterFulltext
    : FULLTEXT
    	(	
    		  alterFulltextCatalog
		    | alterFulltextIndex
	    )
	  SEMI?
    ;

alterFulltextIndex
	: KINDEX ON keywId
    	(
    		  ENABLE
    		| DISABLE
    		| SET CHANGE_TRACKING (MANUAL | AUTO | OFF )
    		| KADD LPAREN
    				fulltextCol (COMMA fulltextCol)*
    			  RPAREN
    			  ( WITH NO POPULATION )?
    			  
    		| DROP
    			LPAREN
    				keywIdList 
    			RPAREN
    			 ( WITH NO POPULATION )?
    		| START ( FULL | INCREMENTAL | UPDATE ) POPULATION
    		| ( STOP | PAUSE | RESUME) POPULATION
    	)
	;
	
alterFulltextCatalog
	:	CATALOG keywId
    	(
    		  REBUILD (WITH ACCENT_SENSITIVITY OPEQ (ON | OFF))?
    		| REORGANIZE
    		| AS DEFAULT
    	)
	;
	
fulltextCol
	: ki1=keywId ( TYPE COLUMN ki2=keywId )? (LANGUAGE languageTerm)?
	;
 
languageTerm
	: SQ_LITERAL
	| HEXNUM
	;
	
// End: alterFulltext
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// alterFunction statements
//
alterFunction
	: FUNCTION keywId
		alterFunctionParams
		alterFunctionReturns
		SEMI?
	;

// Parameter specification is good for all types of
// functions: CLR, inline table-value, etc.
//
alterFunctionParams
	:	LPAREN
			(
				fps+=functionParameterSpec (COMMA fps+=functionParameterSpec)*
			)?
		RPAREN
	;
	
// Syntax available here vairies according to the type of the function
// which we do not know or care to know at this point of course becaues
// this is the parser and does not do semantic checks. Semantics are
// left for the tree-parser.
// Hence we can have all of the syntax for each type of function come next,
// thoguh we can syntactically differentiate the types to some degree, we do
// so only with a rewrite rule to the tree grammar.
//
alterFunctionReturns
	:	RETURNS
		(
			// Scalar functions return data elelements and so are typed
			// as such. Note that data types are picked up as identifiers
			// and then checked semantically to ensure their validity. Again,
			// this type of semantic checking is left to the tree parser
			// 
			   dataType
			   (
			   		// However, if we have an identifier followed by a
			   		// TABLE keyword, then this is a Multistatement table-valued
			   		// function, which allows a slightly different syntax
			   		//
			   		afrTable?
			   		(afrWith)?
					afrAs	   		
			   )
			| TABLE tableTypeDefinition?
				( WITH functionOption (COMMA functionOption)*)?
				AS?
				(
					  BEGIN
						functionBody
						RETURN
					  END
					| RETURN
						LPAREN		// Inline table-bodied function
							selectStatement
						RPAREN
				)
		)
    ;

afrAs
	: AS?		
		(
			  functionBody
			| EXTERNAL NAME keywId	// For CLR Functinos ONLY
		)
	;
	
	
afrWith
	: WITH functionOption (COMMA functionOption)*
	;
	
afrTable
	: TABLE tableTypeDefinition
	;
    
tableTypeDefinition
	: LPAREN
		ctColDefList
		
	  RPAREN
	;
	
filegroup
	: SQ_LITERAL
	| INTEGER
	;

indexOptionList
	: io+=indexOption (COMMA io+=indexOption)*
	;
	
indexOption
	: (MAXDOP|FILLFACTOR) OPEQ INTEGER
	| (
		  PAD_INDEX
		| IGNORE_DUP_KEY
		| STATISTICS_NORECOMPUTE
		| ALLOW_ROW_LOCKS
		| ALLOW_PAGE_LOCKS
        | ONLINE
        | SORT_IN_TEMPDB
	  ) 
			OPEQ ( ON | OFF)
    | tableOption // SQL 2008 R2
	;
	
functionOption
	: ENCRYPTION					// Exclude in smeantic checking if CLR function
	| SCHEMABINDING					// Exclude in semantic checking if CLR function
	| RETURNS KNULL ON KNULL KINPUT // This clause and CALLED ON are mutually exclusive. Check in semantic pass
	| CALLED ON KNULL KINPUT
	| executeAsClause
	;
	
executeAsClause
	: EXECUTE AS (CALLER | SELF | OWNER | SQ_LITERAL ) // EXECUTE is tokenzied by EXEC or EXECUTE keywords
	;
	
functionBody
	: statements
	;
	
functionParameterSpec
	: keywId AS? dataType (OPEQ expression)?
	;
	
dataType
    : dataTypeEl
    ;

dataTypeEl
	: keywId
		(
			LPAREN (INTEGER|KMAX|KMIN) (COMMA INTEGER)? RPAREN
		)?
	;
	
// End: alterFunction
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// alterIndex statements
//
alterIndex
    : KINDEX (keywId | ALL)
    	ON keywId
    	(
    		  REBUILD
    		  	(
    		  		  aiWith
    		  		| aiPartition
    		  	)?
    		| DISABLE
    		| REORGANIZE
    			(
    				PARTITION OPEQ INTEGER
    			)?
    			(
    				WITH LPAREN LOB_COMPACTION OPEQ (ON | OFF) RPAREN
    			)?
    		| SET LPAREN setIndexOptionList RPAREN
    	)
    	SEMI?
    ;
    
aiPartition
	: PARTITION OPEQ (INTEGER| ALL)
    		  	(
    		  		WITH LPAREN spRebuildIndexOptionList RPAREN
    		  	)?
	;
	
aiWith
	: WITH LPAREN rebuildIndexOptionList RPAREN
	;
	
setIndexOptionList
	: s+=setIndexOption (COMMA s+=setIndexOption)*
	;

setIndexOption
	: ( ALLOW_ROW_LOCKS | ALLOW_PAGE_LOCKS | IGNORE_DUP_KEY | STATISTICS_NORECOMPUTE)
		OPEQ
			(ON|OFF)
	;

spRebuildIndexOptionList
	: spRebuildIndexOption (COMMA spRebuildIndexOption)*
	;
	
spRebuildIndexOption
	: MAXDOP OPEQ INTEGER
	| SORT_IN_TEMPDB OPEQ (ON | OFF)
    | tableOption
	;

rebuildIndexOptionList
	: o+=rebuildIndexOption (COMMA o+=rebuildIndexOption)*
	;

rebuildIndexOption
	: (MAXDOP | FILLFACTOR ) OPEQ INTEGER
	|
		(
			  PAD_INDEX
			| SORT_IN_TEMPDB
			| IGNORE_DUP_KEY
			| STATISTICS_NORECOMPUTE
			| ONLINE
			| ALLOW_ROW_LOCKS
		)
			OPEQ (ON | OFF)
	;
// End: alterIndex
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// alterLogin statements
//
alterLogin
    : LOGIN
    	keywId		// Login name is NOT delimited (which is stupid but that's what you get
    	(
    		  ENABLE
    		| DISABLE
    		| WITH setOptionList
    	)
  	  SEMI?
	;

setOptionList
	: setOption (COMMA setOption)*
	;
	
setOption
	: PASSWORD OPEQ SQ_LITERAL HASHED?
    	(
    		  OLD_PASSWORD OPEQ SQ_LITERAL
    		| MUST_CHANGE UNLOCK?
    		| UNLOCK MUST_CHANGE?	
    	)?
    | (
    	  DEFAULT_DATABASE 
    	| DEFAULT_LANGUAGE
    	| CREDENTIAL
    	| NAME
      )
    	OPEQ keywId
    | (
    	  CHECK_POLICY
    	| CHECK_EXPIRATION
      )
      	OPEQ (ON | OFF)
    | NO CREDENTIAL
    ;
// End: alterLogin
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// alterMaster statements
//
alterMaster
    : MASTER KEY
    	(
    		  FORCE? REGENERATE WITH ENCRYPTION BY PASSWORD OPEQ SQ_LITERAL
    		| (KADD | DROP)
    				ENCRYPTION BY 	(
    									  SERVICE MASTER KEY
    									| PASSWORD OPEQ SQ_LITERAL
    								)
    	)
    	SEMI?
    ;
// End: alterMaster
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// alterMessage statements
//
alterMessage
    : MESSAGE TYPE keywIdPart		// Not allowed to have server or database names
    
    	VALIDATION 
    	  OPEQ
    		(
    			  NONE
    			| EMPTY
    			| WELL_FORMED_XML
    			| VALID_XML WITH SCHEMA COLLECTION keywId
    		)
    	SEMI?
    ;
// End: alterMessage
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// alterPartition statements
//
alterPartition
    : PARTITION
    	(
    		  FUNCTION keywId LPAREN RPAREN
    		  (
    		  	(SPLIT | MERGE) RANGE LPAREN expression RPAREN
    		  )
    		| SCHEME keywId NEXT USED (keywId|SQ_LITERAL)?
    	)
    	SEMI?
    ;
// End: alterPartition
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// alterProcedure statements
//
alterProcedure
    : PROCEDURE keywId (SEMI INTEGER)?
    
		procedureParamList?
    	alterProcedureWith?
    	(FOR REPLICATION)?
    	alterProcedureAs
    ;

alterProcedureWith
	: WITH procedureOptionList
	;
	
alterProcedureAs
	: AS
    	(
    		  EXTERNAL NAME keywId SEMI?
    		| unblockedStatements
    	)
	;
	
// End: alterProcedure
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// alterQueue statements
//
alterQueue
    : QUEUE keywId WITH
    	queueElementList
    	SEMI?
    ;
	
// End: alterQueue
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// alterRemote statements
//
alterRemote
    : REMOTE SERVICE BINDING keywId
		createRemoteWith
    	SEMI?
    ;
// End: alterRemote
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// rRole statements
//
alterRole
    : ROLE
    	keywId WITH NAME OPEQ keywId
    	SEMI?
    ;
// End: rRole
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// rRoute statements
//
alterRoute
    : ROUTE keywIdPart
    	routeWith
    	SEMI?
    ;   
 
// End: rRoute
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// rSchema statements
//
alterSchema
    : SCHEMA
    	keywId TRANSFER keywId
    	SEMI?
    ;
// End: rSchema
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// alterService statements
//
alterService
    : SERVICE
    	(
	    	  keywIdPart asQueueOpts
	    	| asMaster
	    )
    	SEMI?
    ;

asMaster
    : MASTER KEY
        (
              asRegenerateOpt
            | asRecoverOpt
            | asAddDrop
        )
    ;

asRegenerateOpt
    : FORCE? REGENERATE
    ;

asRecoverOpt
    : WITH OLD_ACCOUNT OPEQ SQ_LITERAL COMMA OLD_PASSWORD OPEQ SQ_LITERAL
    | WITH NEW_ACCOUNT OPEQ SQ_LITERAL COMMA NEW_PASSWORD OPEQ SQ_LITERAL
    ;

asAddDrop
    : (KADD | DROP) ENCRYPTION BY MACHINE KEY
    ;

asQueueOpts
    : (
          ON q=QUEUE k=keywId s=serviceOptsList?
	 	| s=serviceOptsList (ON q=QUEUE k=keywId)?
      )
    ;

serviceOptsList
	: LPAREN s+=serviceOpts (COMMA s+=serviceOpts)* RPAREN
	;
	
serviceOpts
	: KADD CONTRACT keywIdPart
	| DROP CONTRACT keywIdPart
	;

// End: alterService
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// alterSymmetric statements
//
alterSymmetric
    : SYMMETRIC KEY keywId alterSymmetricOption
    	SEMI?
    ;

alterSymmetricOption
	: alterSymDropList
	| alterSymAddList
	;

alterSymDropList
	: a+=alterSymDrop (COMMA a+=alterSymDrop)*
	;

alterSymDrop
	: DROP ENCRYPTION BY encryptingMechanism
	;

encryptingMechanism
	: CERTIFICATE keywId
	| PASSWORD OPEQ SQ_LITERAL
	| (ASYMMETRIC | SYMMETRIC) KEY keywId
	;
	
alterSymAddList
	: a+=alterSymAdd (COMMA a+=alterSymAdd)*
	;
	
alterSymAdd
	: KADD ENCRYPTION BY encryptingMechanism
	;

// End: alterSymmetric
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// alterTable statements
//
alterTable
    : TABLE keywId
    	(
    		  atAlterColumn
    		| withList
    		| DROP 	conWithColList
    		| (ENABLE | DISABLE)? TRIGGER
    				(
    					  ALL
    					| keywIdList
    				)
    		| SWITCH 	(PARTITION expression)?
    			TO keywId
    					(PARTITION expression)?
            | SET
                LPAREN
                    FILESTREAM_ON OPEQ
                        (    expression
                            | DEFAULT
                        )
                RPAREN
            | REBUILD
                (PARTITION OPEQ (ALL|expression))?
                (WITH LPAREN indexOptionList RPAREN)?
    	)
    	SEMI?
    ;

atAlterColumn
    : ALTER COLUMN columnName
    		  (
                  atAlterColumnAddDrop
    			| atAlterColumnNamed
    		  )
    ;

atAlterColumnNamed
    : alterColumnNamedItem
    ;

alterColumnNamedItem
    : keywId
            (
                LPAREN
                    (
                          INTEGER (COMMA INTEGER)?
                        | KMAX
                        | keywId			// xmlSchemaCollection
                    )
                RPAREN
            )?
            ( COLLATE SQ_LITERAL )?
            ( KNULL | KNOT KNULL)?
    ;

atAlterColumnAddDrop
    : (KADD | DROP)
        (	  ROWGUIDCOL
            | PERSISTED
            | notForReplication
        )
    ;

conWithColList
	: c+=conWithCol (COMMA c+=conWithCol)*
	;
	
conWithCol
	: (CONSTRAINT)? keywId
    		( WITH dropClusterConList )?
    | COLUMN keywId
	;
	
dropClusterConList
	: LPAREN
		d+=dropClusterConOpt (COMMA d+=dropClusterConOpt)*
	  RPAREN
	;
	
dropClusterConOpt
	: MAXDOP OPEQ INTEGER
	| ONLINE OPEQ (ON | OFF)
	| MOVE TO
		(
			  keywId ( LPAREN keywId RPAREN )?
		)
	;
    
withList
	: w+=withAdd (COMMA w+=withAdd)*
	;
	
withAdd
	: (WITH? (CHECK | NOCHECK))?
			(
				  KADD
    				ctColDefList
    			| CONSTRAINT
    				(
    					  ALL
    					| keywIdList
    				)
    		)
	;
	
	
// End: alterTable
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// alterTrigger statements
//
alterTrigger
    : createTrigger
    ;
	
// End: alterTrigger
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// alterUser statements
//
alterUser
    : USER keywId
    		WITH commonSetItemList	// Note - semantics must exclude some options for this
    	SEMI?
    ;
// End: alterUser
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// alterView statements
//
alterView
    : createView
    ;
    
// End: alterView
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// alterXml statements
//
alterXml
    : createXml
    ;
// End: alterXml
///////////////////////////////////////////////////////////
