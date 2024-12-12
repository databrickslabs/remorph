import os
import sys
from typing import Any

from lsprotocol.types import InitializeParams, InitializeResult, INITIALIZE
from pygls.lsp.server import LanguageServer

import logging

from pygls.protocol import LanguageServerProtocol, lsp_method

logging.basicConfig(filename='test-lsp-server.log', filemode='w', level=logging.DEBUG)

logger = logging.getLogger(__name__)


class TestProtocol(LanguageServerProtocol):

    @lsp_method(INITIALIZE)
    def lsp_initialize(self, params: InitializeParams) -> InitializeResult:
        result = super().lsp_initialize(params)
        server.initialization_options = params.initialization_options
        return result


class TestLspServer(LanguageServer):

    CMD_TRANSPILE = "transpile"

    def __init__(self, name, version):
        super().__init__(name, version, protocol_cls=TestProtocol)
        self.initialization_options: Any = None

    @property
    def dialect(self) -> str:
        return self.initialization_options["remorph"]["dialect"]


server = TestLspServer("test-lsp-server", "v0.1")

if __name__ == "__main__":
    logger.debug(f"SOME_ENV={os.getenv('SOME_ENV')}")
    logger.debug(f"sys.args={sys.argv}")
    server.start_io()
