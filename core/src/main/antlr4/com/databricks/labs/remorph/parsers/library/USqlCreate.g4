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

parser grammar USqlCreate;


///////////////////////////////////////////////////////////
// CREATE statements
createStatement
	: CREATE
		(
			  createAggregate
			| createApplication
			| createAssembly
			| createAsymmetric
			| createCertificate
            | createContract
			| createCredential
			| createDatabase
            | createDefault
			| createEndpoint
            | createEvent
			| createFulltext
			| createFunction
			| createIndex
			| createLogin
			| createMaster
			| createMessage
			| createPartition
			| createProcedure
			| createQueue
			| createRemote
			| createRole
			| createRoute
            | createRule
			| createSchema
			| createService
            | createStatistics
			| createSymmetric
            | createSynonym
			| createTable
			| createTrigger
            | createType
			| createUser
			| createView
			| createXml
		)
	;
// End: CREATE statements
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// createAggregate statements
//
createAggregate
	: AGGREGATE keywId
		LPAREN
			expression expression
		RPAREN
	  commonReturns
	  externalName
      SEMI?
	;
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// createApplication statements
//
createApplication
    : APPLICATION cappRole cappList SEMI?
    ;

cappRole
    : ROLE keywId
    ;

cappList
    : WITH commonSetItemList
    ;
	
// End: createApplication
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// createAssembly statements
//
createAssembly
    : ASSEMBLY assemblyName
		authorization?
    	assemblyFrom
    	assemblyWith?
    	SEMI?
    ;

	
// End: createAssembly
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// createAsymmetric statements
//
createAsymmetric
    : ASYMMETRIC KEY keywId
		authorization?
		createAsmOption 
		akPasswordOption?
    	SEMI?
    ;
    
createAsmOption
	: FROM asymKeySource
	| WITH ALGORITHM OPEQ keywId
	;
	
asymKeySource
	: EXECUTABLE? KFILE OPEQ SQ_LITERAL
	| ASSEMBLY SQ_LITERAL
	;
	
		
// End: createAsymmetric
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// createCertificate statements
//
createCertificate
    : CERTIFICATE keywId
		authorization?
		ccKeyOpts
		ccActive?
    	SEMI?
    ;

ccActive
    : ACTIVE FOR BEGIN DIALOG OPEQ (ON|OFF)
    ;
ccKeyOpts
	: FROM
		(
			  existingKeys
		)
    | generateNewKeys
	;

existingKeys
	: ASSEMBLY keywId
	| (EXECUTABLE? KFILE OPEQ SQ_LITERAL)?
	  (WITH PRIVATE KEY LPAREN privateKeyList RPAREN)?
	;

generateNewKeys
	: akPasswordOption? WITH
		(COMMA? dateOptions)*
	;

dateOptions
	: START_DATE OPEQ SQ_LITERAL
	| EXPIRY_DATE OPEQ SQ_LITERAL
    | SUBJECT OPEQ SQ_LITERAL
	;

// End: createCertificate
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// 
createContract
	: CONTRACT keywId
		authorization?
		LPAREN
			contractElementList
		RPAREN
		SEMI?
	;

contractElementList
	: contractElement (COMMA contractElement)*
	;
	
contractElement
	: contractName contractBy
	;

contractBy
    : SENT BY ( INITIATOR | TARGET | ANY)
    ;

contractName
    : sqBrLiteral
    ;

///////////////////////////////////////////////////////////
	
///////////////////////////////////////////////////////////
// createCredential statements
//
createCredential
	: CREDENTIAL keywId WITH IDENTITY OPEQ SQ_LITERAL
		( COMMA SECRET OPEQ SQ_LITERAL)?
		SEMI?
    ;
// End: createCredential
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// createDatabase statements
//
createDatabase
    : DATABASE keywId
		cdOption*
    	SEMI?
    ;

cdOption
    : cdOnClause
    | cdForOption
    | cdLogOption
    | cdCollateClause
    | cdWithClause
    | cdAs
    ;

cdCollateClause
	: COLLATE keywId COMMA?
	;

cdWithClause
	: WITH cdExtAccessOption+
	;

cdExtAccessOption
    :   (
              (DB_CHAINING | TRUSTWORTHY) (ON|OFF)
        ) COMMA?
    ;

cdOnClause
	: ON
        (
            PRIMARY?

            dbFilespecList? COMMA?
            cdFilegroupList?
        )
    ;

cdAs
    : AS cdSnapshotList
    ;

