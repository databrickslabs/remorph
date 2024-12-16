import os
import sys
from typing import Any

from lsprotocol.types import InitializeParams, InitializeResult, INITIALIZE, ServerCapabilities
from pygls.lsp.server import LanguageServer

import logging

logging.basicConfig(filename='test-lsp-server.log', filemode='w', level=logging.DEBUG)

logger = logging.getLogger(__name__)

class TestLspServer(LanguageServer):

    CMD_TRANSPILE = "transpile"

    def __init__(self, name, version):
        super().__init__(name, version)
        self.initialization_options: Any = None

    @property
    def dialect(self) -> str:
        return self.initialization_options["remorph"]["source-dialect"]

    @property
    def whatever(self) -> str:
        return self.initialization_options["custom"]["whatever"]



server = TestLspServer("test-lsp-server", "v0.1")

@server.feature(INITIALIZE)
def lsp_initialize(params: InitializeParams) -> None:
    server.initialization_options = params.initialization_options
    logger.debug(f"dialect={server.dialect}")
    logger.debug(f"whatever={server.whatever}")


if __name__ == "__main__":
    logger.debug(f"SOME_ENV={os.getenv('SOME_ENV')}")
    logger.debug(f"sys.args={sys.argv}")
    server.start_io()
