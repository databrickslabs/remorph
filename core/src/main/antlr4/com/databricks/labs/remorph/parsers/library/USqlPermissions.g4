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
 * This parser covers the syntax for DDL statements that affect permissions, such as GRANT and REVOKE
 */

parser grammar USqlPermissions;

///////////////////////////////////////////////////////////
// DDL statements that affect permissions
//
permissionsDdl
    : grantStatement
    | revokeStatement
    | denyStatement
    ;
// End: permissionsDdl
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// GRANT permissions
//
grantStatement
    : GRANT
        (
              ALL PRIVILEDGES?
            | permissionSet
              permissionOn?
              permissionTo
              (WITH GRANT OPTION)?
              (AS keywId)?
        )
        SEMI?
    ;
// End: GRANT
///////////////////////////////////////////////////////////


///////////////////////////////////////////////////////////
// REVOKE permissions
//
revokeStatement
    : REVOKE

        (GRANT OPTION FOR)?
        permissionBody
        
        SEMI?
    ;

// End:
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// DENY permissions
//
denyStatement
    : DENY

        permissionBody
        SEMI?
    ;

// End: DENY
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// Common permission syntax
//

permissionBody
    : ALL PRIVILEDGES?
    | permissionSet
      permissionOn?
      permissionTo
      CASCADE?
      (AS keywId)?
    ;

permissionOn
    : ON
        permissionObject (COLON COLON keywId)?
    ;

permissionObject
    : (ASYMMETRIC|SYMMETRIC) KEY
    | USER
    | APPLICATION? ROLE
    | FULLTEXT CATALOG
    | OBJECT COLON COLON keywId (LPAREN keywIdList RPAREN)
    | SCHEMA
    | MESSAGE TYPE
    | REMOTE SERVICE BINDING
    | SYS DOT keywId
    | XML SCHEMA COLLECTION
    | keywId
    ;

permissionTo
    : (TO|FROM) keywIdList
    ;

permissionSet
    : psl+=permissionSetElement (COMMA psl+=permissionSetElement)*
    ;

permissionSetElement
    : permissionName (LPAREN keywIdList RPAREN)?
    ;

permissionName
    : permissionSpec
    ;

permissionSpec
    : ADMINISTER BULK OPERATIONS
    | ALTER (
                ANY (
                          APPLICATION ROLE 
                        | ASSEMBLY
                        | (ASYMMETRIC|SYMMETRIC) KEY
                        | CERTIFICATE
                        | CONNECTION
                        | CONTRACT
                        | CREDENTIAL
                        | DATABASE (DDL TRIGGER | EVENT NOTIFICATION)?
                        | DATASPACE
                        | ENDPOINT
                        | EVENT NOTIFICATION
                        | FULLTEXT CATALOG
                        | LINKED SERVER
                        | LOGIN
                        | MESSAGE TYPE
                        | REMOTE SERVICE BINDING
                        | ROLE
                        | ROUTE
                        | SCHEMA
                        | SERVICE
                        | USER

                    )
                | RESOURCES
                | SERVER STATE
                | SETTINGS
                | TRACE
            )?
    | AUTHENTICATE SERVER?
    | BACKUP (DATABASE | LOG)
    | CHECKPOINT
    | CONNECT (REPLICATION |SERVER | SQL)?
    | CONTROL SERVER?
    | CREATE
            (
                 (
                     ANY
                     (
                         DATABASE
                     )
                 )
                |  AGGREGATE
                | ASSEMBLY
                | (ASYMMETRIC|SYMMETRIC) KEY
                | CERTIFICATE
                | CONTRACT
                | DATABASE (DDL EVENT NOTIFICATION)?
                | DDL EVENT NOTIFICATION
                | DEFAULT
                | ENDPOINT
                | FULLTEXT CATALOG
                | FUNCTION
                | MESSAGE TYPE
                | PROCEDURE
                | QUEUE
                | REMOTE SERVICE BINDING
                | ROLE
                | ROUTE
                | RULE
                | SCHEMA
                | SERVICE
                | SYNONYM
                | TABLE
                | TRACE EVENT NOTIFICATION
                | VIEW
                | XML SCHEMA COLLECTION
            )
    | KDELETE
    | EXECUTE
    | EXTERNAL ACCESS ASSEMBLY
    | IMPERSONATE
    | INSERT
    | RECEIVE
    | REFERENCES
    | SELECT
    | SEND
    | SHOWPLAN
    | SHUTDOWN
    | SUBSCRIBE KQUERY NOTIFICATIONS
    | TAKE OWNERSHIP
    | UNSAFE ASSEMBLY
    | UPDATE
    | VIEW  (
                  ANY
                  (
                        DATABASE
                      | DEFINITION
                  )
                | DATABASE STATE
                | DEFINITION
                | SERVER STATE
            )
    ;

// End:
///////////////////////////////////////////////////////////
