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
 * any other category. Not even the others that don't fall into a category.
 */
parser grammar USqlMisc2;

///////////////////////////////////////////////////////////
// DISABLE TRIGGER
//
disableStatement
    : DISABLE TRIGGER

        commonTrigger

        SEMI?
    ;



// End: DISABLE
///////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// ENABLE STATEMENT
//
enableStatement
    : ENABLE TRIGGER

        commonTrigger

        SEMI?
    ;
// End: ENABLE STATEMENT
//////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// END CONVERSATION
//
endConversation
    : END CONVERSATION keywId
       ecWithClause?
      SEMI?
    ;

ecWithClause
    : WITH
        (
              ERROR OPEQ (INTEGER | keywId)
              DESCRIPTION OPEQ (SQ_LITERAL | keywId )
            | CLEANUP
        )
    ;

// End:
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// EXECUTE statement
//
executeStatement
    : execOne 
    ;

execOne
    : EXECUTE
        execBody
    ;

execBody
    : (
              execAs
            | execSp
      )
      SEMI?
    ;
//Execute stored procedure
//
execSp
    : execSpFunc
    | execStringCmd
    ;

execStringCmd
    : LPAREN
        execStringList
        execPassthru?
      RPAREN
      execStringCmdAs?
      (execStringCmdAt)?
    ;

execPassthru
    : e+=execPassthruEl (COMMA e+=execPassthruEl)*
    ;

execPassthruEl
    : COMMA expression OUTPUT?
    ;

execStringList
    : e+=execStringBit (OPPLUS e+=execStringBit)*
    ;

execStringBit
    : keywId | SQ_LITERAL
    ;

execStringCmdAs
    : AS (LOGIN|USER) OPEQ (keywId|SQ_LITERAL)
    ;

execStringCmdAt
    : AT keywId
    ;

execSpFunc
    : keywId (OPEQ keywId)? (SEMI INTEGER)?
      (execSpParamList)?
      (WITH RECOMPILE)?
    ;

execSpParamList
    : e+=execSpParam (COMMA e+=execSpParam)*
    ;

execSpParam
    : (keywId OPEQ)?
        (
              expression ((OUTPUT|KOUT))?
            | DEFAULT
        )
    ;

execAs
    : AS execContext
    ;

execContext
    : (LOGIN | USER) OPEQ (keywId|SQ_LITERAL)
        execWith?
    | CALLER
    ;

execWith
    : WITH

        (
              NO REVERT
            | COOKIE INTO keywId
        )
    ;
// End: EXECUTE statement
///////////////////////////////////////////////////////////


///////////////////////////////////////////////////////////
// WAITFOR {}
//
waitforStatement
    : WAITFOR
        (
              waitStat
            | waitDelay
            | waitTime
        )
        SEMI?
    ;

waitDelay
    : DELAY (keywId|SQ_LITERAL|INTEGER)
    ;

waitTime
    : TIME (keywId|SQ_LITERAL|INTEGER)
    ;

waitStat
    : LPAREN
            waitForSubStat
      RPAREN
        (COMMA TIMEOUT (keywId | INTEGER))?
    ;

waitForSubStat
    : getStatement
    | receiveStatement
    ;
// End: WAITFOR {}
///////////////////////////////////////////////////////////


///////////////////////////////////////////////////////////
// GET CONVERSATION
//
getStatement
    : GET CONVERSATION GROUP keywId FROM keywId

        SEMI?
    ;
// End: GET CONVERSATION
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// GOTO
// As if SQL isn't bad enough on it's own, we need a GOTO
// statement to let people really screw up.
//
gotoStatement
    : GOTO funcKeywId

        SEMI?

    | funcKeywId COLON
    ;
// End: GOTO
///////////////////////////////////////////////////////////


///////////////////////////////////////////////////////////
// IF statement
//
ifStatement
    : IF
        searchCondition
        statements SEMI?
      ifElse?
      SEMI?
    ;

