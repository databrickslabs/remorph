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


def main():
    # Prerequisites:
    # The user has already cloned the remorph project and is executing the `install.py` script
    # So we can skip cloning the remorph project
    # The user must be using a Mac, Linux, or Windows OS
    # Python 3.11+ must be installed
    logging.info("Installing the remorph EDW profiler...\n")
    launch_installer()
    logging.info("Installation complete.")


if __name__ == "__main__":
    main()
