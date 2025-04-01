# (MacOS) Installing the Usage Collection Scheduler

## Installation Steps:

1. Open a new Terminal window

2. Copy the plist file to `~/Library/LaunchAgents/` for a user-specific task or `/Library/LaunchDaemons/` for a system-wide task:

```bash 
$ cp ~/Downloads/remorph/scheduler/macos/com.remorph.usagecollection.plist ~/Library/LaunchAgents/
```

3. Next, load the process by executing the following command:

```bash
$ launchctl load ~/Library/LaunchAgents/com.remorph.usagecollection.plist
```

4. Grant the usage collection script with execution permissions:

```bash
$ chmod +x ~/Downloads/remorph/scheduler/usage_collector.py
```

## Description of the `plist` Elements

1. **Label**: A unique identifier for the job

2. **ProgramArguments**: Specifies the command and arguments (python3 interpreter and the script path)

3. **StartInterval**: Runs the script every 900 seconds (15 minutes)

4. **RunAtLoad**: Ensures the script runs immediately after loading

5. **StandardOutPath**: Logs output to `~/Downloads/remorph/scheduler/stdout` for debugging

6. **StandardErrorPath**: Logs errors to `~/Downloads/remorph/scheduler/stderr` for debugging
