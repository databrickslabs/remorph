import platform
from pathlib import Path
from subprocess import run, CalledProcessError

import venv
import tempfile
import json
import logging

PROFILER_DEPENDENCIES: list[str] = []


def launch_installer():

    logging.info("Creating virtual environment.")

    # Build a virtual environment for launching installer
    with tempfile.TemporaryDirectory() as temp_dir:
        venv_dir = Path(temp_dir) / "profiler_venv"
        builder = venv.EnvBuilder(with_pip=True)
        builder.create(venv_dir)
        venv_python = Path(venv_dir) / "bin" / "python"
        venv_pip = Path(venv_dir) / "bin" / "pip"
        logging.info("Venv setup complete.")

        # Install dependencies in the virtual environment
        if len(PROFILER_DEPENDENCIES) > 0:
            logging.info(f"Installing dependencies: {', '.join(PROFILER_DEPENDENCIES)}")
            try:
                run([str(venv_pip), "install", *PROFILER_DEPENDENCIES], check=True, capture_output=True, text=True)
            except CalledProcessError as e:
                logging.error(f"Failed to install dependencies: {e.stderr}")
                raise RuntimeError(f"Failed to install dependencies: {e.stderr}") from e

        # Execute the Python script using the virtual environment's Python interpreter
        try:
            # Detect the host operating system and execute the appropriate script
            system = platform.system()
            if system == "Darwin":
                installer_path = "macos/install_launch_agent.py"
            elif system == "Linux":
                installer_path = "linux/install_service_file.py"
            elif system == "Windows":
                installer_path = "windows/install_service_file.py"
            else:
                raise RuntimeError(f"Unsupported operating system: {system}")

            logging.info(f"Running scheduler installer for: {system}")
            result = run(
                [str(venv_python), str(installer_path)],
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
                logging.info(f"Python script output: {result.stdout}")

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
        run(
            ["systemctl", "-version"],
            capture_output=True,
            check=True
        )
        return True
    except CalledProcessError as cpe:
        logging.error(f"Systemd not found on the system: {cpe}")
        return False


def validate_prerequisites():
    """
    Validates that the prerequisites for installing the profiler scheduler
    are met.
    1. The user must be using a Mac, Linux, or Windows OS
    2. Python 3.11+ must be installed
    """
    system_info = platform.system().lower()
    if platform.system().lower() not in {"darwin", "linux", "windows"}:
        raise RuntimeError("Unsupported operating system detected.")
    python_version_info = [int(v) for v in platform.python_version().split(".")]
    if python_version_info[0] != 3 or python_version_info[1] < 11:
        raise RuntimeError("Python version must be >= Python 3.11")
    if system_info == "darwin" and not is_systemd_installed():
        raise RuntimeError("Systemd is required.")


def main():
    logging.info("Installing the remorph profiler scheduler...\n")
    validate_prerequisites()
    launch_installer()
    logging.info("Installation complete.")


if __name__ == "__main__":
    main()
