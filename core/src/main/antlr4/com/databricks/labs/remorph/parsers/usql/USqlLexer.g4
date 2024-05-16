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

lexer grammar USqlLexer;

options {
    caseInsensitive = true;
}

// T-SQL Lexer
//

fragment	WSfrag		: ' ' | '\t' 	;
fragment	NLfrag		: ('\r' '\n'? | '\n')	;
fragment	DIGIT		: '0'..'9'		;
fragment	DIGITS		: DIGIT+		;
// TODO: Expand to unincode characters in v4
fragment	ALPHA		: 'A'..'Z'  	;
fragment	ALPHAS		: ALPHA+		;
fragment	ALNUM		: ALPHA | DIGIT	;
fragment	ALNUMS		: ALNUM+		;
fragment	HEXDIGIT	: DIGIT | 'A'..'F' ;

///////////////////////////////////////////////////////////////////////
// Single quoted string is usually for literal values
//
SQ_LITERAL : 'N'? '\'' ( '\'' '\'' | ~'\'' )* '\'' ;

///////////////////////////////////////////////////////////////////////
// Double quoted string is usually for identifiers that don't follow
// normal rules of the ID token, such as "Name With Spaces", but can also be
// string literals if the QUOTED_IDENTIFIER option is set to OFF
//
DQ_LITERAL : 'N'? '"' ( '""' | ~'"' )* '"' ;

///////////////////////////////////////////////////////////////////////
// [] Literal is also used like the "" literal to enclose things like coloumn names and table names
// that woudl otherwise be illegal.
//
BR_LITERAL : 'N'? '[' (~']')* ']' ;

///////////////////////////////////////////////////////////////////////
// This eats the whitespace between keywords and identifiers
// which is of no syntactical significance.
//
WS	: WSfrag+ -> channel(HIDDEN) ;

///////////////////////////////////////////////////////////////////////
// This eats newline characters, which have no syntactical
// significance, though in certain places, such as the single line
// comment rule, they can have lexical significance.
//
NL	: NLfrag+	-> channel(HIDDEN) ;

///////////////////////////////////////////////////////////////////////
// A single line comment, which is introduced by -- and ends at the
// next line break.
//
COMMENT	:	'--' (~('\r' | '\n'))* NLfrag	-> channel(HIDDEN)	;

// A multiline comment is akin to a C style comment and is bounded
// by /* and */. However the T-SQL lexer allows for, and checks
// embedded comments. See how here we use a fragment rule to define
// the lexical construct, as this does not try to create tokens and
// hence can be called recursively by itself. The actual token making
// rule here then, just calls that fragment rule.
//
ML_COMMENT
	:	ML_COMFRAG -> channel(HIDDEN)	;

///////////////////////////////////////////////////////////////////////
// This rule is a fragment so that it can call itself recursively
// and deal with multiple embedded comments.
//
fragment	ML_COMFRAG
		:
			'/*'
                // The predicate looks for the start of an embedded comment
                // and this triggers a recursive call of this rule
                // and therefore automatically matches /* and */ pairs.
                //
                ( ML_COMFRAG | .)*?  // Nongreedy
			'*/'
		;

// A hexadecimal binary constant can be just 0x, which is an empty binary
// string, though the manuals do not specifically state what this means.
//
HEXNUM		:	'0X' HEXDIGIT*						;

// A decimal number fragment, which is part of a scientific notation FLOAT
// number, or, on its own is a decimal number.
//
fragment
DECIMAL_BIT	: DIGITS ('.' DIGITS)
			| '.' DIGITS
			;

// The exponent part of a number in scientific notation
//
fragment
EXPONENT	:	'E' ('+'|'-')? DIGITS	;

FLOAT       :   (DECIMAL_BIT|INTEGER) EXPONENT  ;
DECIMAL		: 	DECIMAL_BIT                     ;
INTEGER		:	DIGITS                          ;