cdSnapshotList
	: cs+=cdSnapshot (COMMA cs+=cdSnapshot)* AS SNAPSHOT OF keywId
	;

cdSnapshot
	: LPAREN
		NAME OPEQ keywId COMMA FILENAME OPEQ SQ_LITERAL
	  RPAREN
	;
	
cdLogOption
	: LOG ON dbFilespecList COMMA?
	;
	
cdFilegroupList
	: cf+=cdFilegroup (COMMA cf+=cdFilegroup)*
	;
	
cdFilegroup
	: FILEGROUP keywId (CONTAINS FILESTREAM)? DEFAULT? dbFilespecList
	;

cdForOption
	: FOR
		(
			  ATTACH (WITH cdServiceBrokerOption)?
			| ATTACH_REBUILD_LOG
		) COMMA?
	;

cdServiceBrokerOption
	: ENABLE_BROKER
	| NEW_BROKER
	| ERROR_BROKER_CONVERSATIONS
	;
// End: createDatabase
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// createDefault statements
// (Deprecated).
//
createDefault
	: DEFAULT keywId AS expression SEMI?
	;

///////////////////////////////////////////////////////////
// createEndpoint statements
//
createEndpoint
    : ENDPOINT keywId
        authorization?
        ceState?
    	ceAs?
        ceFor
      SEMI?
    ;

ceFor
    : FOR cepLanguages
    ;


cepLanguages
	: cepSoap
	| epServiceBroker
	| epDatabaseMirroring
	| TSQL
	;

cepSoap
	: SOAP
		LPAREN
			epWebmethodList?
		
            (COMMA? epSoapOptlist)?
        RPAREN
	;

epWebmethodList
	: epWebmethod (COMMA epWebmethod)*
	;

epWebmethod
	: WEBMETHOD SQ_LITERAL (DOT SQ_LITERAL)?
		epWmParams
	;

ceAs
    : AS cepProtocols
    ;

cepProtocols
	: HTTP
		LPAREN
			epProtocolsHttpPath
            epProtocolsHttpAuthentication
			epProtocolsHttpPorts
			epProtocolsHttpSite?
			epProtocolsHttpClearPort?
			epProtocolsHttpSslPort?
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


ceState
    : STATE OPEQ
        (
              STARTED
            | STOPPED
            | DISABLED
        )
    ;

// End: createEndpoint
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// createEvent statements
//
createEvent
	: EVENT NOTIFICATION keywId
		eventOn
		( WITH FAN_IN)?
	  eventNameFor
	  eventTo
	  SEMI?
	;

eventTo
    : TO SERVICE SQ_LITERAL (COMMA SQ_LITERAL)?
    ;

eventOn
    : ON (
				  SERVER
				| DATABASE
				| QUEUE keywId
			)
    ;

eventNameFor
	: FOR eventNameList
    ;

eventNameList
    : e+=eventName (COMMA e+=eventName)*
	;
		
eventName
	: keywId
	;
	
	
// End: createEndpoint
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// createFulltext statements
//
createFulltext
    : FULLTEXT
    	(
	    	  fulltextCatalog

		    | fulltextIndex
	    )
	  SEMI?
    ;

fulltextCatalog
    : CATALOG keywId
        fulltextFilegroup?
        fulltextPath?
        fulltextAccent?
        ( AS DEFAULT)?
        authorization?
    ;

fulltextFilegroup
    : ON FILEGROUP filegroup
    ;

fulltextPath
    : KIN PATH SQ_LITERAL
    ;

fulltextAccent
    : WITH ACCENT_SENSITIVITY OPEQ (ON | OFF)
    ;

fulltextIndex
    : KINDEX ON keywId
		        LPAREN
					fulltextCol (COMMA fulltextCol)*
		        RPAREN
		        fulltextKey
				fulltextChangeTracking?
    ;

fulltextKey
    : KEY KINDEX keywId
					(ON keywId)?
    ;

fulltextChangeTracking
    : WITH CHANGE_TRACKING (MANUAL | AUTO | OFF )
		(COMMA NO POPULATION )?
    ;

// End: createFulltext
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// createFunction statements
//
createFunction
	: alterFunction
	;

// End: createFunction
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// createIndex statements
//
createIndex
	:	(
		    UNIQUE? (CLUSTERED | NONCLUSTERED)?
			KINDEX keywId
    		ciOn 
			ciInclude?
			ciWith?
			ciOn2?

		 | PRIMARY? ciXmlIndex keywId
    		ciOn3
    		ciXmlIndexUsing?
            ciXmlIndexWith?
         | spatialIndex
    	)
    	SEMI?
    ;

