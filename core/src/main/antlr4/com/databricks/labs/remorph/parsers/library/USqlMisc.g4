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

/**
 * This grammar covers T-SQL statements that don't particularly fall in to
 * any other category.
 */
parser grammar USqlMisc;

///////////////////////////////////////////////////////////
// Miscellaneous statements
//
miscellaneousStatements
    : beginStatement
	| breakStatement
	| checkpointStatement
	| closeStatement
	| commitStatement
	| continueStatement
    | dbccStatement
    | declareStatement
    | deleteStatement
    | disableStatement
    | enableStatement
    | endConversation
    | waitforStatement
    | getStatement
    | gotoStatement
    | ifStatement
    | insertStatement
    | killStatement
    | mergeStatement
    | moveStatement
    | openStatement
    | printStatement
    | raiserrorStatement
    | readtextStatement
    | receiveStatement
    | reconfigureStatement
    | restoreStatement
    | returnStatement
    | revertStatement
    | rollbacksaveStatement
    | sendStatement
    | setStatement
    | setUser
    | shutdownStatement
    | truncateStatement
    | updateStatement
    | updatetextStatement
    | whileStatement
    | writetextStatement
;

// End: Miscellaneous statements
///////////////////////////////////////////////////////////
beginStatement
	: BEGIN SEMI?
		(
			  (
				  CONVERSATION TIMER LPAREN keywId RPAREN TIMEOUT OPEQ INTEGER

				| DIALOG CONVERSATION? ID

					FROM SERVICE keywId
					TO SERVICE SQ_LITERAL (COMMA SQ_LITERAL)?
					(ON CONTRACT keywId)?
					(
						WITH
							(
								(RELATED_CONVERSATION_GROUP | RELATED_CONVERSATION) OPEQ keywId

							)?

                        (COMMA? LIFETIME OPEQ INTEGER)?
                        (COMMA? ENCRYPTION OPEQ (ON|OFF))?
					)?

				| DISTRIBUTED? TRANSACTION
					(keywId)?
						(WITH KMARK SQ_LITERAL?)?	// NOt allowed on DISTRIBUTED

				| TRY statementBlock END TRY

				| CATCH statementBlock END CATCH
			  )

			| statementBlock END
		)
        SEMI?
	;
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// BREAK statement
//
breakStatement
	: BREAK
	;
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// BULK statement
//
bulkStatement
	: BULK INSERT
		keywId?
		FROM SQ_LITERAL
		(
			WITH
				LPAREN

					bulkOptionList

				RPAREN

		)?
	;

bulkOptionList
	: bulkOption (COMMA bulkOption)*
	;

bulkOption
	: CHECK_CONSTRAINTS
	| FIRE_TRIGGERS
	| KEEPIDENTITY
	| KEEPNULLS
	| TABLOCK

	| (
		  BATCHSIZE
		| FIRSTROW
		| KILOBYTES_PER_BATCH
		| LASTROW
		| MAXERRORS
		| ROWS_PER_BATCH
	  )
	  	OPEQ INTEGER

	| (
		  CODEPAGE
		| DATAFILETYPE
		| FIELDTERMINATOR
		| FORMATFILE
		| ROWTERMINATOR
		| ERRORFILE
	  )
	  	OPEQ SQ_LITERAL

	| ORDER
		LPAREN
			( keywId (ASC|DESC)? (COMMA keywId (ASC|DESC)?)* )
		RPAREN
	;
////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////
// CHECKPOINT statement
//
checkpointStatement
	: CHECKPOINT (expression)? SEMI?
	;
////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////
// CLOSE statement
//
closeStatement
	: CLOSE
		(
			  (GLOBAL)? keywIdPart
			| MASTER KEY
			| SYMMETRIC KEY keywId
			| ALL SYMMETRIC KEYS
		)
		SEMI?
	;
////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////
// 	COMMIT statement
//
commitStatement
	: COMMIT
			(
				  TRANSACTION (keywId)?
				| WORK
			)?

		SEMI?
	;
////////////////////////////////////////////////////////////////////////
// 	CONTINUE statement
//
continueStatement
	: CONTINUE SEMI?
	;
////////////////////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// BACKUP statement
//
backupStatement
	: BACKUP
		(
			  (
				  DATABASE keywId

				  	backupFileOrGroupList?    // Specific file or groups?

				| LOG keywId
		   	  )
		  		TO backupDeviceList
				  	mirrorTo

				  	(WITH (DIFFERENTIAL | backupWithOptionsList))?

			| CERTIFICATE keywId TO KFILE OPEQ SQ_LITERAL
				backupCertKey?

			| SERVICE? MASTER KEY TO KFILE OPEQ SQ_LITERAL
				ENCRYPTION BY PASSWORD OPEQ SQ_LITERAL

		)
	  SEMI?
	;

backupCertKey
    : WITH PRIVATE KEY
        LPAREN

            backupCertOpts
        RPAREN
    ;

backupCertOpts
    : bco+=backupCertOpt (COMMA bco+=backupCertOpt)*
    ;