ifElse
    : ELSE statements SEMI?
    ;

// End:
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// INSERT statement
//
insertStatement
    : INSERT
        commonTopClause?
        insertInto
        insertUpdateTarget

        SEMI?
    ;

insertInto
    : isOptInto
        (
              keywId
            | rowsetFunction
        )
        commonWithHints?
    ;

isOptInto
    : INTO
    |
    ;

insertUpdateTarget
    :
        (LPAREN
            keywIdList RPAREN
        )?   // column list
        outputClause?
        insertUpdateTargetTbl

    | DEFAULT VALUES
    ;

insertUpdateTargetTbl
    : insertUpdateTargetValues
    | executeStatement
    | selectStatement
   // | LPAREN selectStatement RPAREN
    ;

insertUpdateTargetValues
    : VALUES valuesListList
    ;

valuesListList
    : LPAREN i+=iutValuesList RPAREN (COMMA LPAREN i+=iutValuesList RPAREN)*
    ;

iutValuesList
    : i+=iutValue (COMMA i+=iutValue)*
    ;

iutValue
    : DEFAULT
    | expression  // Covers KNULL
    ;

// End:
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// MERGE statement
//
mergeStatement
    : MERGE
        commonTopClause?
        mergeInto
        USING tableSource
        mergeOn
        outputClause?
        (optionClause)?
        SEMI?
    ;

mergeOn
    : ON searchCondition
        mergeMatches?
    ;

mergeMatches
    : whenClauses+
    ;

whenClauses
    : WHEN
        (
              MATCHED (KAND searchCondition)? THEN mergeMatched
            | KNOT MATCHED
                (
                    (BY TARGET)? (KAND searchCondition)?
                        THEN mergeNotMatched
                  | BY SOURCE (KAND searchCondition)?
                        THEN mergeMatched
                )
        )
    ;

mergeMatched
    : UPDATE mergeSetClause
    | KDELETE
    ;

mergeSetClause
    : SET
        mergeSetList
    ;

mergeSetList
    : s+=setVars (COMMA s+=setVars)*
    ;
    
mergeNotMatched
    : INSERT
        (LPAREN

            keywIdList RPAREN

        )?
        (
              insertUpdateTargetValues
            | DEFAULT VALUES
        )
    ;

mergeInto
    : isOptInto
        (
              keywId
            | rowsetFunction
        )
        mergeWithHints?
        asClause?
    ;

mergeHintLimitedList
    : t+=mergeHintLimited+
    ;

mergeHintLimited
		: tableHintLimited
        | KINDEX
                    (
                          LPAREN (INTEGER | funcKeywId) (COMMA (INTEGER | funcKeywId))* RPAREN
                        | OPEQ (INTEGER | funcKeywId)
                    )
		;

mergeWithHints
    : WITH LPAREN mergeHintLimitedList RPAREN
    ;

// End:
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// KILL statment
//
killStatement
    : KILL
        (
              killProcess
            | killQuery
            | killStats
        )

        SEMI?
    ;

killQuery
    : KQUERY NOTIFICATION SUBSCRIPTION

        (
              ALL
            | keywId
            | INTEGER
        )
    ;

killStats
    : STATS JOB (keywId|INTEGER)
    ;

killProcess
    : k=killProcessUow
      (WITH STATUSONLY)?
    ;

killProcessUow
    : keywId
    | INTEGER
    ;

// End: KILL statement
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// MOVE statement
//
moveStatement
    : MOVE CONVERSATION
        keywId TO keywId
        SEMI?
    ;

// End: MOVE statement
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// OPEN statement
//
openStatement
    : OPEN
        (
              openKey
            | openCursor
        )
        SEMI?
    ;

openKey
    : (MASTER KEY|SYMMETRIC KEY keywId)
        DECRYPTION BY
        okEncryptingMechanism
    ;