///////////////////////////////////////////////////////////////////////
// Keywords. Many keywords can also be identifiers, so the
// parser must deal with this when it is looking for an
// identifier. The original parser was probably a hand crafted
// design with syntax directed lexing. Such things tend to lead
// to languages with horrible ambiguities, but we can deal with it
// with a little thought.
//
ACCESS                          :	'ACCESS'						;
ACTION                          :   '$ACTION'                       ;
ABSENT							:	'ABSENT'						;
ABSOLUTE                        :   'ABSOLUTE'                      ;
ACCENT_SENSITIVITY				:	'ACCENT_SENSITIVITY'			;
ACTIVATION						:	'ACTIVATION'					;
ACTIVE							:	'ACTIVE'						;
ADMINISTER                      :   'ADMINISTER'                    ;
KADD							:	'ADD'							;
ADDRESS							:	'ADDRESS'						;
AFTER							:	'AFTER'							;
AGGREGATE                       :   'AGGREGATE'                     ;
ALGORITHM						:	'ALGORITHM'						;
ALL								:	'ALL'							;
ALLOW_PAGE_LOCKS				:	'ALLOW_PAGE_LOCKS'				;
ALLOW_ROW_LOCKS					:	'ALLOW_ROW_LOCKS'				;
ALLOW_SNAPSHOT_ISOLATION		:	'ALLOW_SNAPSHOT_ISOLATION'		;
ALL_SPARSE_COLUMNS				:	'ALL_SPARSE_COLUMNS'			;
ALL_RESULTS						:	'ALL_RESULTS'					;
ALTER							:	'ALTER'							;
ANONYMOUS						:	'ANONYMOUS'						;
ANSI_NULL_DEFAULT 				:	'ANSI_NULL_DEFAULT '			;
ANSI_NULLS						:	'ANSI_NULLS'					;
ANSI_PADDING					:	'ANSI_PADDING'					;
ANSI_WARNINGS					:	'ANSI_WARNINGS'					;
ANY								:	'ANY'							;
APPEND                          :	'APPEND'						;
APPLICATION						:	'APPLICATION'					;
APPLY							:	'APPLY'							;
ARITHABORT						:	'ARITHABORT'					;
AS								:	'AS'							;
ASC								:	'ASC'							;
ASSEMBLY						:	'ASSEMBLY'						;
ASYMMETRIC						:	'ASYMMETRIC'					;
AT                              :   'AT'                            ;
ATTACH                          :   'ATTACH'                        ;
ATTACH_REBUILD_LOG              :   'ATTACH_REBUILD_LOG'            ;
AUTHENTICATE					:	'AUTHENTICATE'					;
AUTHENTICATION					:	'AUTHENTICATION'				;
AUTHORIZATION					:	'AUTHORIZATION'					;
AUTH_REALM						:	'AUTH_REALM'					;
AUTO							:	'AUTO'							;
AUTO_CLOSE 						:	'AUTO_CLOSE'					;
AUTO_CREATE_STATISTICS 			:	'AUTO_CREATE_STATISTICS'		;
AUTO_SHRINK                     :   'AUTO_SHRINK'                   ;
AUTO_UPDATE_STATISTICS_ASYNC	:	'AUTO_UPDATE_STATISTICS_ASYNC'	;
AUTO_UPDATE_STATISTICS			:	'AUTO_UPDATE_STATISTICS'		;
AVG								:	'AVG'							;
BACKUP							:	'BACKUP'						;
BASE64							:	'BASE64'						;
BASIC							:	'BASIC'							;
BATCHES							:	'BATCHES'						;
BATCHSIZE						:	'BATCHSIZE'						;
BEGIN							:	'BEGIN'							;
BEGIN_DIALOG					:	'BEGIN_DIALOG'					;
BETWEEN							:	'BETWEEN'						;
BINARY							:	'BINARY'						;
BINDING							:	'BINDING'						;
BLOCKSIZE						:	'BLOCKSIZE'						;
BREAK							:	'BREAK'							;
BROKER_INSTANCE					:	'BROKER_INSTANCE'				;
BROWSE							:	'BROWSE'						;
BUFFERCOUNT						:	'BUFFERCOUNT'					;
BULK							:	'BULK'							;
BULK_LOGGED						:	'BULK_LOGGED'			    	;
BY								:	'BY'							;
CALLED							:	'CALLED'						;
CALLER                          :   'CALLER'                        ;
CASCADE							:	'CASCADE'						;
CASE							:	'CASE'							;
CAST							:	'CAST'							;
CATALOG							:	'CATALOG'						;
CATCH							:	'CATCH'							;
CERTIFICATE						:	'CERTIFICATE'					;
CHANGE_TRACKING					:	'CHANGE_TRACKING'				;
CHARACTER_SET					:	'CHARACTER_SET'					;
CHECK							:	'CHECK'							;
CHECK_CONSTRAINTS				:	'CHECK_CONSTRAINTS'				;
CHECK_EXPIRATION				:	'CHECK_EXPIRATION'				;
CHECKPOINT						:	'CHECKPOINT'					;
CHECK_POLICY					:	'CHECK_POLICY'					;
CHECKSUM_AGG					:	'CHECKSUM_AGG'					;
CHECKSUM						:	'CHECKSUM'						;
CLEANUP                         :   'CLEANUP'                       ;
CLEAR							:	'CLEAR'							;
CLEAR_PORT						:	'CLEAR_PORT'					;
CLOSE							:	'CLOSE'							;
CLUSTERED						:	'CLUSTERED'						;
CODEPAGE						:	'CODEPAGE'						;
COLLATE							:	'COLLATE'						;
COLLECTION						:	'COLLECTION'					;
COLUMN							:	'COLUMN'						;
COLUMN_SET						:	'COLUMN_SET'					;
COLUMNS                         :   'COLUMNS'                       ;
COMMIT							:	'COMMIT'						;
COMMITTED						:	'COMMITTED'						;
COMPATIBILITY_LEVEL             :   'COMPATIBILITY_LEVEL'           ;
COMPRESSION						:	'COMPRESSION'					;
COMPUTE							:	'COMPUTE'						;
CONCAT							:	'CONCAT'						;
CONCAT_NULL_YIELDS_NULL     	:	'CONCAT_NULL_YIELDS_NULL'		;
CONNECT                         :   'CONNECT'                       ;
CONNECTION                      :	'CONNECTION'					;
CONSTRAINT						:	'CONSTRAINT'					;
CONTAINS						:	'CONTAINS'						;
CONTAINSTABLE					:	'CONTAINSTABLE'					;
CONTENT							:	'CONTENT'						;
CONTINUE_AFTER_ERROR			:	'CONTINUE_AFTER_ERROR'			;
CONTINUE						:	'CONTINUE'						;
CONTRACT						:	'CONTRACT'						;
CONVERSATION					:	'CONVERSATION'					;
CONVERT							:	'CONVERT'						;
COOKIE                          :   'COOKIE'                        ;
COPY							:	'COPY'							;
COUNT_BIG						:	'COUNT_BIG'						;
COUNT							:	'COUNT'							;
COUNTER							:	'COUNTER'						;
CONTROL                         :   'CONTROL'                       ;
CREATE                          :   'CREATE'                        ;
CREDENTIAL						:	'CREDENTIAL'					;
CROSS							:	'CROSS'							;
CUBE							:	'CUBE'							;
CURSOR                          :   'CURSOR'                        ;
CURSOR_CLOSE_ON_COMMIT			:	'CURSOR_CLOSE_ON_COMMIT'	    ;
CURSOR_DEFAULT			    	:	'CURSOR_DEFAULT'			    ;
DATABASE						:	'DATABASE'						;
DATABASE_MIRRORING				:	'DATABASE_MIRRORING'			;
DATABASE_SNAPSHOT               :   'DATABASE_SNAPSHOT'             ;
DATA							:	'DATA'							;
DATAFILETYPE					:	'DATAFILETYPE'					;
DATA_COMPRESSION                :   'DATA_COMPRESSION'              ;
DATASPACE                       :	'DATASPACE'						;
DATE_CORRELATION_OPTIMIZATION	:	'DATE_CORRELATION_OPTIMIZATION'	;
DB_CHAINING						:	'DB_CHAINING'			    	;
DBCC                            :   'DBCC'                          ;
DDL                             :	'DDL'							;
DEALLOCATE                      :   'DEALLOCATE'                    ;
DEADLOCK_PRIORITY               :   'DEADLOCK_PRIORITY'             ;
DECLARE                         :   'DECLARE'                       ;
DECRYPTION						:	'DECRYPTION'					;
DEFAULT_DATABASE				:	'DEFAULT_DATABASE'				;
DEFAULT			    			:	'DEFAULT'			    		;
DEFAULT_LANGUAGE				:	'DEFAULT_LANGUAGE'				;
DEFAULT_LOGON_DOMAIN			:	'DEFAULT_LOGON_DOMAIN'			;
DEFAULT_SCHEMA					:	'DEFAULT_SCHEMA'				;
DEFINITION                      :   'DEFINITION'                    ;
DELAY                           :   'DELAY'                         ;
DENY                            :   'DENY'                          ;
DENSE_RANK						:	'DENSE_RANK'					;
DEPENDENTS                      :	'DEPENDENTS'					;
DESC							:	'DESC'							;
DESCRIPTION						:	'DESCRIPTION'					;
DIALOG							:	'DIALOG'						;
DIFFERENTIAL					:	'DIFFERENTIAL'					;
DIGEST							:	'DIGEST'						;
DISABLE_BROKER			    	:	'DISABLE_BROKER'				;
DISABLED						:	'DISABLED'						;
DISABLE							:	'DISABLE'						;
DISK							:	'DISK'							;
DISTINCT						:	'DISTINCT'						;
DISTRIBUTED						:	'DISTRIBUTED'					;
DOCUMENT						:	'DOCUMENT'						;
DROP							:	'DROP'							;
DROP_EXISTING					:	'DROP_EXISTING'					;
DYNAMIC                         :   'DYNAMIC'                       ;
ELEMENTS						:	'ELEMENTS'						;
ELSE							:	'ELSE'							;
EMERGENCY						:	'EMERGENCY'						;
EMPTY							:	'EMPTY'							;
ENABLE_BROKER			    	:	'ENABLE_BROKER'					;
ENABLED							:	'ENABLED'						;
ENABLE							:	'ENABLE'						;
ENCRYPTION						:	'ENCRYPTION'					;
END								:	'END'							;
ENDPOINT						:	'ENDPOINT'						;
ERROR_BROKER_CONVERSATIONS		:	'ERROR_BROKER_CONVERSATIONS'	;
ERROR                           :   'ERROR'                         ;
ERRORFILE						:	'ERRORFILE'						;
ESCAPE							:	'ESCAPE'						;
EXCEPT							:	'EXCEPT'						;
EVENT                           :   'EVENT'                         ;
EVENTDATA						:	'EVENTDATA'						;
EXECUTE							:	'EXEC' 'UTE'?					;
EXECUTABLE						:	'EXECUTABLE'					;
EXISTS							:	'EXISTS'						;
EXPAND							:	'EXPAND'						;
EXPIREDATE						:	'EXPIREDATE'					;
EXPIRY_DATE						:	'EXPIRY_DATE'					;
EXPLICIT						:	'EXPLICIT'						;
EXTERNAL_ACCESS					:	'EXTERNAL_ACCESS'				;
EXTERNAL						:	'EXTERNAL'						;
FAILOVER			    		:	'FAILOVER'			    		;
FAN_IN                          :   'FAN_IN'                        ;
FAST							:	'FAST'							;
FASTFIRSTROW					:	'FASTFIRSTROW'					;
FAST_FORWARD                     :  'FAST_FORWARD'                  ;
FETCH                           :   'FETCH'                         ;
FIELDTERMINATOR					:	'FIELDTERMINATOR'				;
KFILE							:	'FILE'							;
FILEGROUP						:	'FILEGROUP'						;
FILEGROWTH						:	'FILEGROWTH'			    	;
FILENAME			    		:	'FILENAME'						;
FILESTREAM                      :   'FILESTREAM'                    ;
FILESTREAM_ON                   :	'FILESTREAM_ON'					;
FILLFACTOR						:	'FILLFACTOR'					;
FIRE_TRIGGERS					:	'FIRE_TRIGGERS'					;
FIRST                           :   'FIRST'                         ;
FIRSTROW						:	'FIRSTROW'						;
FORCED			    			:	'FORCED'			    		;
FORCE							:	'FORCE'							;
FORCE_SERVICE_ALLOW_DATA_LOSS	:	'FORCE_SERVICE_ALLOW_DATA_LOSS'	;
FOREIGN							:	'FOREIGN'						;
FOR								:	'FOR'							;
FORMATFILE						:	'FORMATFILE'					;
FORMAT							:	'FORMAT'						;
FORWARD_ONLY                    :   'FORWARD_ONLY'                  ;
FREE                            :   'FREE'                          ;
FREETEXT						:	'FREETEXT'						;
FREETEXTTABLE					:	'FREETEXTTABLE'					;
FROM							:	'FROM'							;
FULL			    			:	'FULL'							;
FULLSCAN                        :   'FULLSCAN'                      ;
FULLTEXT						:	'FULLTEXT'						;
FUNCTION						:	'FUNCTION'						;
GB								:	'GB'							;
GET                             :   'GET'                           ;
GLOBAL			    			:   'GLOBAL'						;
GO								:	'GO'							;
GOTO                            :   'GOTO'                          ;
GRANT                           :   'GRANT'                         ;
GROUP							:	'GROUP'							;
GROUPING						:	'GROUPING'						;
HASHED							:	'HASHED'						;
HASH							:	'HASH'							;
HAVING							:	'HAVING'						;
HEADER_LIMIT					:	'HEADER_LIMIT'					;
HIGH                            :   'HIGH'                          ;
HOLDLOCK						:	'HOLDLOCK'						;
HTTP							:	'HTTP'							;
IDENTITY						:	'IDENTITY'						;
IDENTITY_INSERT                 :   'IDENTITY_INSERT'               ;
IDENTITY_VALUE					:	'IDENTITY_VALUE'				;
IF                              :   'IF'                            ;
IGNORE_CONSTANTS                :	'IGNORE_CONSTANTS'				;
IGNORE_CONSTRAINTS				:	'IGNORE_CONSTRAINTS'			;
IGNORE_DUP_KEY					:	'IGNORE_DUP_KEY'				;
IGNORE_TRIGGERS					:	'IGNORE_TRIGGERS'				;
IMMEDIATE						:	'IMMEDIATE'						;
IMPERSONATE                     :   'IMPERSONATE'                   ;
INCLUDE                         :   'INCLUDE'                       ;
INCREMENTAL						:	'INCREMENTAL'					;
INCREMENT						:	'INCREMENT'						;
INIT							:	'INIT'							;
INITIATOR                       :   'INITIATOR'                     ;
INNER							:	'INNER'							;
INSERT							:	'INSERT'						;
INSTEAD							:	'INSTEAD'						;
INSENSITIVE                     :   'INSENSITIVE'                   ;
INTEGRATED						:	'INTEGRATED'					;
INTERSECT						:	'INTERSECT'						;
INTO							:	'INTO'							;
IO                              :   'IO'                            ;
IS								:	'IS'							;
ISOLATION                       :   'ISOLATION'                     ;
JOB                             :   'JOB'                           ;
JOIN							:	'JOIN'							;
KAND							:	'AND'							;
KB								:	'KB'							;
KDELETE							:	'DELETE'						;
KEEPDEFAULTS					:	'KEEPDEFAULTS'					;
KEEPFIXED						:	'KEEPFIXED'						;
KEEPIDENTITY					:	'KEEPIDENTITY'					;
KEEP							:	'KEEP'							;
KEEPNULLS						:	'KEEPNULLS'						;
KERBEROS						:	'KERBEROS'						;
KEY								: 	'KEY'							;
KEY_SOURCE                      :   'KEY_SOURCE'                    ;
KEYS							:	'KEYS'							;
KEYSET                          :   'KEYSET'                        ;
KILL                            :   'KILL'                          ;
KILOBYTES_PER_BATCH				:	'KILOBYTES_PER_BATCH'			;
KINDEX							:	'INDEX'							;
KIN								:	'IN'							;
KINPUT							:	'INPUT'							;
KMARK							:	'MARK'							;
KNOT							:	'NOT'							;
KNULL							:	'NULL'							;
KOR								:	'OR'							;
KOUT							:	'OUT'							;
KQUERY                          :   'QUERY'                         ;
KREWIND							:	'REWIND'						;
KSKIP							:	'SKIP'							;
LAST                            :   'LAST'                          ;
LANGUAGE						:	'LANGUAGE'						;
LASTROW							:	'LASTROW'						;
LEFT							:	'LEFT'							;
LEVEL                           :   'LEVEL'                         ;
LIFETIME						:	'LIFETIME'						;
LIKE							:	'LIKE'							;
LINKED                          :	'LINKED'						;
LISTENER_PORT                   :   'LISTENER_PORT'                 ;
LISTENER_IP						:	'LISTENER_IP'					;
LOB_COMPACTION					:	'LOB_COMPACTION'				;
LOCAL			    			:   'LOCAL'							;
LOGIN							:	'LOGIN'							;
LOGIN_TYPE						:	'LOGIN_TYPE'					;
LOG								:	'LOG'			    			;
LOGON							:	'LOGON'							;
LOOP							:	'LOOP'							;
LOW                             :   'LOW'                           ;
MACHINE							:	'MACHINE'						;
MANUAL							:	'MANUAL'						;
MASKED                          :	'MASKED'						;
MASTER							:	'MASTER'						;
MATCHED                         :   'MATCHED'                       ;
MAXDOP							:	'MAXDOP'						;
MAXERRORS						:	'MAXERRORS'						;
KMAX							:	'MAX'							;
MAX_QUEUE_READERS				:	'MAX_QUEUE_READERS'				;
MAXRECURSION					:	'MAXRECURSION'					;
MAXSIZE							:	'MAXSIZE'						;
MAXTRANSFERSIZE					:	'MAXTRANSFERSIZE'				;
MB								:	'MB'							;
MEDIADESCRIPTION				:	'MEDIADESCRIPTION'				;
MEDIANAME						:	'MEDIANAME'						;
MEDIAPASSWORD					:	'MEDIAPASSWORD'					;
MERGE							:	'MERGE'							;
MESSAGE_FORWARDING				:	'MESSAGE_FORWARDING'			;
MESSAGE_FORWARD_SIZE			:	'MESSAGE_FORWARD_SIZE'			;
MESSAGE							:	'MESSAGE'						;
KMIN							:	'MIN'							;
MIRROR_ADDRESS					:	'MIRROR_ADDRESS'				;
MIRROR							:	'MIRROR'						;
MIXED							:	'MIXED'							;
MODIFY							:	'MODIFY'						;
MOVE							:	'MOVE'							;
MULTI_USE						:	'MULTI_USE'						;
MULTI_USER						:	'MULTI_USER'					;
MUST_CHANGE						:	'MUST_CHANGE'					;
NAME							:	'NAME'							;
NAMESPACE						:	'NAMESPACE'						;
NEGOTIATE						:	'NEGOTIATE'						;
NEW_ACCOUNT						:	'NEW_ACCOUNT'					;
NEW_BROKER						:	'NEW_BROKER'					;
NEWNAME							:	'NEWNAME'	    				;
NEW_PASSWORD					:	'NEW_PASSWORD'					;
NEXT							:	'NEXT'							;
NO_ACTION						:	'NO_ACTION'						;
NOACTION						:	'NOACTION'						;
NOCHECK							:	'NOCHECK'						;
NO_CHECKSUM						:	'NO_CHECKSUM'					;
NODE							:	'NODE'							;
NOEXPAND						:	'NOEXPAND'						;
NOFORMAT						:	'NOFORMAT'						;
NOINIT							:	'NOINIT'						;
NOLOCK							:	'NOLOCK'						;
NO_LOG							:	'NO_LOG'						;
NONCLUSTERED					:	'NONCLUSTERED'					;
NONE							:	'NONE'			    			;
NO								:	'NO'							;
NORECOMPUTE                     :   'NORECOMPUTE'                   ;
NORECOVERY						:	'NORECOVERY'					;
NOREWIND						:	'NOREWIND'						;
NORMAL                          :   'NORMAL'                        ;
NOSKIP							:	'NOSKIP'						;
NOTIFICATION                    :   'NOTIFICATION'                  ;
NOTIFICATIONS                    :	'NOTIFICATIONS'					;
NO_TRUNCATE						:	'NO_TRUNCATE'					;
NOUNLOAD						:	'NOUNLOAD'						;
NO_WAIT							:	'NO_WAIT'						;
NOWAIT							:	'NOWAIT'						;
NRA             				:	'NUMERIC_ROUNDABORT'            ;
NTILE							:	'NTILE'							;
NTLM							:	'NTLM'							;
OBJECT							:	'OBJECT'						;
OFFLINE			    			:	'OFFLINE'			    		;
OFF								:	'OFF'							;
OF								:	'OF'							;
OLD_ACCOUNT						:	'OLD_ACCOUNT'					;
OLD_PASSWORD					:	'OLD_PASSWORD'					;
ONLINE			    			:	'ONLINE'						;
ONLY							:	'ONLY'							;
ON								:	'ON'							;
OPEN                            :   'OPEN'                          ;
OPENDATASOURCE					:	'OPENDATASOURCE'				;
OPENQUERY						:	'OPENQUERY'						;
OPENROWSET						:	'OPENROWSET'					;
OPENXML							:	'OPENXML'						;
OPERATIONS                      :	'OPERATIONS'					;
OPTIMISTIC                      :   'OPTIMISTIC'                    ;
OPTIMIZE						:	'OPTIMIZE'						;
OPTION							:	'OPTION'						;
ORDER							:	'ORDER'							;
OUTER							:	'OUTER'							;
OUTPUT							:	'OUTPUT'						;
OVER							:	'OVER'							;
OVERRIDE                        :   'OVERRIDE'                      ;
OWNER							:	'OWNER'							;
OWNERSHIP                       :   'OWNERSHIP'                     ;
PAD_INDEX						:	'PAD_INDEX'						;
PAGE                            :   'PAGE'                          ;
PAGE_VERIFY						:	'PAGE_VERIFY'					;
PAGECOUNT                       :	'PAGECOUNT'						;
PAGLOCK							:	'PAGLOCK'						;
PARAMETERIZATION				:	'PARAMETERIZATION'				;
PARTIAL                         :	'PARTIAL'						;
PARTITION						: 	'$'? 'PARTITION'				;
PARTITIONS						: 	'PARTITIONS'                    ;
PARTNER			    			:	'PARTNER'			    		;
PASSWORD						:	'PASSWORD'						;
PATH							:	'PATH'							;
PAUSE							:	'PAUSE'							;
PERCENT							:	'PERCENT'						;
PERMISSION_SET					:	'PERMISSION_SET'				;
PERSISTED						:	'PERSISTED'						;
PIVOT							:	'PIVOT'							;
PLAN							:	'PLAN'							;
POPULATION						:	'POPULATION'					;
PORTS							:	'PORTS'							;
PRIMARY							:	'PRIMARY'						;
PRINT                           :   'PRINT'                         ;
PRIOR                           :   'PRIOR'                         ;
PRIVATE							:	'PRIVATE'						;
PRIVILEDGES                     :   'PRIVILEDGES'                   ;
PROFILE                         :   'PROFILE'                       ;
PROCEDURE_NAME					:	'PROCEDURE_NAME'				;
PROCEDURE						:	'PROC' 'EDURE'?					;
PROPERTY                        :	'PROPERTY'						;
QUEUE							:	'QUEUE'							;
QUOTED_IDENTIFIER				:	'QUOTED_IDENTIFIER'				;
RAISERROR                       :   'RAIS' 'E'? 'ERROR'             ;
RANGE							:	'RANGE'							;
RANK							:	'RANK'							;
RAW								:	'RAW'							;
RECEIVE                         :   'RECEIVE'                       ;
READ                            :   'READ'                          ;
READCOMMITTEDLOCK				:	'READCOMMITTEDLOCK'				;
READCOMMITTED					:	'READCOMMITTED'					;
READ_COMMITTED_SNAPSHOT			:	'READ_COMMITTED_SNAPSHOT'		;
READ_ONLY						:	'READ_ONLY'						;
READPAST						:	'READPAST'						;
READTEXT                        :   'READTEXT'                      ;
READUNCOMMITTED					:	'READUNCOMMITTED'				;
READ_WRITE_FILEGROUPS			:	'READ_WRITE_FILEGROUPS'			;
READ_WRITE						:	'READ_WRITE'					;
REBUILD							:	'REBUILD'						;
RECOMPILE						:	'RECOMPILE'						;
RECONFIGURE                     :   'RECONFIGURE'                   ;
RECOVERY 						:	'RECOVERY'						;
RECURSIVE_TRIGGERS				:	'RECURSIVE_TRIGGERS'			;
REFERENCES						:	'REFERENCES'					;
REGENERATE						:	'REGENERATE'					;
RELATED_CONVERSATION_GROUP		:	'RELATED_CONVERSATION_GROUP'	;
RELATED_CONVERSATION			:	'RELATED_CONVERSATION'			;
RELATIVE                        :   'RELATIVE'                      ;
REMOTE							:	'REMOTE'						;
REMOVE							:	'REMOVE'						;
REORGANIZE						:	'REORGANIZE'					;
REPEATABLEREAD					:	'REPEATABLEREAD'				;
REPEATABLE						:	'REPEATABLE'					;
REPLICATION						:	'REPLICATION'					;
REQUIRED						:	'REQUIRED'						;
RESAMPLE						:	'RESAMPLE'						;
RESET							:	'RESET'							;
RESOURCES                       :	'RESOURCES'						;
RESTART							:	'RESTART'						;
RESTORE                         :   'RESTORE'                       ;
RESTRICTED_USE			    	:	'RESTRICTED_USE'			    ;
RESTRICTED_USER					:	'RESTRICTED'					;
RESUME			    			:	'RESUME'						;
RETAINDAYS						:	'RETAINDAYS'					;
RETENTION						:	'RETENTION'						;
RETURN							:	'RETURN'						;
RETURNS							:	'RETURNS'						;
REVERT                          :   'REVERT'                        ;
REVOKE                          :   'REVOKE'                        ;
RIGHT							:	'RIGHT'							;
ROBUST							:	'ROBUST'						;
ROLE							:	'ROLE'							;
ROLLBACK						:	'ROLLBACK'						;
ROLLUP							:	'ROLLUP'						;
ROOT							:	'ROOT'							;
ROUTE							:	'ROUTE'							;
ROWGUIDCOL						:	'ROWGUIDCOL'					;
ROWLOCK							:	'ROWLOCK'						;
ROW_NUMBER						:	'ROW_NUMBER'					;
ROWSETS_ONLY					:	'ROWSETS_ONLY'					;
ROWS_PER_BATCH					:	'ROWS_PER_BATCH'				;
ROW                             :   'ROW'                           ;
ROWCOUNT                        :	'ROWCOUNT'						;
ROWS							:	'ROWS'							;
ROWTERMINATOR					:	'ROWTERMINATOR'					;
RULE                            :   'RULE'                          ;
SAFE							:	'SAFE'							;
SAFETY			    			:	'SAFETY'			    		;
SAMPLE                          :   'SAMPLE'                        ;
SAVE                            :   'SAVE'                          ;
SCHEMABINDING					:	'SCHEMABINDING'					;
SCHEMA							:	'SCHEMA'						;
SCHEME							:	'SCHEME'						;
SCROLL                          :   'SCROLL'                        ;
SCROLL_LOCKS                    :   'SCROLL_LOCKS'                  ;
SECONDS							:	'SECONDS'						;
SECRET							:	'SECRET'						;
SELECT							:	'SELECT'						;
SELF							:	'SELF'							;
SEND                            :   'SEND'                          ;
SENT                            :   'SENT'                          ;
SERIALIZABLE					:	'SERIALIZABLE'					;
SERVER							:	'SERVER'						;
SERVICE_BROKER					:	'SERVICE_BROKER'				;
SERVICE_NAME					:	'SERVICE_NAME'					;
SERVICE							:	'SERVICE'						;
SESSIONS						:	'SESSIONS'						;
SESSION_TIMEOUT					:	'SESSION_TIMEOUT'				;
SET								:	'SET'			    			;
SETS                            :   'SETS'                          ;
SETTINGS                        :	'SETTINGS'						;
SETUSER                         :   'SETUSER'                       ;
SETERROR                        :   'SETERROR'                      ;
SHOWPLAN                        :   'SHOWPLAN'                      ;
SHUTDOWN                        :   'SHUTDOWN'                      ;
SID                             :	'SID'							;
SIGNATURE						:	'SIGNATURE'						;
SIMPLE			    			:	'SIMPLE'			    		;
SINGLE_BLOB						:	'SINGLE_BLOB'					;
SINGLE_CLOB						:	'SINGLE_CLOB'					;
SINGLE_NCLOB					:	'SINGLE_NCLOB'					;
SINGLE_USER						:	'SINGLE_USER'					;
SINGLE_USE						:	'SINGLE_USE'			    	;
SITE							:	'SITE'							;
SIZE							:	'SIZE'							;
SNAPSHOT                        :   'SNAPSHOT'                      ;
SOAP							:	'SOAP'							;
SOME							:	'SOME'							;
SORT_IN_TEMPDB					:	'SORT_IN_TEMPDB'				;
SOURCE                          :   'SOURCE'                        ;
SPARSE                          :   'SPARSE'                        ;
SPATIAL                         :	'SPATIAL'						;
SPLIT							:	'SPLIT'							;
SQL								:	'SQL'							;
SSL_PORT						:	'SSL_PORT'						;
SSL								:	'SSL'							;
STANDARD						:	'STANDARD'						;
STANDBY							:	'STANDBY'						;
STARTED							:	'STARTED'						;
START_DATE						:	'START_DATE'					;
START							:	'START'							;
STATIC                          :   'STATIC'                        ;
STATE							:	'STATE'							;
STATISTICS_NORECOMPUTE			:	'STATISTICS_NORECOMPUTE'		;
STATISTICS                      :   'STATISTICS'                    ;
STATS							:	'STATS'							;
STATS_STREAM                    :	'STATS_STREAM'					;
KSTATUS							:	'STATUS'						;
STATUSONLY                      :   'STATUSONLY'                    ;
STDEVP							:	'STDEVP'						;
STDEV							:	'STDEV'							;
STOP_ON_ERROR					:	'STOP_ON_ERROR'					;
STOPPED							:	'STOPPED'						;
STOP							:	'STOP'							;
SUBSCRIBE                       :	'SUBSCRIBE'						;
SUBJECT							:	'SUBJECT'						;
SUBSCRIPTION                    :   'SUBSCRIPTION'                  ;
SUM								:	'SUM'							;
SUPPORTED						:	'SUPPORTED'						;
SUSPEND			    			:	'SUSPEND'			    		;
SWITCH							:	'SWITCH'						;
SYMMETRIC						:	'SYMMETRIC'						;
SYNONYM                         :   'SYNONYM'                       ;
SYS                             :   'SYS'                           ;
SYSTEM							:	'SYSTEM'						;
TABLESAMPLE						:	'TABLESAMPLE'					;
TABLE							:	'TABLE'							;
TABLOCK							:	'TABLOCK'						;
TABLOCKX						:	'TABLOCKX'						;
TAKE                            :   'TAKE'                          ;
TAPE							:	'TAPE'							;
TARGET                          :   'TARGET'                        ;
TB								:	'TB'							;
TCP								:	'TCP'							;
TEXTIMAGE_ON                    :   'TEXTIMAGE_ON'                  ;
THEN							:	'THEN'							;
TIES							:	'TIES'							;
TIMEOUT			    			:	'TIMEOUT'			    		;
TIME                            :   'TIME'                          ;
TIMER							:	'TIMER'							;
TOP								:	'TOP'							;
TORN_PAGE_DETECTION				:	'TORN_PAGE_DETECTION'			;
TO								:	'TO'							;
TRACE                           :   'TRACE'                         ;
TRANSACTION						:	'TRAN' 'SACTION'?				;
TRANSFER						:	'TRANSFER'						;
TRIGGER							:	'TRIGGER'						;
TRUNCATE                        :   'TRUNCATE'                      ;
TRUNCATE_ONLY					:	'TRUNCATE_ONLY'					;
TRUSTWORTHY						:	'TRUSTWORTHY'			    	;
TRY								:	'TRY'							;
TSQL                            :   'TSQL'                          ;
TYPE							:	'TYPE'							;
TYPE_WARNING                    :   'TYPE_WARNING'                  ;
UNCHECKED						:	'UNCHECKED'						;
UNCOMMITTED						:	'UNCOMMITTED'					;
UNION							:	'UNION'							;
UNIQUE							:	'UNIQUE'						;
UNLIMITED						:	'UNLIMITED'						;
UNLOAD							:	'UNLOAD'						;
UNLOCK							:	'UNLOCK'						;
UNPIVOT							:	'UNPIVOT'						;
UNSAFE							:	'UNSAFE'						;
UPDATE							:	'UPDATE'						;
UPDATETEXT                      :   'UPDATETEXT'                    ;
UPDLOCK							:	'UPDLOCK'						;
USED							:	'USED'							;
USER							:	'USER'							;
USE								:	'USE'							;
USING                           :   'USING'                         ;
VALIDATION						:	'VALIDATION'					;
VALID_XML						:	'VALID_XML'						;
VALUE                           :	'VALUE'							;
VALUES							:	'VALUES'						;
VARP							:	'VARP'							;
VAR								:	'VAR'							;
VARYING							:	'VARYING'						;
VIEW_METADATA					:	'VIEW_METDATA'					;
VIEWS							:	'VIEWS'							;
VIEW							:	'VIEW'							;
VISIBILITY						:	'VISIBILITY'					;
WAITFOR                         :   'WAITFOR'                       ;
WEBMETHOD						:	'WEBMETHOD'						;
WELL_FORMED_XML					:	'WELL_FORMED_XML'				;
WHEN							:	'WHEN'							;
WHERE							:	'WHERE'							;
WHILE                           :   'WHILE'                         ;
WINDOWS							:	'WINDOWS'						;
WITH							:	'WITH'							;
WITHOUT                         :	'WITHOUT'						;
WITNESS			    			:	'WITNESS'			    		;
WORK							:	'WORK'							;
WRITETEXT                       :   'WRITETEXT'                     ;
WSDL							:	'WSDL'							;
XLOCK							:	'XLOCK'							;
XMLDATA							:	'XMLDATA'						;
XMLSCHEMA						:	'XMLSCHEMA'						;
XML								:	'XML'							;
XSINIL							:	'XSINIL'						;
FILELISTONLY                    :   'FILELISTONLY'                  ;
HEADERONLY                      :   'HEADERONLY'                    ;
LABELONLY                       :   'LABELONLY'                     ;
REWINDONLY                      :   'REWINDONLY'                    ;
VERIFYONLY                      :   'VERIFYONLY'                    ;