backupCertOpt
    : KFILE OPEQ SQ_LITERAL
    | (DECRYPTION|ENCRYPTION) BY PASSWORD OPEQ SQ_LITERAL
    ;

backupFileOrGroupList
    : fog+=backupFileOrGroup (COMMA fog+=backupFileOrGroup)*
    ;

backupFileOrGroup
    : (KFILE|FILEGROUP|PAGE) OPEQ (keywId |SQ_LITERAL)
    | READ_WRITE_FILEGROUPS
    ;

mirrorTo
	: (MIRROR TO backupDeviceList)*
	;

backupWithOptionsList
	: backupWithOptions (COMMA backupWithOptions)*
	;

backupWithOptions
	: COPY ONLY
	| NO_LOG
	| NOINIT
	| INIT
	| NOSKIP
	| KSKIP
	| NOFORMAT
	| FORMAT
	| NO_CHECKSUM
	| CHECKSUM
	| STOP_ON_ERROR
	| CONTINUE_AFTER_ERROR
	| RESTART
	| KREWIND
	| NOREWIND
	| UNLOAD
	| NOUNLOAD
	| NORECOVERY
	| NO_TRUNCATE
	| TRUNCATE_ONLY

	| (
		  DESCRIPTION
		| PASSWORD
		| NAME
		| EXPIREDATE
		| MEDIADESCRIPTION
		| MEDIAPASSWORD
		| MEDIANAME
	  )
	  	 OPEQ (SQ_LITERAL | keywId)

	| (
		  RETAINDAYS
		| BLOCKSIZE
		| BUFFERCOUNT
		| MAXTRANSFERSIZE
	  )
		OPEQ ( INTEGER | keywId)

	| STATS OPEQ INTEGER
	| STANDBY OPEQ SQ_LITERAL
	;

backupDeviceList
	: backupDevice (COMMA backupDevice)*
	;

backupDevice
	: keywId
	| (DISK | TAPE | DATABASE_SNAPSHOT) OPEQ (SQ_LITERAL | keywId)
	;

///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// DBCC statement
//

dbccStatement
    : DBCC

        (
              dbccDll
            | dbccCheckalloc
            | dbccCheckcatalog
            | dbccCheckconstraints
            | dbccCheckdb
            | dbccCheckfilegroup
            | dbccCheckident
            | dbccChecktable
            | dbccCleantable
            | dbccConcurrency
            | dbccDbreindex
            | dbccDropcleanbuffers
            | dbccFreeproccache
            | dbccFreesessioncache
            | dbccFreesystemcache
            | dbccHelp
            | dbccIndexdefrag
            | dbccInputbuffer
            | dbccOpentran
            | dbccOutputbuffer
            | dbccPintable
            | dbccProccache
            | dbccShowStatistics
            | dbccShowcontig
            | dbccShrinkdatabase
            | dbccShrinkfile
            | dbccSqlperf
            | dbccTraceoff
            | dbccTraceon
            | dbccTracestatus
            | dbccUnpintable
            | dbccUpdateusage
            | dbccUseroptions
        )

        SEMI?
    ;

dbccDll
    : funcKeywId LPAREN FREE RPAREN (dbccWith)?
    ;

dbccCheckalloc
    : CHECKALLOC
        (
            (
                  dbccForm_1
                | dbccWith
            )
        )?
    ;

dbccForm_1
    : LPAREN

            dbccDbname
            (COMMA? (keywId|SQ_LITERAL|INTEGER))?

      RPAREN
      (dbccWith)?
    ;

dbccDbname
    : keywId
    | SQ_LITERAL
    | INTEGER
    ;

// NB: This is all options for all dbcc commands so you have to check they 
//     are valid in the AST walk
//
dbccWith
    : WITH
        (COMMA? dbccWithOption)+
    ;

dbccWithOption
    : keywId
    ;

dbccCheckcatalog
    : CHECKCATALOG
         (
             (
                  dbccForm_2
                | dbccWith
             )
         )?
    ;

dbccForm_2
    :   LPAREN
            dbccDbname
        RPAREN
        (dbccWith)?
    ;

dbccCheckconstraints
    : CHECKCONSTRAINTS
        dbccForm_2
    ;

dbccCheckdb
    : CHECKDB
        (
            (
                  dbccForm_1
                | dbccWith
            )
        )?
    ;

dbccCheckfilegroup
    : CHECKFILEGROUP
        (
            (
                  dbccForm_1
                | dbccWith
            )
        )?
    ;

dbccCheckident
    : CHECKIDENT
        dbccForm_3
    ;

dbccForm_3
    : LPAREN
            dbccDbname
            (COMMA? (keywId|SQ_LITERAL|INTEGER) (COMMA? (keywId|INTEGER|SQ_LITERAL))?)?
      RPAREN
      (dbccWith)?
    ;

dbccChecktable
    : CHECKTABLE
        dbccForm_1
    ;

dbccCleantable
    : CLEANTABLE
        dbccForm_3
    ;

dbccConcurrency
    : CONCURRENCYVIOLATION
    ;

dbccDbreindex
    : DBREINDEX
        dbccForm_3
    ;