spatialIndex
    : SPATIAL KINDEX keywId
        ON
        (
            (keywId | DEFAULT)
            | LPAREN columnName RPAREN
            // TODO: Implement all spatial index syntax
        )
    ;

ciXmlIndexWith
    : WITH LPAREN xmlIndexOptionList RPAREN
    ;

ciXmlIndexUsing
    : USING XML KINDEX keywId
    			( FOR (VALUE | PATH | PROPERTY) )?
    ;
    
ciXmlIndex
    : XML KINDEX
    ;

ciOn3
    : ON keywId LPAREN keywId RPAREN
    ;

ciOn2
    : ON (keywId | SQ_LITERAL) (LPAREN keywId RPAREN)?
    ;

ciOn
    : ON keywId colListParen
    ;

ciInclude
    : INCLUDE colListParen
    ;

ciWith
    : WITH
        /* Prior to T-SQL 2005 the parens seem optional */
        (
              LPAREN relationalIndexOptionList RPAREN
            | relationalIndexOptionList
        )
    ;

colListParen
    : LPAREN
        columnName (ASC|DESC)? (COMMA columnName (ASC|DESC)?)*
      RPAREN
    ;

relationalIndexOptionList
	: r+=relationalIndexOption (COMMA r+=relationalIndexOption)*
	;
	
relationalIndexOption
	: xmlIndexOption
	| 
		(
			  IGNORE_DUP_KEY
			| ONLINE
		) 
			OPEQ (ON | OFF)
	;
	
xmlIndexOptionList
	: xmlIndexOption (COMMA xmlIndexOption)*
	;
	
xmlIndexOption
	: (MAXDOP | FILLFACTOR ) OPEQ INTEGER
	|
		(
			  PAD_INDEX
			| SORT_IN_TEMPDB
			| STATISTICS_NORECOMPUTE
			| ALLOW_ROW_LOCKS
			| ALLOW_PAGE_LOCKS
			| DROP_EXISTING
		)
			(OPEQ (ON | OFF))?
    | tableOption // SQL 2008 R2
	;
// End: createIndex
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// createLogin statements
//
createLogin
    : LOGIN
    	keywId		// Login name is NOT delimited (which is stupid but that's what you get
    	clFromWith
  	  SEMI?
	;

clFromWith
    : FROM loginSources
    | WITH clOptionList
    ;


loginSources
		// Note that this allows too many options for WINDOWS - check semantically
		//
	: WINDOWS (WITH clOption (COMMA clOption)*)?
	| CERTIFICATE keywId
	| ASYMMETRIC KEY keywId
	;
	
clOptionList
	: PASSWORD OPEQ SQ_LITERAL HASHED? MUST_CHANGE?
			(COMMA clOption)*
	;
	
clOption
	: SID OPEQ expression
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
    ;
    
// End: createLogin
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// createMaster statements
//
createMaster
    : MASTER KEY
    	ENCRYPTION BY PASSWORD OPEQ SQ_LITERAL
      SEMI?
    ;
// End: createMaster
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// createMessage statements
//
createMessage
    : MESSAGE TYPE keywIdPart		// Not allowed to have server or database names
		authorization?
    	cmValidation?
    	SEMI?
    ;

cmValidation
    : VALIDATION
    	  OPEQ
    		(
    			  NONE
    			| EMPTY
    			| WELL_FORMED_XML
    			| VALID_XML WITH SCHEMA COLLECTION keywId
    		)
    ;

// End: createMessage
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// createPartition statements
//
createPartition
    : PARTITION
		(
    			cpFunction
    		|	cpScheme
    	)
    	SEMI?
    ;

cpFunction
    : FUNCTION keywId LPAREN dataType RPAREN
    			AS RANGE (LEFT|RIGHT)?
    			FOR VALUES LPAREN expressionList RPAREN
    ;

cpScheme
    : SCHEME keywId
        AS PARTITION keywId
    	ALL? TO LPAREN
    					 keywIdList	// Spec says PRIMARY must be used here as [PRIMARY]
    					RPAREN
    ;

// End: createPartition
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// createProcedure statements
//
createProcedure
    : PROCEDURE keywId (SEMI INTEGER)?
    	procedureParamList?
    	cprocWith?
    	(FOR REPLICATION)?
    	cprocAs
    ;

cprocAs
    : AS
    		(
    			  EXTERNAL NAME keywId SEMI?
    			| unblockedStatements
    		)
    ;

