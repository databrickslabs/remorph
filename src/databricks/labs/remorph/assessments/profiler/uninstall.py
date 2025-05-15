import platform
from subprocess import run, CalledProcessError

import logging


USAGE_COLLECTION_TASK_NAME = "Remorph Usage Collection"


def is_windows_task_scheduled():
    """
    Queries the status of the usage collection status.
    Returns:
        True - if schtasks returns a positive status code
        False - if schtasks throws an exception if the task was not found.
    """
    try:
        logging.info("Checking if task exists.")
        run(["SCHTASKS", "/QUERY", "/TN", USAGE_COLLECTION_TASK_NAME], check=True)
        return True
    except CalledProcessError as e:
        error_msg = e.stderr
        logging.error(f"Failed to query scheduled usage collection task: {error_msg}")
        return False


def delete_windows_task():
    """
    Removes the usage collection task from schtasks
    """
    logging.info("Deleting scheduled task from the task manager.")
    if is_windows_task_scheduled():
        try:
            run(["SCHTASKS", "/DELETE", "/TN", USAGE_COLLECTION_TASK_NAME, "/F"], check=True)
        except CalledProcessError as e:
            error_msg = e.stderr
            raise RuntimeError(f"Failed to delete the usage collection task for Windows: {error_msg}") from e


def launch_uninstaller():
    """
    Removes the scheduled usage collection task from the system task scheduler.
    """
    system = platform.system()
    logging.info(f"Running remorph profiler uninstaller for: {system}")
    if system == "Windows":
        try:
            delete_windows_task()
        except RuntimeError as e:
            logging.error(f"Failed to delete the usage collection task for Windows: {e}")
            raise RuntimeError(f'Failed to delete the usage collection task for Windows: {e}') from e
    else:
        raise RuntimeError(f"Unsupported operating system: {system}")


def main():
    logging.info("Uninstalling the remorph profiler...\n")
    launch_uninstaller()
    logging.info("Uninstallation complete.")


if __name__ == "__main__":
    main()
