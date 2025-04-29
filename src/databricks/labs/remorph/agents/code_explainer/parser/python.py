from __future__ import annotations

from typing import Any, Dict, Iterator, Literal, Optional, List

from langchain_core.documents import Document
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers.language import LanguageParser


class PythonParser(object):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.loader = GenericLoader.from_filesystem(
            self.file_path,
            parser=LanguageParser("python")
        )

    def parse(self) -> Optional[List[Document]]:
        """Parse the SQL code into list of Documents"""
        return self.loader.load()


    def lazy_parse(self) -> Optional[Iterator[Document]]:
        """Parse the SQL code into Documents. Yields one Document at a time."""
        return self.loader.lazy_load()