cprocWith
    : WITH procedureOptionList
    ;

procedureOptionList
	: procedureOption+
	;

procedureOption
	: ENCRYPTION
	| RECOMPILE
	| executeAsClause
	;
	
procedureParamList
    : LPAREN procedureParamListBody RPAREN
    | procedureParamListBody
    ;
    
procedureParamListBody
	: pp+=procedureParam (COMMA pp+=procedureParam)*
	;

procedureParam
	: keywIdPart AS? ctDataType  procedureParamDefault? ( KOUT | OUTPUT)?
	;

procedureParamDefault
    : OPEQ expression
    ;

// End: createProcedure
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// createQueue statements
//
createQueue
    : QUEUE keywId
    	queueElementWith?
        queueOn?
    	SEMI?
    ;

queueOn
    : ON (keywId | DEFAULT)
    ;

queueElementWith
    : WITH queueElementList
    ;

queueElementList
	: q+=queueElement (COMMA q+=queueElement)*
	;

queueElement
	: ( RETENTION | KSTATUS ) OPEQ (ON | OFF)
	|
		ACTIVATION
		LPAREN
			(
				  qeActivationList
				| DROP      // Only for ALTER version really
			)
		RPAREN
	;

qeActivationList
	: qeActivation (COMMA qeActivation)*
	;

qeActivation
	: PROCEDURE_NAME OPEQ keywId
	| MAX_QUEUE_READERS OPEQ INTEGER
    | KSTATUS  OPEQ (ON | OFF)
	| executeAsClause
	;
	
// End: createQueue
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// createRemote statements
//
createRemote
    : REMOTE SERVICE BINDING keywId
        authorization?
        TO SERVICE SQ_LITERAL
    	createRemoteWith
    	SEMI?
    ;

createRemoteWith
    : WITH
        (
              remoteUserOpt (COMMA remoteAnonOpt)?
            | remoteAnonOpt (COMMA remoteUserOpt)?
        )
    ;

remoteUserOpt
	: USER OPEQ keywIdPart
	;
	
remoteAnonOpt
	: ANONYMOUS OPEQ (ON |OFF)
	;
	
// End: createRemote
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// rRole statements
//
createRole
    : ROLE
    	keywId authorization?
    	SEMI?
    ;
// End: rRole
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// rRoute statements
//
createRoute
    : ROUTE keywIdPart
        authorization?
    	routeWith
    	SEMI?
    ;

routeWith
    : WITH routeOptionList
    ;

routeOptionList
	: ro+=routeOption (COMMA ro+=routeOption)*
	;

routeOption
    : routeOptionElement
    ;

routeOptionElement
	: (SERVICE_NAME | BROKER_INSTANCE | ADDRESS | MIRROR_ADDRESS)
			OPEQ SQ_LITERAL
	| LIFETIME OPEQ INTEGER
	; 
// End: rRoute
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// createRule statements
//
createRule
    : RULE keywId AS searchCondition SEMI?
    ;

// End: createRule statements

///////////////////////////////////////////////////////////
// createSchema statements
//
createSchema
    : SCHEMA
    	schemaNameClause
        schemaElements?
    ;

schemaNameClause
    : (
          s=keywId a=authorization?
        | a=authorization
      )
    ;

schemaElements
    : se+=schemaElement+
    ;

schemaElement
    : se=schemaElementItem
    ;

schemaElementItem
    : CREATE (createTable | createView )
    | grantStatement
    | revokeStatement
    | denyStatement
    ;

// End: rSchema
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// createService statements
//
createService
    : SERVICE keywIdPart
        authorization?
    	crServiceQueueOptions
	    contracts?
    	SEMI?
    ;

contracts
    : LPAREN cn+=csContractName (COMMA cn+=csContractName)* RPAREN
    ;

csContractName
    : sqBrLiteral
    ;

crServiceQueueOptions
    : ON QUEUE q=keywId
    ;

// End: createService
///////////////////////////////////////////////////////////


///////////////////////////////////////////////////////////
// createStatistics statements
//
createStatistics
    : STATISTICS
        keywId
        csOn
        csWith?
        SEMI?
    ;

csWith
    : WITH
        (
              FULLSCAN
            | SAMPLE INTEGER (PERCENT | ROWS)
            | csStreamList
        )
        (COMMA? NORECOMPUTE)?
    ;

csStreamList
    : s+=csStream (COMMA s+=csStream)*
    ;

csStream
    : STATS_STREAM OPEQ keywId
    ;

csOn
    : ON keywId columnList
    ;
   

