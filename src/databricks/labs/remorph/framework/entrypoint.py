import logging
import os
import sys
from pathlib import Path

from databricks.labs.remorph.framework.logger import install_logger


def get_logger(file_name: str):
    project_root = find_project_root().absolute()
    entrypoint = Path(file_name).absolute()

    relative = entrypoint.relative_to(project_root).as_posix()
    relative = relative.lstrip('src' + os.sep)
    relative = relative.rstrip('.py')
    module_name = relative.replace(os.sep, '.')

    logger = logging.getLogger(module_name)

    level = 'INFO'
    if is_in_debug():
        level = 'DEBUG'
    logger.setLevel(level)

    return logger


def run_main(main):
    install_logger()
    main(*sys.argv[1:])


def find_project_root() -> Path:
    this_path = Path(__file__)
    # TODO: detect when in wheel
    for leaf in ["pyproject.toml", "setup.py"]:
        root = find_dir_with_leaf(this_path, leaf)
        if root is not None:
            return root
    msg = "Cannot find project root"
    raise NotADirectoryError(msg)


def find_dir_with_leaf(folder: Path, leaf: str) -> Path | None:
    root = folder.root
    while str(folder.absolute()) != root:
        if (folder / leaf).exists():
            return folder
        folder = folder.parent
    return None


def is_in_debug() -> bool:
    if 'IDE_PROJECT_ROOTS' in os.environ:
        return True
    return os.path.basename(sys.argv[0]) in [
        "_jb_pytest_runner.py",
        "testlauncher.py",
    ]


def relative_paths(*maybe_paths) -> list[Path]:
    all_paths = [Path(str(_)) for _ in maybe_paths]
    common_path = Path(os.path.commonpath([_.as_posix() for _ in all_paths]))
    return [_.relative_to(common_path) for _ in all_paths]
