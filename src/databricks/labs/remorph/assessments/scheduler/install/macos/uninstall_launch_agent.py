import logging
from pathlib import Path
import subprocess


def uninstall_launch_agent():
    launch_agents_dir = Path.home() / Path("Library/LaunchAgents")
    plist_path = launch_agents_dir / "com.remorph.usagecollection.plist"

    # Check if the profiler scheduler has been previously registered
    if plist_path.exists():
        logging.info("Plist exists. Unloading agent.")
        subprocess.run(["launchctl", "unload", str(plist_path)], check=False)
        plist_path.unlink()
        logging.info("Plist file removed from LaunchAgents dir.")


def main():
    logging.info("Uninstalling MacOS scheduler components...\n")
    uninstall_launch_agent()
    logging.info("Uninstallation complete.")


if __name__ == "__main__":
    main()
