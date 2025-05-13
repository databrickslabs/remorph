import platform
from subprocess import run, CalledProcessError

import json
import logging


def launch_uninstaller():

    logging.info("Creating virtual environment.")

    try:
        # Detect the host operating system and execute the appropriate script
        system = platform.system()
        if system == "Darwin":
            uninstaller_path = "macos/uninstall_launch_agent.py"
        elif system == "Linux":
            uninstaller_path = "linux/uninstall_service_file.py"
        elif system == "Windows":
            uninstaller_path = "windows\\uninstall_task_file.py"
        else:
            raise RuntimeError(f"Unsupported operating system: {system}")

        logging.info(f"Running remorph profiler uninstaller for: {system}")

        result = run(
            ["python", uninstaller_path],
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
    logging.info("Uninstalling the remorph profiler...\n")
    launch_uninstaller()
    logging.info("Uninstallation complete.")


if __name__ == "__main__":
    main()
