import codecs
import os


# Optionally check to see if a string begins with a Byte Order Mark
# such a character will cause the transpiler to fail
def remove_bom(input_string):
    # Check and remove UTF-8 BOM
    if input_string.startswith(codecs.BOM_UTF8.decode("utf-8")):
        return input_string[len(codecs.BOM_UTF8.decode("utf-8")) :]

    # Check and remove UTF-16 (LE and BE) BOM
    elif input_string.startswith(codecs.BOM_UTF16_LE.decode("utf-16")):
        return input_string[len(codecs.BOM_UTF16_LE.decode("utf-16")) :]
    elif input_string.startswith(codecs.BOM_UTF16_BE.decode("utf-16")):
        return input_string[len(codecs.BOM_UTF16_BE.decode("utf-16")) :]

    # Check and remove UTF-32 (LE and BE) BOM
    elif input_string.startswith(codecs.BOM_UTF32_LE.decode("utf-32")):
        return input_string[len(codecs.BOM_UTF32_LE.decode("utf-32")) :]
    elif input_string.startswith(codecs.BOM_UTF32_BE.decode("utf-32")):
        return input_string[len(codecs.BOM_UTF32_BE.decode("utf-32")) :]

    return input_string


def is_sql_file(file):
    """
    Checks if the given file is a SQL file.

    :param file: The name of the file to check.
    :return: True if the file is a SQL file (i.e., its extension is either .sql or .ddl), False otherwise.
    """
    _, file_extension = os.path.splitext(file)
    return file_extension.lower() in [".sql", ".ddl"]


def make_dir(path):
    """
    Creates a directory at the specified path if it does not already exist.

    :param path: The path where the directory should be created.
    """
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