dbccDropcleanbuffers
    : DROPCLEANBUFFERS
        (dbccWith)?
    ;

dbccFreeproccache
    : FREEPROCCACHE
        (dbccWith)?
    ;

dbccFreesessioncache
    : FREESESSIONCACHE
        (dbccWith)?
    ;

dbccFreesystemcache
    : FREESYSTEMCACHE
        LPAREN (ALL|SQ_LITERAL) RPAREN
        (dbccWith)?
    ;

dbccHelp
    : HELP
        dbccForm_2
    ;

dbccIndexdefrag
    : INDEXDEFRAG
        dbccForm_4
    ;

dbccForm_4
    : LPAREN
            dbccDbname
            (COMMA? (keywId|SQ_LITERAL) (COMMA (keywId|SQ_LITERAL) (COMMA? (keywId|INTEGER|SQ_LITERAL))?)? )?
      RPAREN
      (dbccWith)?
    ;

dbccInputbuffer
    : INPUTBUFFER
        dbccForm_1
    ;

dbccOpentran
    : OPENTRAN
         (
             (
                  dbccForm_2
                | dbccWith
             )
         )?
    ;

dbccOutputbuffer
    : OUTPUTBUFFER
        dbccForm_1
    ;

dbccPintable
    : PINTABLE dbccForm_1
    ;

dbccProccache
    : PROCCACHE
        (dbccWith)?
    ;

dbccShowStatistics
    : SHOW_STATISTICS
        dbccForm_1
    ;

dbccShowcontig
    : SHOWCONTIG
        (
            (
                  dbccForm_1
                | dbccWith
            )
        )?
    ;

dbccShrinkdatabase
    : SHRINKDATABASE
        (
            (
                  dbccForm_3
                | dbccWith
            )
        )?
    ;

dbccShrinkfile
    : SHRINKFILE
        dbccForm_3
    ;

dbccSqlperf
    : SQLPERF
        dbccForm_1
    ;

dbccTraceoff
    : TRACEOFF
        LPAREN
            (COMMA? OPMINUS? INTEGER)+
        RPAREN
        (dbccWith)?
    ;

dbccTraceon
    : TRACEON
        LPAREN
            (COMMA? OPMINUS? INTEGER)+
        RPAREN
        (dbccWith)?
    ;

dbccTracestatus
    : TRACESTATUS
        LPAREN
            (COMMA? OPMINUS? INTEGER)*
        RPAREN
        (dbccWith)?
    ;

dbccUnpintable
    : UNPINTABLE dbccForm_1
    ;

dbccUpdateusage
    : UPDATEUSAGE
        dbccForm_3
    ;

dbccUseroptions
    : USEROPTIONS
        (dbccWith)?
    ;

// End: DBCC
///////////////////////////////////////////////////////////


///////////////////////////////////////////////////////////
// DECLARE statement for local variables
//
declareStatement
    : DECLARE
        (
               declareCursor        // See tsqlcursors
            | declareList                                  // Local variables
        )
      SEMI?
    ;

declareList
    : declareListItem (COMMA declareListItem)*
    ;

declareListItem
    : keywId declareAs
    ;

declareAs
    : optAs
        declareAsOpts
    ;

declareAsOpts
    : crTypeDataType (OPEQ expression)?
    | TABLE LPAREN declareDefs RPAREN
    ;

declareDefs
    : d+=declareDef (COMMA d+=declareDef)*
    ;

declareDef
    : declareCol
    | declareTableConstraint
    ;

declareCol
    : keywId
        (
              crTypeDataType
            | AS expression
        )
      declareColStuff*
    ;

declareColStuff
    : ctCollate
    | declareColIdentity
    | ROWGUIDCOL
    | declareColConstraint
    ;

declareColConstraint
    : declareColConstraintEl
    ;

declareColConstraintEl
    : (KNULL | KNOT KNULL)
	| (PRIMARY KEY | UNIQUE)
    | (CLUSTERED | NONCLUSTERED)
	| CHECK LPAREN searchCondition RPAREN
	;

declareColIdentity
    : DEFAULT expression
    | IDENTITY ( LPAREN OPMINUS? INTEGER COMMA OPMINUS? INTEGER RPAREN )?
    ;

declareTableConstraint
    : (PRIMARY KEY | UNIQUE) LPAREN keywIdList RPAREN
    | CHECK LPAREN searchCondition RPAREN
    ;

// End: DECLARE
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// Delete statement (can also be called using WITH commonTable)
//
deleteStatement
    : KDELETE
        commonTopClause?
        (deleteFromClause)?
        outputClause?
        fromClause?
        deleteWhereClause?
        optionClause?
      SEMI?
    ;

deleteWhereClause
    : WHERE
        (
              searchCondition
            | deleteCurrent
        )
    ;

deleteCurrent
    : CURRENT OF (GLOBAL)? keywId
    ;

deleteFromClause
    : optFrom
        tableSourcePrimitive     
    ;
    
optFrom
    : FROM
    |
    ;

// End: DELETE statement
///////////////////////////////////////////////////////////
