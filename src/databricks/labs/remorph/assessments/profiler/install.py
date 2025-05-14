import platform
from subprocess import run, CalledProcessError
from pathlib import Path

import logging
import getpass


USAGE_COLLECTION_TASK_NAME = "Remorph Usage Collection"


def schedule_windows_task():
    """
    Schedules the profiler usage collection task to execute using schtasks.
    """
    pipeline_scheduler_path = f"{Path.cwd().parent}\\pipeline_scheduler.py"
    usage_collection_command = f"python {pipeline_scheduler_path}"
    logging.info(f"Scheduling usage collection task: {usage_collection_command}")
    try:
        run(
            [
                "SCHTASKS",
                "/CREATE",
                "/TN",
                USAGE_COLLECTION_TASK_NAME,
                "/TR",
                usage_collection_command,
                "/SC",
                "MINUTE",
                "/MO",
                "15",  # TODO: Make this configurable
                "/RL",
                "HIGHEST",
                "/F",
                "/RU",
                getpass.getuser(),
            ],
            check=True,
            text=True,
        )
    except CalledProcessError as e:
        error_msg = e.stderr
        raise RuntimeError(f"Failed to schedule the usage collection task for Windows: {error_msg}") from e


def launch_installer():
    """
    Schedules usage collection task using the hosts system scheduler.
    """
    system = platform.system()
    logging.info(f"Running profiler installer for: {system}")
    if system == "Windows":
        try:
            schedule_windows_task()
        except RuntimeError as e:
            logging.error(f"Failed to schedule the usage collection task for Windows: {e}")
            raise RuntimeError(f"Failed to schedule the usage collection task for Windows: {e}") from e
    else:
        raise RuntimeError(f"Unsupported operating system: {system}")


def is_systemd_installed() -> bool:
    """
    Validates if systemd is installed on the host.
    Returns:
        bool - True if systemd is installed
               False if systemd not found on the system
    """
    try:
        run(["systemctl", "-version"], capture_output=True, check=True)
        return True
    except CalledProcessError as cpe:
        logging.error(f"Systemd not found on the system: {cpe}")
        return False


def is_task_scheduler_installed() -> bool:
    """
    Validates if the schtasks command is installed on the host.
    Returns:
        bool - True if schtasks is installed
               False if schtasks not found on the system
    """
    try:
        # Check if the manual page for `schtasks` can be displayed
        run(["SCHTASKS", "/?"], capture_output=True, check=True)
        return True
    except CalledProcessError as cpe:
        logging.error(f"Schtasks not found on the system: {cpe}")
        return False


def validate_system_requirements():
    """
    Validates the system requirements for installing the profiler are met:
    1. The user must be using a Mac, Linux, or Windows OS
    2. Python 3.10+ must be installed
    3. System scheduler must be callable, e.g. systemd, launchmd, schtasks
    """
    logging.info("Validating system requirements.")
    logging.info("Checking operating system.")
    system_info = platform.system().lower()
    if platform.system().lower() not in {"darwin", "linux", "windows"}:
        raise RuntimeError("Unsupported operating system detected.")
    logging.info("Checking Python version.")
    python_version_info = [int(v) for v in platform.python_version().split(".")]
    if python_version_info[0] != 3 or python_version_info[1] < 10:
        raise RuntimeError("Python version must be >= Python 3.10")
    logging.info("Checking system scheduler.")
    if system_info == "windows" and not is_task_scheduler_installed():
        raise RuntimeError("Schtasks is required to install the remorph profiler.")


def main():
    logging.info("Installing the remorph profiler...\n")
    validate_system_requirements()
    launch_installer()
    logging.info("Installation complete.")


if __name__ == "__main__":
    main()