okEncryptingMechanism
	: (ASYMMETRIC KEY | CERTIFICATE) keywId (WITH PASSWORD OPEQ SQ_LITERAL)?
	| PASSWORD OPEQ SQ_LITERAL
    | SYMMETRIC KEY keywId
	;

// End: OPEN
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// PRINT statement
//
printStatement
    : PRINT
        expression
        SEMI?
    ;

// End: PRINT
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// RAISERROR statement
//
raiserrorStatement
    : RAISERROR
        (
                LPAREN
                    expressionList
                RPAREN
                raiseerrorWith?

              // SYBASE backwards compatibility
              //
            | expression (raiseList)?
        )
        SEMI?
    ;

raiseList
    : e+=expression (COMMA e+=expression)*
    ;

raiseerrorWith
    : WITH raiseerrorOptList
    ;

raiseerrorOptList
    : r+=raiseerrorOpt (COMMA r+=raiseerrorOpt)*
    ;

raiseerrorOpt
    : LOG
    | NOWAIT
    | SETERROR
    ;

// End: RAISEERROR
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// READTEXT statement
//
readtextStatement
    : READTEXT
        keywId keywId expression expression
        HOLDLOCK?
        SEMI?
    ;

// End: READTEXT
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// RECEIVE statement
//
receiveStatement
    : RECEIVE
        commonTopClause?
        receiveColList
        receiveFrom
        receiveInto?
        receiveWhere?
    ;

receiveFrom
    : FROM keywId
    ;

receiveWhere
    : WHERE
        keywId OPEQ keywId
    ;

receiveInto
    : INTO keywId
    ;

receiveColList
    : r+=receiveCol (COMMA r+=receiveCol)*
    ;

receiveCol
    : OPMUL
    | funcKeywId OPEQ expression
    | expression
        (AS funcKeywId)?
    ;

// End: RECEIVE
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// RECONFIGURE
//
reconfigureStatement
    : RECONFIGURE WITH OVERRIDE
    ;

// End: RECONFIGURE
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// RESTORE
//
restoreStatement
    : RESTORE
        (
              restoreKey
            | restoreDatabase
            | restoreOther
        )
        SEMI?
    ;

restoreKey
    : (MASTER | SERVICE MASTER) KEY
        rkFrom
        akPasswordOption
        FORCE?
    ;

rkFrom
    :   FROM KFILE OPEQ SQ_LITERAL
    ;

restoreDatabase
    : (LOG|DATABASE)
        keywId
        backupFileOrGroupList?    // Specific file or groups?
        restoreFrom?
        restoreWith?
    ;

restoreWith
    : WITH
        PARTIAL?
        (COMMA? restWithOption)+
    ;

restWithOption
    : restWithOptions
    ;

restWithOptions
    : KFILE OPEQ (INTEGER | keywId)
    | MOVE (COMMA? (keywId|SQ_LITERAL) TO (keywId|SQ_LITERAL))+
    | keywId (OPEQ (keywId|SQ_LITERAL) (AFTER SQ_LITERAL)?)?
    | STATS OPEQ INTEGER
    ;

restoreFrom
    : FROM
              backupDeviceList
    ;

restoreOther
    : (FILELISTONLY | HEADERONLY | LABELONLY | REWINDONLY | VERIFYONLY)
        restoreFrom
        restoreWith?
    ;

// End: RESTORE
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// RETURN statement
//
returnStatement
    : commonReturn
        SEMI?
    ;

// End: RETURN
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
//
//
revertStatement
    : REVERT
        (WITH COOKIE OPEQ keywId)?
        SEMI?
    ;
// End:
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// ROLLBACK statement
//
rollbacksaveStatement
    : (ROLLBACK|SAVE)
        (
              TRANSACTION funcKeywId?
            | WORK
        )?
      SEMI?
    ;
// End: ROLLBACK
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// SEND statement
//
sendStatement
    : SEND
        sendOn
        sendMessageType?
        (LPAREN expression RPAREN)?
      SEMI?
    ;