// End: createStatistics
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// createSymmetric statements
// TODO: restart here
//
createSymmetric
    : SYMMETRIC KEY keywId
        authorization?
        createSymKeyOptions
        createSymEncryption
    	SEMI?
    ;

createSymKeyOptions
    : WITH keyOptions
    ;

keyOptions
    : k+=keyOption (COMMA k+=keyOption)*
    ;

keyOption
    : KEY_SOURCE OPEQ SQ_LITERAL
    | ALGORITHM OPEQ ID
    | IDENTITY_VALUE OPEQ SQ_LITERAL
    ;

createSymEncryption
	: ENCRYPTION BY encryptingMechanisms
	;

encryptingMechanisms
    : e+=encryptingMechanism (COMMA e+=encryptingMechanism)*
    ;

encryptingMechanism
	: CERTIFICATE keywId
	| PASSWORD OPEQ SQ_LITERAL
	| (ASYMMETRIC | SYMMETRIC) KEY keywId
	;


// End: createSymmetric
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// CREATE SYNONYM
//
createSynonym
    : SYNONYM
        keywId FOR keywId
        SEMI?
    ;
// End: createSynonym
///////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////
// createTable statements
//
createTable
    : TABLE keywId
        LPAREN
            ctColDefList COMMA?
        RPAREN
        ctPartition?
        ctTextimage?
        ctFilestream?
        ctWith?
    	SEMI?
    ;

ctFilestream
    : FILESTREAM_ON
        (
            keywId
            | DEFAULT
        )
    ;

ctWith
    : WITH
        LPAREN tableOptionList RPAREN
    ;

tableOptionList
    : t+=tableOption (COMMA t+=tableOption)*
    ;

tableOption
    :     DATA_COMPRESSION OPEQ (NONE | ROW | PAGE )
          ctOnPartitions?
    ;
    
ctOnPartitions
    : ON PARTITIONS
        LPAREN
            partitionList
        RPAREN
    ;

partitionList
    : p+=partitionListEl (COMMA p+=partitionListEl)*
    ;

partitionListEl
    : expression (TO expression)?
    ;

ctTextimage
    : TEXTIMAGE_ON dqBrLiteral
    ;

ctPartition
    : ON
        (
                  keywId (LPAREN keywId RPAREN)?
        )
    ;

ctColDefList
    : ctColDefListElement (COMMA ctColDefListElement)*
    ;

ctColDefListElement
    : ctColumnDefPlus ctColTableConstraint*
    | ctColTableConstraint
    ;

ctColumnDefPlus
    : ctColumnDefinition colDefOption*
    ;

colDefOption
    : FILESTREAM
    | ctCollate
    | MASKED WITH (FUNCTION OPEQ SQ_LITERAL)
    | IDENTITY ( LPAREN OPMINUS? INTEGER COMMA OPMINUS? INTEGER RPAREN )?
    | notForReplication
    | ROWGUIDCOL
    | SPARSE
    // TODO: GENERATED, ENCRYPTED
    ;


ctColumnDefinition
	: keywId       	// Column name (might be just 'timestamp' or something like that)
        (
              ctDataType
            | AS expression			// Computed
                (PERSISTED )?
            | columnSetDefinition
        )?
	;

columnSetDefinition
    : XML COLUMN_SET FOR ALL_SPARSE_COLUMNS
    ;

ctDataType
    : ctData
    ;

ctData
    : (CURSOR | keywId) ID? VARYING? // (keywId (keywId)?)?	// type name (can be 'national character varying' for instance)
              (
				LPAREN
					( 
						  INTEGER (COMMA INTEGER)?
						| KMAX
						| ((CONTENT | DOCUMENT))? keywId
					)
				RPAREN
			  )?
    ;

ctCollate
    : COLLATE keywId
    ;


ctColTableConstraint
	: optConstraintName?
		(
			  (PRIMARY KEY | UNIQUE)
			  	(CLUSTERED | NONCLUSTERED)?
                (ctTableConCols)?
			  	ctConWith?
			  	ctConOn?
			  
			| optForeignKey
			
				ctTableConCols?
                ctConReferences
				
				ctConOnDelete?
                ctConOnUpdate?
                notForReplication?
			
			| CHECK notForReplication? LPAREN searchCondition RPAREN

            | KNOT? KNULL

            | DEFAULT expression optWithValues? (FOR keywId)?

            | ROWGUIDCOL
		)
	;

optWithValues
    : WITH VALUES
    ;

optConstraintName
    : CONSTRAINT keywId
    ;

