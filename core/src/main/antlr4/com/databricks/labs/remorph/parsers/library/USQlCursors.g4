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
 * This grammar contains all statements that deal with cursors other than
 * CREATE cursor
 */
parser grammar USqlCursors;

///////////////////////////////////////////////////////////
// DDL statements that control cursors
//
 cursorDdl
    : deallocate
    ;
// End: Cursor DDL
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
//
//
cursorStatements
    : fetchStatement
    ;

// End:
///////////////////////////////////////////////////////////


///////////////////////////////////////////////////////////
// Cursor deallocate statement
//
deallocate
    : DEALLOCATE
        (GLOBAL)? keywId
        SEMI?
    ;

// End: Cursor deallocate
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// cursor declaration (triggered from DECLARE parsing in tsqlmisc)
//
declareCursorPred
    : keywId INSENSITIVE? SCROLL? CURSOR
    ;

declareCursor
    : keywId i=INSENSITIVE? s=SCROLL? CURSOR ( i=INSENSITIVE)? ( s=SCROLL)?
        commonCursorDecl?
    ;

commonCursorDecl
    :   (LOCAL|GLOBAL)?
        dcExtendedOptions
        dcForStatement
        dcForOptions?
    ;

dcForOptions
    : FOR dcForOption
    ;

dcForOption
    : READ ONLY
    | UPDATE (OF keywIdList)?
    ;

dcExtendedOptions
    : (FORWARD_ONLY | SCROLL)?
      ( STATIC | KEYSET | DYNAMIC | FAST_FORWARD)?
      ( READ_ONLY | SCROLL_LOCKS | OPTIMISTIC)?
      TYPE_WARNING?
    ;

dcForStatement
    : FOR selectStatement
    ;
    
// End:
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// FETCH statement
//
fetchStatement
    : FETCH
        fetchOpts?
        FROM?
        fetchGlobal
        fetchInto?
        SEMI?
    ;

fetchOptsPred
    : NEXT
    | PRIOR
    | FIRST
    | LAST
    | ABSOLUTE
    | RELATIVE
    ;

fetchOpts
    : NEXT
    | PRIOR
    | FIRST
    | LAST
    | (ABSOLUTE|RELATIVE) (OPMINUS? INTEGER | keywId)
    ;

fetchGlobal
    : (GLOBAL)? keywId
    ;

fetchInto
    : INTO keywIdList
    ;

// End: FETCH statement
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
// OPEN cursor
//
openCursor
    : (GLOBAL)? keywId
    ;

// End:
///////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////
//
//

// End:
///////////////////////////////////////////////////////////
