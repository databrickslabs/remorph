import codecs
from pathlib import Path


# Optionally check to see if a string begins with a Byte Order Mark
# such a character will cause the transpiler to fail
def remove_bom(input_string: str) -> str:
    """
    Removes the Byte Order Mark (BOM) from the given string if it exists.
    :param input_string: String to remove BOM from
    :return: String without BOM
    """
    output_string = input_string

    # Check and remove UTF-16 (LE and BE) BOM
    if input_string.startswith(codecs.BOM_UTF16_BE.decode("utf-16-be")):
        output_string = input_string[len(codecs.BOM_UTF16_BE.decode("utf-16-be")) :]
    elif input_string.startswith(codecs.BOM_UTF16_LE.decode("utf-16-le")):
        output_string = input_string[len(codecs.BOM_UTF16_LE.decode("utf-16-le")) :]
    elif input_string.startswith(codecs.BOM_UTF16.decode("utf-16")):
        output_string = input_string[len(codecs.BOM_UTF16.decode("utf-16")) :]
    # Check and remove UTF-32 (LE and BE) BOM
    elif input_string.startswith(codecs.BOM_UTF32_BE.decode("utf-32-be")):
        output_string = input_string[len(codecs.BOM_UTF32_BE.decode("utf-32-be")) :]
    elif input_string.startswith(codecs.BOM_UTF32_LE.decode("utf-32-le")):
        output_string = input_string[len(codecs.BOM_UTF32_LE.decode("utf-32-le")) :]
    elif input_string.startswith(codecs.BOM_UTF32.decode("utf-32")):
        output_string = input_string[len(codecs.BOM_UTF32.decode("utf-32")) :]
    # Check and remove UTF-8 BOM
    elif input_string.startswith(codecs.BOM_UTF8.decode("utf-8")):
        output_string = input_string[len(codecs.BOM_UTF8.decode("utf-8")) :]

    return output_string


def is_sql_file(file: str | Path) -> bool:
    """
    Checks if the given file is a SQL file.

    :param file: The name of the file to check.
    :return: True if the file is a SQL file (i.e., its extension is either .sql or .ddl), False otherwise.
    """
    file_extension = Path(file).suffix
    return file_extension.lower() in [".sql", ".ddl"]


def make_dir(path: str | Path) -> None:
    """
    Creates a directory at the specified path if it does not already exist.

    :param path: The path where the directory should be created.
    """
    Path(path).mkdir(parents=True, exist_ok=True)


def dir_walk(root: Path):
    """
    Walks the directory tree rooted at the given path, yielding a tuple containing the root directory, a list of
    :param root: Path
    :return: tuple of  root, subdirectory , files
    """
    sub_dirs = [d for d in root.iterdir() if d.is_dir()]
    files = [f for f in root.iterdir() if f.is_file()]
    yield root, sub_dirs, files
    for s in sub_dirs:
        yield from dir_walk(s)