optForeignKey
    : FOREIGN KEY
    |
    ;

ctConReferences
    : REFERENCES
				keywId (ctTableConCols)?
    ;
    
ctTableConCols
    : LPAREN
				cn+=ctTableConCol (COMMA cn+=ctTableConCol)*
	  RPAREN
    ;

ctTableConCol
    : columnName (ASC|DESC)?
    ;

ctConOnDelete
    : ON KDELETE ctOnOptions
    ;

ctConOnUpdate
    : ON UPDATE ctOnOptions
    ;

ctConOn
    : ON
        keywId (LPAREN keywId RPAREN)?
    ;

ctConWith
    : WITH
        (
              FILLFACTOR OPEQ INTEGER
            | LPAREN indexOptionList RPAREN
        )
    ;

ctTableConstraintCol
	: keywId (ASC |DESC)?
	;
    			

ctOnOptions
	: NO_ACTION 
	| CASCADE 
	| SET (KNULL | DEFAULT)
	;

// End: createTable
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// createTrigger statements
//
createTrigger
    : TRIGGER
    
    	keywId ON 
    	(
    		  trigIud
    		| trigDdl
    	)

    	SEMI?
    ;

trigDdl
    : trigDdlStuff
    ;

trigDdlStuff
    : (DATABASE | ALL SERVER)
    			(
    				trigWith?

    				(FOR | AFTER)
    						(
    							  LOGON
    							| keywIdList
    						)

    				triggerBody
    			)
    ;

trigIud
    : trigIudStuff
    ;

trigIudStuff
    :  keywId

    		  trigWith?

    		  ( FOR | AFTER | INSTEAD OF)

    		  trigDelInsUpList

              (WITH APPEND)?
    		  notForReplication?

				triggerBody
    ;

trigWith
    : WITH triggerOptionList
    ;

triggerBody
    
	: AS
		(
    		  unblockedStatements
    		| EXTERNAL NAME keywId
    	)
    ;

unblockedStatements
    : beginStatement
    | statements+ (END|EOF)
    ;

trigDelInsUpList
	: t+=trigDelInsUp (COMMA t+=trigDelInsUp)*


	;

trigDelInsUp
	: KDELETE
	| INSERT
	| UPDATE
	;

triggerOptionList
	: t+=triggerOption (COMMA t+=triggerOption)*
	;

triggerOption
	: ENCRYPTION
	| executeAsClause
	;
	
// End: createTrigger
///////////////////////////////////////////////////////////


///////////////////////////////////////////////////////////
// createType statements
//
createType
    : TYPE
        keywId
        (
              crTypeFrom
            | externalName
            | AS TABLE
                LPAREN
                    ctColDefList COMMA?
                RPAREN
        )
        SEMI?
    ;


crTypeFrom
    : FROM
        crTypeDataType
        (KNULL | KNOT KNULL)?
    ;

crTypeDataType
    : crTypeData
    ;

crTypeData
    : keywId 	// type name
			  (
				LPAREN
					(
						    INTEGER (COMMA INTEGER)?
                          | ((CONTENT|DOCUMENT))? keywId
					
					)
				RPAREN
			  )?
    ;

// End of createType
///////////////////////////////////////////////////////////


///////////////////////////////////////////////////////////
// createUser statements
//
createUser
    : USER keywId
        (
              crUserForFrom
            | WITHOUT LOGIN
        )

        crUserSchema?

       SEMI?
    ;

crUserSchema
    : WITH DEFAULT_SCHEMA OPEQ keywId
    ;
    
crUserForFrom
    : (FOR|FROM)
        crUserCredentials
    ;

crUserCredentials
    : LOGIN keywId
    | CERTIFICATE keywId
    | ASYMMETRIC KEY keywId
    ;

// End: createUser
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// createView statements
//
createView
    : VIEW
    		keywId columnList?
    		
    		viewWith?
    		viewAs
    		
    		(WITH CHECK OPTION)?
    	SEMI?
    ;

viewAs
    : AS selectStatement
    ;

viewWith
    : WITH viewAttributeList
    ;

viewAttributeList
	: viewAttribute (COMMA viewAttribute)*
	;
	
viewAttribute
	: ENCRYPTION
	| SCHEMABINDING
	| VIEW_METADATA
	;
	
// End: createView
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// createXml statements
//
createXml
    : XML SCHEMA COLLECTION keywId? AS (SQ_LITERAL |keywId)
    	SEMI?
    ;
// End: createXml
///////////////////////////////////////////////////////////
