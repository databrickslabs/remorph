import json
import logging
import os
import subprocess
from collections.abc import Generator
from datetime import datetime
from pathlib import Path
from typing import Any, TextIO

from sqlglot import parse
from sqlglot.dialects.dialect import Dialect
from sqlglot.errors import ErrorLevel

logger = logging.getLogger(__name__)


def get_supported_sql_files(input_dir: Path) -> Generator[Path, None, None]:
    yield from filter(lambda item: item.is_file() and item.suffix.lower() in [".sql", ".ddl"], input_dir.rglob("*"))


def write_json_line(file: TextIO, content: dict[str, Any]):
    json.dump(content, file)
    file.write("\n")


def get_env_var(env_var: str, *, required: bool = False) -> str:
    """
    Get the value of an environment variable.

    :param env_var: The name of the environment variable to get the value of.
    :param required: Indicates if the environment variable is required and raises a ValueError if it's not set.
    :return: Returns the environment variable's value, or None if it's not set and not required.
    """
    value = os.getenv(env_var)
    if value is None and required:
        message = f"Environment variable {env_var} is not set"
        raise ValueError(message)
    return value


def get_current_commit_hash() -> str | None:
    try:
        return (
            subprocess.check_output(
                ["/usr/bin/git", "rev-parse", "--short", "HEAD"],
                cwd=Path(__file__).resolve().parent,
            )
            .decode("ascii")
            .strip()
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logger.warning(f"Could not get the current commit hash. {e!s}")
        return None


def collect_transpilation_stats(
    project: str,
    commit_hash: str,
    version: str,
    source_dialect: type[Dialect],
    target_dialect: type[Dialect],
    input_dir: Path,
    result_dir: Path,
):
    if not input_dir.exists() or not input_dir.is_dir():
        message = f"The input path {input_dir} doesn't exist or is not a directory"
        raise NotADirectoryError(message)

    if not result_dir.exists():
        logger.info(f"Creating the output directory {result_dir}")
        result_dir.mkdir(parents=True)
    elif not result_dir.is_dir():
        message = f"The output path {result_dir} exists but is not a directory"
        raise NotADirectoryError(message)

    source_dialect_name = source_dialect.__name__
    target_dialect_name = target_dialect.__name__
    report_file_path = result_dir / f"{project}_{source_dialect_name}_{target_dialect_name}.jsonl".lower()

    with open(report_file_path, "w", encoding="utf8") as report_file:
        for input_file in get_supported_sql_files(input_dir):
            sql = input_file.read_text(encoding="utf-8-sig")
            report_entry = {
                "project": project,
                "commit_hash": commit_hash,
                "version": version,
                "source_dialect": source_dialect_name,
                "target_dialect": target_dialect_name,
                "timestamp": datetime.utcnow().isoformat(),
                "filename": str(input_file.absolute().relative_to(input_dir.parent.absolute())),
                "parsing_status": "",
                "queries_parsed": 0,
                "parsing_error": "",
                "transpilation_status": "",
                "queries_transpiled": 0,
                "transpilation_error": "",
            }
            try:
                expressions = [
                    expression
                    for expression in parse(
                        sql,
                        read=source_dialect,
                        error_level=ErrorLevel.RAISE,
                    )
                    if expression
                ]
                report_entry["parsing_status"] = "successful"
                report_entry["queries_parsed"] = len(expressions)
            except Exception as pe:
                report_entry["parsing_status"] = "failed"
                report_entry["parsing_error"] = str(pe)
                report_entry["transpilation_status"] = "skipped"
                continue

            try:
                write_dialect = Dialect.get_or_raise(target_dialect)
                generated_sqls = [write_dialect.generate(expression, copy=False) for expression in expressions]
                report_entry["queries_transpiled"] = len([sql for sql in generated_sqls if sql.strip()])
                report_entry["transpilation_status"] = "successful"
            except Exception as te:
                report_entry["transpilation_status"] = "failed"
                report_entry["transpilation_error"] = str(te)

            write_json_line(report_file, report_entry)
