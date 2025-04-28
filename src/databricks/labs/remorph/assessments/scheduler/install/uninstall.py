import platform
from pathlib import Path
from subprocess import run, CalledProcessError

import venv
import tempfile
import json
import logging


def launch_uninstaller():

    logging.info("Creating virtual environment.")

    # Create a temporary directory for the virtual environment
    with tempfile.TemporaryDirectory() as temp_dir:
        venv_dir = Path(temp_dir) / "profiler_venv"
        builder = venv.EnvBuilder(with_pip=True)
        builder.create(venv_dir)
        venv_python = Path(venv_dir) / "bin" / "python"
        logging.info("Venv setup complete.")

        # Execute the Python script using the virtual environment's Python interpreter
        try:
            # Detect the host operating system and execute the appropriate script
            system = platform.system()
            if system == "Darwin":
                installer_path = "macos/uninstall_launch_agent.py"
            elif system == "Linux":
                installer_path = "linux/uninstall_service_file.py"
            elif system == "Windows":
                installer_path = "windows/uninstall_task_file.py"
            else:
                raise RuntimeError(f"Unsupported operating system: {system}")

            logging.info(f"Running scheduler uninstaller for: {system}")
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
    logging.info("Uninstalling the remorph EDW profiler scheduler...\n")
    launch_uninstaller()
    logging.info("Uninstallation complete.")


if __name__ == "__main__":
    main()
