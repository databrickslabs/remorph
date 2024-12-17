import os
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, Optional, Type, Literal, Union
from uuid import uuid4

import attrs
from cattrs import Converter
from cattrs.converters import T
from cattrs.dispatch import UnstructuredValue
from lsprotocol.types import (
    InitializeParams,
    INITIALIZE,
    RegistrationParams,
    Registration, TextEdit, Diagnostic, InitializeResponse, TEXT_DOCUMENT_DID_OPEN, DidOpenTextDocumentParams,
    TEXT_DOCUMENT_DID_CLOSE, DidCloseTextDocumentParams, Range, Position, METHOD_TO_TYPES,
)
from pygls.lsp.server import LanguageServer

import logging

from pygls.protocol import LanguageServerProtocol, JsonRPCRequestMessage, default_converter, JsonRPCProtocol

logging.basicConfig(filename='test-lsp-server.log', filemode='w', level=logging.DEBUG)

logger = logging.getLogger(__name__)

TRANSPILE_TO_DATABRICKS_METHOD = "document/transpileToDatabricks"
TRANSPILE_TO_DATABRICKS_CAPABILITY = {
    "id": str(uuid4()),
    "method": TRANSPILE_TO_DATABRICKS_METHOD
}


@attrs.define
class TranspileDocumentParams:
    uri: str = attrs.field()
    language_id: str = attrs.field()

@attrs.define
class TranspileDocumentRequest:
    id: Union[int, str] = attrs.field()
    params: TranspileDocumentParams = attrs.field()
    method: Literal["document/transpileToDatabricks"] = TRANSPILE_TO_DATABRICKS_METHOD
    jsonrpc: str = attrs.field(default="2.0")

@attrs.define
class TranspileDocumentResult:
    uri: str = attrs.field()
    changes: Sequence[TextEdit] = attrs.field()
    diagnostics: Sequence[Diagnostic] = attrs.field()

@attrs.define
class TranspileDocumentResponse:
    id: Union[int, str] = attrs.field()
    result: TranspileDocumentResult = attrs.field()
    jsonrpc: str = attrs.field(default="2.0")

METHOD_TO_TYPES[TRANSPILE_TO_DATABRICKS_METHOD] = (
    TranspileDocumentRequest,
    TranspileDocumentResponse,
    TranspileDocumentParams,
    None
    )

class TestLspServer(LanguageServer):

    def __init__(self, name, version):
        super().__init__(name, version)
        self.initialization_options: Any = None

    @property
    def dialect(self) -> str:
        return self.initialization_options["remorph"]["source-dialect"]

    @property
    def whatever(self) -> str:
        return self.initialization_options["custom"]["whatever"]

    async def did_initialize(self, init_params: InitializeParams) -> None:
        self.initialization_options = init_params.initialization_options
        logger.debug(f"dialect={server.dialect}")
        logger.debug(f"whatever={server.whatever}")
        # TODO check whether the client supports dynamic registration
        registrations = [Registration(id=TRANSPILE_TO_DATABRICKS_CAPABILITY["id"], method=TRANSPILE_TO_DATABRICKS_CAPABILITY["method"])]
        register_params = RegistrationParams(registrations)
        await self.client_register_capability_async(register_params)

    def transpile_to_databricks(self, params: TranspileDocumentParams) -> TranspileDocumentResult:
        source_sql = self.workspace.get_text_document(params.uri).source
        source_lines = source_sql.split("\n")
        transpiled_sql = source_sql.upper()
        changes = [
            TextEdit(
                range=Range(start=Position(0, 0), end=Position(len(source_lines), len(source_lines[-1]))),
                new_text=transpiled_sql
            )
        ]
        return TranspileDocumentResult(uri=params.uri, changes=changes, diagnostics=[])


server = TestLspServer("test-lsp-server", "v0.1")


@server.feature(INITIALIZE)
async def lsp_did_initialize(params: InitializeParams) -> None:
    await server.did_initialize(params)


@server.feature(TEXT_DOCUMENT_DID_OPEN)
async def lsp_text_document_did_open(params: DidOpenTextDocumentParams) -> None:
    logger.debug(f"open-document-uri={params.text_document.uri}")


@server.feature(TEXT_DOCUMENT_DID_CLOSE)
async def lsp_text_document_did_close(params: DidCloseTextDocumentParams) -> None:
    logger.debug(f"close-document-uri={params.text_document.uri}")


@server.feature(TRANSPILE_TO_DATABRICKS_METHOD)
def transpile_to_databricks(params: TranspileDocumentParams) -> TranspileDocumentResult:
    return server.transpile_to_databricks(params)


if __name__ == "__main__":
    logger.debug(f"SOME_ENV={os.getenv('SOME_ENV')}")
    logger.debug(f"sys.args={sys.argv}")
    server.start_io()
