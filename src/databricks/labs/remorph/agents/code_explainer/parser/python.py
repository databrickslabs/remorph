from __future__ import annotations

from collections.abc import Iterator

from langchain_core.documents import Document
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers.language import LanguageParser


class PythonParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.loader = GenericLoader.from_filesystem(self.file_path, parser=LanguageParser("python"))

    def parse(self) -> list[Document] | None:
        """Parse the Python code into list of Documents"""
        return self.loader.load()

    def lazy_parse(self) -> Iterator[Document] | None:
        """Parse the Python code into Documents. Yields one Document at a time."""
        return self.loader.lazy_load()