CHECKALLOC                      :   'CHECKALLOC'                    ;
CHECKCATALOG                    :   'CHECKCATALOG'                  ;
CHECKCONSTRAINTS                :   'CHECKCONSTRAINTS'              ;
CHECKDB                         :   'CHECKDB'                       ;
CHECKFILEGROUP                  :   'CHECKFILEGROUP'                ;
CHECKIDENT                      :   'CHECKIDENT'                    ;
CHECKTABLE                      :   'CHECKTABLE'                    ;
CLEANTABLE                      :   'CLEANTABLE'                    ;
CONCURRENCYVIOLATION            :   'CONCURRENCYVIOLATION'          ;
DBREINDEX                       :   'DBREINDEX'                     ;
DBREPAIR                        :   'DBREPAIR'                      ;
DROPCLEANBUFFERS                :   'DROPCLEANBUFFERS'              ;
FREEPROCCACHE                   :   'FREEPROCCACHE'                 ;
FREESESSIONCACHE                :   'FREESESSIONCACHE'              ;
FREESYSTEMCACHE                 :   'FREESYSTEMCACHE'               ;
HELP                            :   'HELP'                          ;
INDEXDEFRAG                     :   'INDEXDEFRAG'                   ;
INPUTBUFFER                     :   'INPUTBUFFER'                   ;
OPENTRAN                        :   'OPENTRAN'                      ;
OUTPUTBUFFER                    :   'OUTPUTBUFFER'                  ;
PINTABLE                        :   'PINTABLE'                      ;
PROCCACHE                       :   'PROCCACHE'                     ;
SHOW_STATISTICS                 :   'SHOW_STATISTICS'               ;
SHOWCONTIG                      :   'SHOWCONTIG'                    ;
SHRINKDATABASE                  :   'SHRINKDATABASE'                ;
SHRINKFILE                      :   'SHRINKFILE'                    ;
SQLPERF                         :   'SQLPERF'                       ;
TRACEOFF                        :   'TRACEOFF'                      ;
TRACEON                         :   'TRACEON'                       ;
TRACESTATUS                     :   'TRACESTATUS'                   ;
UNPINTABLE                      :   'UNPINTABLE'                    ;
UPDATEUSAGE                     :   'UPDATEUSAGE'                   ;
USEROPTIONS                     :   'USEROPTIONS'                   ;
CURRENT                         :   'CURRENT'                       ;