sendOn
    : ON CONVERSATION keywId
    ;

sendMessageType
    : MESSAGE TYPE keywId
    ;

// End: SEND
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// SET statement
//
setStatement
    : SET (specialFlags (ON | OFF)? | setVars) SEMI?
    ;

setVars
    : setVarList e1=expression? e2=expression?
        (   : assop e3=expression
            | ON
            | OFF
        )?
    ;

assop
    : OPEQ
    | OPPLUSEQ
    | OPMINUSEQ
    | OPMULEQ
    | OPDIVEQ
    | OPMODEQ
    | OPBANDEQ
    | OPBOREQ
    | OPBXOREQ
    ;

setVarList
    : keywId (COMMA keywId)*
    ;

// Parsed by expression
specialFlags
    : DEADLOCK_PRIORITY
        (
              LOW
            | NORMAL
            | HIGH
            | expression
        )
    | STATISTICS (IO|PROFILE|TIME|XML)
    | TRANSACTION ISOLATION LEVEL

        (
              READ (COMMITTED|UNCOMMITTED)
            | REPEATABLE READ
            | SNAPSHOT
            | SERIALIZABLE
        )
    | CURSOR commonCursorDecl
    | DEFAULT
    ;
// End: SET
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
//
//
setUser
    : SETUSER
        (
            (keywId | SQ_LITERAL) (WITH RESET)?
        )?
    ;
// End:
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// SHUTDOWN
//
shutdownStatement
    : SHUTDOWN (WITH NOWAIT)? SEMI?
    ;
// End:
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// TRUNCATE statement
//
truncateStatement
    : TRUNCATE TABLE
        keywId
        SEMI?
    ;
// End:
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// UPDATE
//
updateStatement
    : UPDATE
        (
              updateTable
            | updateStatistics
        )
        SEMI?
    ;

updateTable
    :   commonTopClause?
        insertInto?     // Same as INSERT, auto insert an INTO node though the keyword is not there
        updateSet
        outputClause?
        updateFrom?
        deleteWhereClause?
        optionClause?
    ;

updateSet
    : SET
        updateSetList
    ;

updateSetList
    : u+=updateElement (COMMA u+=updateElement)*
    ;

updateElement
    : keywId
        (
              OPEQ (expression  | DEFAULT) (OPEQ (expression | DEFAULT))?
            | LPAREN expressionList RPAREN
        )
    ;

updateFrom
    : FROM tableSourceList
    ;

updateStatistics
    : STATISTICS
        keywId
        (statsIndexList)?
        updateStatsWith?
    ;

statsIndexList
    : keywId
    | LPAREN keywIdList RPAREN
    ;

updateStatsWith
    : WITH
        (
              FULLSCAN
            | SAMPLE (keywId|INTEGER) (PERCENT | ROWS)?
            | RESAMPLE
            | updateStatsStreams
        )
        (COMMA? (ALL|COLUMNS|KINDEX))?
        (COMMA? NORECOMPUTE)?
    ;

updateStatsStreams
    : s+=ussStream (COMMA s+=ussStream)*
    ;

ussStream
    : STATS_STREAM OPEQ keywId
    | ROWCOUNT OPEQ INTEGER
    | PAGECOUNT OPEQ INTEGER
    ;

// End: UPDATE
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// UPDATETEXT
//
updatetextStatement
    : UPDATETEXT
        keywId keywIdPart
        (KNULL | keywId | INTEGER)
        (KNULL | keywId | INTEGER)
        (WITH LOG)?
        (expression (keywId|INTEGER)?)?
        SEMI?
    ;
// End:
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// WHILE statement
//
whileStatement
    : WHILE
        searchCondition
        statements
    ;

// End: WHILE
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
//
//
writetextStatement
    : WRITETEXT
        keywId
        keywId
        (WITH LOG)?
        expression
        SEMI?
    ;
// End:
///////////////////////////////////////////////////////////
