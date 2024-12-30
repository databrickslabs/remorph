# Contributing

## First Principles

Favoring standard libraries over external dependencies, especially in specific contexts like Databricks,
is a best practice in software development.

There are several reasons why this approach is encouraged:
- Standard libraries are typically well-vetted, thoroughly tested, and maintained by the official maintainers of the programming language or platform. This ensures a higher level of stability and reliability.
- External dependencies, especially lesser-known or unmaintained ones, can introduce bugs, security vulnerabilities, or compatibility issues  that can be challenging to resolve. Adding external dependencies increases the complexity of your codebase.
- Each dependency may have its own set of dependencies, potentially leading to a complex web of dependencies that can be difficult to manage. This complexity can lead to maintenance challenges, increased risk, and longer build times.
- External dependencies can pose security risks. If a library or package has known security vulnerabilities and is widely used, it becomes an attractive target for attackers. Minimizing external dependencies reduces the potential attack surface and makes it easier to keep your code secure.
- Relying on standard libraries enhances code portability. It ensures your code can run on different platforms and environments without being tightly coupled to specific external dependencies. This is particularly important in settings like Databricks, where you may need to run your code on different clusters or setups.
- External dependencies may have their versioning schemes and compatibility issues. When using standard libraries, you have more control over versioning and can avoid conflicts between different dependencies in your project.
- Fewer external dependencies mean faster build and deployment times. Downloading, installing, and managing external packages can slow down these processes, especially in large-scale projects or distributed computing environments like Databricks.
- External dependencies can be abandoned or go unmaintained over time. This can lead to situations where your project relies on outdated or unsupported code. When you depend on standard libraries, you have confidence that the core functionality you rely on will continue to be maintained and improved.

While minimizing external dependencies is essential, exceptions can be made case-by-case. There are situations where external dependencies are
justified, such as when a well-established and actively maintained library provides significant benefits, like time savings, performance improvements,
or specialized functionality unavailable in standard libraries.

## GPG signing
The Remorph project requires any commit to be signed-off using GPG signing.
Before you submit any commit, please make sure you are properly setup, as follows.

If you don't already have one, create a GPG key:
 - on MacOS, install the GPG Suite from https://gpgtools.org/
 - from the Applications folder, launch the GPG Keychain app
 - create a new GPG key, using your Databricks email
 - Right-click on the created key and select Export, to save the key
 - Check the key using TextEdit, it should start with -----BEGIN PGP PUBLIC KEY BLOCK-----

Register your PGP key in GitHub:
 - In GitHub, select Settings from your picture at the top-right
   - select SSH and PGP key
     - click on New key, and paste the text content of the exported key
   - select Emails
     - if your databricks email is not registered, register it
     - complete the verification before the next steps

Tell local git to signoff your commits using your PGP key
    - see full instructions here https://docs.github.com/en/authentication/managing-commit-signature-verification/telling-git-about-your-signing-key
    - in short, you need to run the following commands from a terminal:
        - git config --global --unset gpg.format
        - gpg --list-secret-keys --keyid-format=long
        - git config --global user.signingkey <KEY.ID.FROM.ABOVE>
        - git config --global commit.gpgsign true

Once all this is done, you can verify it's correct as follows:
    - create a branch and use it
    - create a file <FILENAME> with some content
    - git add <FILENAME>
    - git commit -m "test PGP"
    - git verify-commit <COMMIT>
The last command should display something like the following:
`gpg: Signature made Tue Nov 26 11:34:23 2024 CET
gpg:                using RSA key FD4D754BB2B1D4F09F2BF658F4B0C73DFC65A17B
gpg: Good signature from "GitHub <your.email@databricks.com>" [ultimate]
`

## Change management

When you introduce a change in the code, specifically a deeply technical one, please ensure that the change provides same or improved set of capabilities.
PRs that remove existing functionality shall be properly discussed and justified.

## Code Organization

When writing code, divide it into two main parts: **Components for API Interaction** and **Components for Business Logic**.
API Interaction should only deal with talking to external systems through APIs. They are usually integration-tested, and mocks are simpler.
Business Logic handles the actual logic of your application, like calculations, data processing, and decision-making.

_Keep API components simple._ In the components responsible for API interactions, try to keep things as straightforward as possible.
Refrain from overloading them with complex logic; instead, focus on making API calls and handling the data from those calls.

_Inject Business Logic._ If you need to use business logic in your API-calling components, don't build it directly there.
Instead, inject (or pass in) the business logic components into your API components. This way, you can keep your API components
clean and flexible, while the business logic remains separate and reusable.