//////////////////////////////////////////////////////////////////////
// SQL Identifer, used for table names, variables and so on
// note that bracketed ids are returned as BR_LITERALS
//
ID		: (ALPHA | '_' | '@' | '#') (ALNUM | '_' | '@' | '#' | '$' )*
		;

///////////////////////////////////////////////////////////////////////
// Operators, single character keywords and the like
//
COMMA		:	','             ;
DOT			:	'.'             ;
LPAREN		:	'('             ;
RPAREN		:	')'         	;
DOLLAR		:	'$'             ;
OPPLUSEQ    :   '+='            ;
OPPLUS		: 	'+'             ;
BANG        :	'!'             ;
OPCAT       :	'||'            ;

OPMINUSEQ   :   '-='            ;
OPMINUS		:	'-'             ;
OPMULEQ     :   '*='            ;
OPMUL		:	'*'             ;
OPDIVEQ     :   '/='            ;
OPDIV		:	'/'             ;
OPMODEQ     :   '%='            ;
OPMOD		:	'%'             ;
OPBANDEQ    :   '&='            ;
OPBAND		:	'&'             ;
OPBOREQ     :   '|='            ;
OPBOR		:	'|'             ;
OPBXOREQ    :   '^='            ;
OPBXOR		:	'^'             ;
OPBNOT		:	'~'             ;
OPEQ		:	'='             ;
OPGT		:	'>'             ;
OPLT		:	'<'             ;
// T-SQL lexer/parser is weak and allows "<      >" to mean OPNE and so on
// It likely does not define them as separate tokens
OPGE		:	'>' WSfrag* '=' ;
OPLE		:	'<' WSfrag* '=' ;
OPNE		:	'<' WSfrag* '>'
            |   '!' WSfrag* '=' ;
