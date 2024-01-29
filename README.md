Databricks Labs Remorph
---
![Databricks Labs Remorph](docs/remorph-logo.svg)

-----

# Table of Contents

1. [Introduction](#introduction)
   - [Remorph](#remorph)
   - [Transpile](#transpile)
2. [Environment Setup](#environment-setup)
3. [How to use Transpile](#how-to-use-transpile)
4. [Project Support](#project-support)

----
# Introduction

## Remorph
Remorph stands as a comprehensive toolkit meticulously crafted to facilitate seamless migrations to Databricks. 
This suite of tools is dedicated to simplifying and optimizing the entire migration process, offering two distinctive functionalities – Transpile and Reconcile. Whether you are navigating code translation or resolving potential conflicts, Remorph ensures a smooth journey for any migration project. With Remorph as your trusted ally, 
the migration experience becomes not only efficient but also well-managed, setting the stage for a successful transition to the Databricks platform.

## Transpile
Transpile is a self-contained SQL parser, transpiler, and validator designed to interpret a diverse range of SQL inputs and generate syntactically and semantically correct SQL in the Databricks SQL dialect. This tool serves as an automated solution, named Transpile, specifically crafted for migrating and translating SQL scripts from various sources to the Databricks SQL format. Currently, it exclusively supports Snowflake as a source platform, leveraging the open-source SQLglot.

Transpile stands out as a comprehensive and versatile SQL transpiler, boasting a robust test suite to ensure reliability. Developed entirely in Python, it not only demonstrates high performance but also highlights syntax errors and provides warnings or raises alerts for dialect incompatibilities based on configurations.

#### Design Flow:
```mermaid
flowchart TD
    A(Transpile CLI) --> |Directory| B[Transpile All Files In Directory];
    A --> |File| C[Transpile Single File] ;
    B --> D[List Files];
    C --> E("Sqlglot(transpile)");
    D --> E
    E --> |Parse Error| F(Failed Queries)
    E --> G{Skip Validations}
    G --> |Yes| H(Save Output)
    G --> |No| I{Validate}
    I --> |Success| H
    I --> |Fail| J(Flag, Capture)
    J --> H
```

----

# Environment Setup

1. `Databricks CLI` - Ensure that you have the Databricks Command-Line Interface (CLI) installed on your machine. Refer to the installation instructions provided for Linux, MacOS, and Windows, available [here](https://docs.databricks.com/en/dev-tools/cli/install.html#install-or-update-the-databricks-cli).

2. `Databricks Connect` - Set up the Databricks workspace configuration file by following the instructions provided [here](https://docs.databricks.com/en/dev-tools/auth/index.html#databricks-configuration-profiles). Note that Databricks labs use 'DEFAULT' as the default profile for establishing connections to Databricks.
   
3. `Python` - Verify that your machine has Python version 3.10 or later installed to meet the required dependencies for seamless operation.
   - `Windows` - Install python from [here](https://www.python.org/downloads/). Your Windows computer will need a shell environment ([GitBash](https://www.git-scm.com/downloads) or [WSL](https://learn.microsoft.com/en-us/windows/wsl/about))
   - `MacOS/Unix` - Use [brew](https://formulae.brew.sh/formula/python@3.10) to install python in macOS/Unix machines
#### Installing Databricks CLI on macOS
![macos-databricks-cli-install](docs/macos-databricks-cli-install.gif)

#### Install Databricks CLI via curl on Windows
![windows-databricks-cli-install](docs/windows-databricks-cli-install.gif)

#### Check Python version on Windows, macOS, and Unix

![check-python-version](docs/check-python-version.gif)

----

# How to Use Transpile

## Step 1 : Installation

Upon completing the environment setup, install Remorph by executing the following command:
```bash
databricks labs install remorph
```

Verify the successful installation by executing the provided command; confirmation of a successful installation is indicated when the displayed output aligns with the example screenshot provided:
```bash
 databricks labs remorph transpile --help
 ```
![transpile-help](docs/transpile-help.png)

## Step 2 : Set Up Prerequisite File
1. Transpile necessitates input in the form of either a directory containing SQL files or a single SQL file. 
2. The SQL file should encompass scripts intended for migration to Databricks SQL.

Below is the detailed explanation on the arguments required for Transpile.
- `input-sql [Required]` - The path to the SQL file or directory containing SQL files to be transpiled.
- `source [Required]` - The source platform of the SQL scripts. Currently, only Snowflake is supported.
- `output-folder [Optional]` - The path to the output folder where the transpiled SQL files will be stored. If not specified, the transpiled SQL files will be stored in the same directory as the input SQL file.
- `skip-validation [Optional]` - The default value is True. If set to False, the transpiler will validate the transpiled SQL scripts against the Databricks catalog and schema provided by user.
- `catalog-name [Optional]` - The name of the catalog in Databricks. If not specified, the default catalog `transpiler_test` will be used.
- `schema-name [Optional]` - The name of the schema in Databricks. If not specified, the default schema `convertor_test` will be used.

## Step 3 : Execution
Execute the below command to intialize the transpile process.
```bash
 databricks labs  remorph transpile --input-sql <absolute-path> --source <snowflake> --output-folder <absolute-path> --skip-validation <True|False> --catalog-name <catalog name> --schema-name <schema name>
```

----

# Project Support
Please note that all projects in the /databrickslabs github account are provided for your exploration only, and are not formally supported by Databricks with Service Level Agreements (SLAs).  They are provided AS-IS and we do not make any guarantees of any kind.  Please do not submit a support ticket relating to any issues arising from the use of these projects.

Any issues discovered through the use of this project should be filed as GitHub Issues on the Repo.  They will be reviewed as time permits, but there are no formal SLAs for support.
