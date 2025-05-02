import logging
from pathlib import Path
import subprocess
import shutil


def install_launch_agent():
    # Ensure that the User's `LaunchAgents` dir exists
    launch_agents_dir = Path.home() / Path("Library/LaunchAgents")
    launch_agents_dir.mkdir(parents=True, exist_ok=True)
    plist_path = launch_agents_dir / "com.remorph.usagecollection.plist"

    # Ensure that the scheduler script exits too
    scheduler_path = Path(__file__).parent.parent.parent / "pipeline_scheduler.py"
    if not scheduler_path.exists():
        raise FileNotFoundError(f"Could not find the profiler scheduler: {scheduler_path}")

    # Check if the profiler scheduler has been previously registered
    if plist_path.exists():
        logging.info("Plist exists already. Unloading.")
        subprocess.run(["launchctl", "unload", str(plist_path)], check=False)
    else:
        logging.info("Plist does not exist. Copying template to LaunchAgents dir.")
        # copy the plist file to the launch agents dir
        shutil.copy2("com.remorph.usagecollection.plist", plist_path)

    # TODO: Update plist file

    # Register the profiler scheduler
    subprocess.run(["launchctl", "load", str(plist_path)], check=True)
    logging.info("Loaded LaunchAgent com.remorph.usagecollection.plist successfully.")


def main():
    logging.info("Installing MacOS scheduler components...\n")
    install_launch_agent()
    logging.info("Installation complete.")


if __name__ == "__main__":
    main()
