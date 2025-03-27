# Installing the Usage Collection Scheduler

## Why do we need a usage collection scheduler?
- Some data warehouses do not preserve query history for longer than a few days or are limited to only a few rows. As an example, Amazon Redshift only preserves usage history for around 2-5 days
- Having adequate usage history is critical to provide an accurate Total Cost of Ownership (TCO) estimate
- Having too little history could produce an inaccurate representation of data warehouse query patterns and system utilization

## Supported operating systems
The usage collection scheduler can be installed on the following operating systems:

1. MacOS
2. Linux

## Local vs. Remote Deployments

The usage collection scheduler can be executed in the following deployments:

1. **Local scheduler** - Scheduler is installed on a local laptop or workstation, provided that the local system can connect to a bastion host and forward connectivity to the data warehouse
2. **Remote scheduler** - Scheduler is installed directly on a bastion host in a separate subnet or a compute instance deployed within the data warehouse's subnet


## Automatic restart 

The usage collection scheduler utilizes the host operating system to run as a background process. As a result, the process will automatically resume processing after a system restart; no intervention is needed during a host system restart. The scheduler will automatically detect usage history gaps and proactively backfill when possible.
