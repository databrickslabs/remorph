import platform
from subprocess import run, CalledProcessError

import json
import logging


def launch_installer():

    try:
        # Detect the host operating system and execute the appropriate script
        system = platform.system()
        if system == "Windows":
            installer_path = "windows\\install_task_file.py"
        else:
            raise RuntimeError(f"Unsupported operating system: {system}")

        logging.info(f"Running profiler installer for: {system}")
        result = run(
            ["python", installer_path],
            check=True,
            capture_output=True,
            text=True,
        )

        try:
            output = json.loads(result.stdout)
            logging.debug(output)
            if output["status"] == "success":
                logging.info(f"Python script completed: {output['message']}")
            else:
                raise RuntimeError(f"Script reported error: {output['message']}")
        except json.JSONDecodeError:
            logging.error(f"Python script output: {result.stdout}")

    except CalledProcessError as e:
        error_msg = e.stderr
        logging.error(f"Installation script failed: {error_msg}")
        raise RuntimeError(f"Installation script failed: {error_msg}") from e


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
    Validates if schtasks is installed on the host.
    Returns:
        bool - True if schtasks is installed
               False if schtasks not found on the system
    """
    try:
        # check is we can display the manual page for `schtasks`
        run(["SCHTASKS", "/?"], capture_output=True, check=True)
        return True
    except CalledProcessError as cpe:
        logging.error(f"Schtasks not found on the system: {cpe}")
        return False


def validate_prerequisites():
    """
    Validates that the prerequisites for installing the profiler
    are met.
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
    if system_info == "darwin" and not is_systemd_installed():
        raise RuntimeError("Systemd is required to install the remorph profiler.")
    if system_info == "windows" and not is_task_scheduler_installed():
        raise RuntimeError("Schtasks is required to install the remorph profiler.")


def main():
    logging.info("Installing the remorph profiler...\n")
    validate_prerequisites()
    launch_installer()
    logging.info("Installation complete.")


if __name__ == "__main__":
    main()