OPNLT		:	'!' WSfrag* '<' ;
OPNGT		:	'!' WSfrag* '>' ;
OPSEQ       :   '=*'            ;
COLON		:	':'         	;
SEMI		:	';'             ;

// We are stuck with the fact that T-SQL does not delimit currency values in any way so
// we must specify all the currency symbols here by their Unicode code point, then allow
// this token as well as any currency symbols used elsewhere, such as $ to precede a
// money value in a parser rule. Some currencies such as the Albanian Lek use the
// code point sequence that represents their name. Until I can find out if SQL server
// really supports those or only single codepoint symbols, I have left those out. If
// they are required then they will be returned by a separate token in order that
// they may be allowed as Identifiers in keyw_id when they might conflict.
// Many currencies are covered by the dollar symbol, which is returned as a separate
// token for other reasons.
//
// Source: http://www.xe.com/symbols.php
//
CURRENCY_SYMBOL
			: '\u060b'				// Afghanistan Afghanis
			| '\u0192'				// Aruba Guilders/Florins
			// TODO: And so on down to...
			| '\u00a3'				// UK Quid
			// TODO: And so on down to...
			| '\ufdfc'				// Yemen Rials
			;

// The lexer should never raise errors as errors should propagate
// as high up the tool chain as they can go. In this case, the parser
// will report the error as a BAD_CHARACTER syntax error.
BAD_CHARACTER
            : .
            ;
