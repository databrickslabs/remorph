import os
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any
from uuid import uuid4

from lsprotocol.types import (
    InitializeParams,
    INITIALIZE,
    RegistrationParams,
    Registration, TextEdit, Diagnostic, InitializeResponse, TEXT_DOCUMENT_DID_OPEN, DidOpenTextDocumentParams,
    TEXT_DOCUMENT_DID_CLOSE, DidCloseTextDocumentParams,
)
from pygls.lsp.server import LanguageServer

import logging

logging.basicConfig(filename='test-lsp-server.log', filemode='w', level=logging.DEBUG)

logger = logging.getLogger(__name__)

TRANSPILE_TO_DATABRICKS_CMD = "transpileToDatabricks"
TRANSPILE_TO_DATABRICKS_FEATURE = f"document/{TRANSPILE_TO_DATABRICKS_CMD}"
TRANSPILE_TO_DATABRICKS_CAPABILITY = {
    "id": str(uuid4()),
    "method": TRANSPILE_TO_DATABRICKS_FEATURE
}


@dataclass
class TranspileParams:
    document_uri: str


@dataclass
class TranspileResponse:
    document_uri: str
    changes: Sequence[TextEdit]
    diagnostics: Sequence[Diagnostic]

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
        await server.client_register_capability_async(register_params)

    def transpile_to_databricks(self, params: TranspileParams) -> TranspileResponse:
        return TranspileResponse(document_uri=params.document_uri, changes=[], diagnostics=[])


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


@server.feature(TRANSPILE_TO_DATABRICKS_FEATURE)
def transpile_to_databricks(params: TranspileParams) -> TranspileResponse:
    return server.transpile_to_databricks(params)


if __name__ == "__main__":
    logger.debug(f"SOME_ENV={os.getenv('SOME_ENV')}")
    logger.debug(f"sys.args={sys.argv}")
    server.start_io()
