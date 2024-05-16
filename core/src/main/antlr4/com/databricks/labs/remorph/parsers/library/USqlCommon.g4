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
 * This parser covers all grammar fragments that are common among two or more rules
 * and can be reused in the interests of efficiency. Constructs like AUTHORIZATION
 * and EXTERNAL are specified here and referred to in the main grammar and the
 * import grammars.
 */
parser grammar USqlCommon;


// General common constructs
//
externalName
    : EXTERNAL NAME keywId
    ;

commonReturns
    : RETURNS expression
    ;

commonReturn
    : RETURN expression?
    ;

commonDataTypeName
    : keywId
    | CURSOR
    ;

authorization
	: AUTHORIZATION keywId
	;

optInto
    : INTO
    |
    ;

tableHintLimitedList
    : t+=tableHintLimited+
    ;

tableHintLimited
		: KEEPIDENTITY      | KEEPDEFAULTS      | FASTFIRSTROW
        | HOLDLOCK          | IGNORE_CONSTANTS  | IGNORE_TRIGGERS
        | NOWAIT            | PAGLOCK           | READCOMMITTED
        | READCOMMITTEDLOCK | READPAST          | REPEATABLEREAD
        | ROWLOCK           | SERIALIZABLE      | TABLOCK
        | TABLOCKX          | UPDLOCK            | XLOCK
		;

commonTopClause
    :  TOP LPAREN expression RPAREN PERCENT?
    ;

commonWithHints
    : WITH LPAREN tableHintLimitedList RPAREN
    ;
    
outputClause
    : outputDml
        (
              INTO keywId (LPAREN keywIdList RPAREN)?

              outputDml?
        )?
    ;

outputDml
    : OUTPUT dmlSelectList
    ;

dmlSelectList
    : d+=dmlSelect (COMMA d+=dmlSelect)*
    ;

dmlSelect
    : delColName (optAs keywId)?
    ;

delColName
    : expression (DOT OPMUL)?
    | ACTION
    ;

// Assembly common
//
commonSetItemList
	: si+=commonSetItem (COMMA si+=commonSetItem)*
	;

commonSetItem
	: NAME OPEQ keywId
	| PASSWORD OPEQ SQ_LITERAL
	| DEFAULT_SCHEMA OPEQ keywId
	;

assemblyFrom
	: FROM expression
	;

assemblyWith
	: WITH assemblyOptionList
	;

assemblyOptionList
	: assemblyOption (COMMA assemblyOption)*
	;

assemblyOption
	: PERMISSION_SET OPEQ ( SAFE | EXTERNAL_ACCESS | UNSAFE)
	| VISIBILITY OPEQ (ON | OFF)
	| UNCHECKED DATA
	;

assemblyName
	: keywId
	;

// Assymetric key common
//
akPasswordOption
	: ENCRYPTION BY PASSWORD OPEQ SQ_LITERAL
			( COMMA? DECRYPTION BY PASSWORD OPEQ SQ_LITERAL )?
	| DECRYPTION BY PASSWORD OPEQ SQ_LITERAL ( COMMA? ENCRYPTION BY PASSWORD OPEQ SQ_LITERAL )?
	;

// Certificate common
//
privateKeyList
	: privateKeySpec (COMMA privateKeySpec)*
	;

privateKeySpec
	: KFILE OPEQ SQ_LITERAL
	| DECRYPTION BY PASSWORD OPEQ SQ_LITERAL
	| ENCRYPTION BY PASSWORD OPEQ SQ_LITERAL
	;

// Database common
//
dbFilespecList
	: af+=dbFilespec (COMMA af+=dbFilespec)*
	;

dbFilespec
	: LPAREN
		adfsName?
        adfsNewname?
        adfsFilename?
        adfsSize?
        adfsMax?
        adfsFilegrowth?
        (COMMA OFFLINE)?
	  RPAREN
	;

// Common trigger syntax
//
commonTrigger
    :   (keywIdList | ALL)
        commonTriggerOn
    ;

commonTriggerOn
    : ON
        (

              DATABASE
            | ALL SERVER
            | keywId
        )
    ;
