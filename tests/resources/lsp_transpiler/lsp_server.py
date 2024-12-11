from pygls.lsp.server import LanguageServer

import logging

logging.basicConfig(filename='test-lsp-server.log', filemode='w', level=logging.DEBUG)

class TestLspServer(LanguageServer):
    CMD_TRANSPILE = "transpile"


server = TestLspServer("test-lsp-server", "v0.1")

if __name__ == "__main__":
    server.start_io()