_Test your Business Logic._ It's essential to test your business logic to ensure it works correctly and thoroughly. When writing
unit tests, avoid making actual API calls - unit tests are executed for every pull request, and **_take seconds to complete_**.
For calling any external services, including Databricks Connect, Databricks Platform, or even Apache Spark, unit tests have
to use "mocks" or fake versions of the APIs to simulate their behavior. This makes testing your code more manageable and catching any
issues without relying on external systems. Focus on testing the edge cases of the logic, especially the scenarios where
things may fail. See [this example](https://github.com/databricks/databricks-sdk-py/pull/295) as a reference of an extensive
unit test coverage suite and the clear difference between _unit tests_ and _integration tests_.

## JVM Proxy

In order to use this, you have to install `remorph` on any workspace via `databricks labs install .`,
so that `.databricks-login.json` file gets created with the following contents:

```
{
  "workspace_profile": "labs-azure-tool",
  "cluster_id": "0708-200540-wcwi4i9e"
}
```

then run `make dev-cli` to collect classpath information. And then invoke commands,
like `databricks labs remorph debug-script --name file`. Add `--debug` flag to recompile project each run.

Example output is:
```text
databricks labs remorph debug-script --name foo
21:57:42  INFO [databricks.sdk] Using Azure CLI authentication with AAD tokens
21:57:42  WARN [databricks.sdk] azure_workspace_resource_id field not provided. It is recommended to specify this field in the Databricks configuration to avoid authentication errors.
Debugging script...
Map(log_level -> disabled, name -> foo)
```

## Local Setup

This section provides a step-by-step guide to set up and start working on the project. These steps will help you set up your project environment and dependencies for efficient development.

To begin, install prerequisites:

`wget` is required by the maven installer
```shell
brew install wget
```

`maven` is the dependency manager for JVM based languages
```shell
brew install maven
```

`jdk11` is the jdk used by remorph
download it from [OpenJDK11](https://www.openlogic.com/openjdk-downloads?field_java_parent_version_target_id=406&field_operating_system_target_id=431&field_architecture_target_id=391&field_java_package_target_id=396) and install it


`python` is the runtime lamguage for remorph
```shell
brew install python
```

`hatch` is a Python project manager
```shell
pip install hatch
```

Then run project-specific install scripts

`make dev` creates the default environment and installs development dependencies, assuming you've already cloned the github repo.
```shell
make dev
```

Verify installation with
```shell
make test
```

To ensure your integrated development environment (IDE) uses the newly created virtual environment, you can retrieve the Python path with this command:
```shell
hatch run python -c "import sys; print(sys.executable)"
```

As of writing, we only support IntelliJ IDEA CE 2024.1. Development using more recent versions doesn't work (yet!).
Download and install [IntelliJ IDEA](https://www.jetbrains.com/idea/download/other.html)

Configure your IDE to:
 - use OpenJDK11 as the SDK for the project
 - install the IntelliJ Scala plugin version 2024.1.25. Do not use more recent versions, they don't work!!!
 - use this Python venv path so that you work within the virtual environment when developing the project:
![IDE Setup](docs/img/remorph_intellij.gif)

Before every commit, apply the consistent formatting of the code, as we want our codebase look consistent:
```shell
make fmt
```

Before every commit, run automated bug detector (`make lint`) and unit tests (`make test`) to ensure that automated
pull request checks do pass, before your code is reviewed by others:
```shell
make lint test
```

## IDE plugins

If you will be working with the ANTLR grammars, then you should install the ANTLR plugin for your IDE. There
is a plugin for VS Code, but it does not have as many checks as the one for IntelliJ IDEA.

While the ANTLR tool run at build time, will warn (and the build will stop on warnings) about things like
tokens that are used in the parser grammar but not defined in the lexer grammar, the IntelliJ IDEA plugin
provides a few extra tools such as identifying unused rules, and providing a visual representation of trees
etc.

Please read the documentation for the plugin so that you can make the most of it and have it generate
the lexer and parser in a temp directory to tell you about things like undefined tokens etc.

If you intended to make changes to the ANTLR defined syntax, please read teh README.md under ./core before
doing so. Changes to ANTLR grammars can have a big knock on effects on the rest of the codebase, and must
be carefully reviewed and tested - all the way from parse to code generation. Such changes are generally
not suited to beginners.

## First contribution

Here are the example steps to submit your first contribution:

1. Make a Fork from remorph repo (if you really want to contribute)
2. `git clone`
3. `git checkout main` (or `gcm` if you're using [ohmyzsh](https://ohmyz.sh/)).
4. `git pull` (or `gl` if you're using [ohmyzsh](https://ohmyz.sh/)).
5. `git checkout -b FEATURENAME` (or `gcb FEATURENAME` if you're using [ohmyzsh](https://ohmyz.sh/)).
6. .. do the work
7. `make fmt`
8. `make lint`
9. .. fix if any
10. `make test`
11. .. fix if any
12. `git commit -a`. Make sure to enter meaningful commit message title.
13. `git push origin FEATURENAME`
14. Go to GitHub UI and create PR. Alternatively, `gh pr create` (if you have [GitHub CLI](https://cli.github.com/) installed).
    Use a meaningful pull request title because it'll appear in the release notes. Use `Resolves #NUMBER` in pull
    request description to [automatically link it](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/using-keywords-in-issues-and-pull-requests#linking-a-pull-request-to-an-issue)
    to an existing issue.
15. announce PR for the review

## Troubleshooting

If you encounter any package dependency errors after `git pull`, run `make clean`
