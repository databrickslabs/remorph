Remorph _pluggable_ transpilers
---

`Remorph` transpiles source code using _pluggable_ transpilers.
They are pluggable in the sense that:
 - their code sits outside of the `remorph` code base
 - there can be more than 1 installed, although as of writing, `remorph` can only use 1 at a given point in time
 - `remorph` knows nothing about them until they are discovered at runtime

Communication between `remorph` and a transpiler is achieved using `LSP`, see for example [this starter](https://github.com/databrickslabs/remorph-plugin-starters/tree/python-sdk/python) to learn more about how this works.

This document describes how `remorph` discovers and runs transpilers.

Although one could _in theory_ run a transpiler without access to the Databricks platform, `remorph` requires a valid Databricks install.
Remorph leverages this by expecting transpilers to reside in the `.databricks` folder hierarchy, as follows:

&#x002E;\
&#x251C;&#x2500;.Databricks/\
&#x2502;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&#x251C;&#x2500;labs/\
&#x2502;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&#x251C;&#x2500;remorph-transpilers/\
&#x2502;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&#x251C;&#x2500;some-transpiler/\
&#x2502;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&#x251C;&#x2500;other-transpiler/\
&#x2502;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&#x251C;&#x2500;my-transpiler/



Each transpiler resides in its own dedicated sub-directory, whose name can be anything (although avoiding spaces is recommended). It itself comprises 2 folders:

&#x002E;\
&#x251C;&#x2500;.lib/\
&#x2502;&nbsp;&nbsp;&nbsp;&nbsp;&#x251C;&#x2500;.config.yml\
&#x2502;&nbsp;&nbsp;&nbsp;&nbsp;&#x251C;&#x2500;.&lt;transpiler code&gt;\
&#x251C;&#x2500;.state/\
&#x2502;&nbsp;&nbsp;&nbsp;&nbsp;&#x251C;&#x2500;.version.json\


A transpiler `lib` subdirectory _must_ comprise a `config.yml` file that follows the following structure:

```yaml
remorph:
  version: 1 # mandatory, _must_ equal 1
  name: <name of the transpiler> # mandatory, can be different from the folder name
  dialects: # this section is mandatory and cannot be empty
    - <sql dialect 1> # such as 'oracle' - it is recommended to leverage dialect names from sqlglot)
    - <sql dialect 2>
    - ...
    - <sql dialect _n_>
  environment: # this section is optional, variables are set prior to launching the transpiler
    - <name 1>: <value 1>
    - <name 2>: <value 2>
    - ...
    - <name _n_>: <value _n_>
  command_line: # this section is mandatory and cannot be empty, it is used to launch the transpiler
    - <executable> # such as 'java', or 'python'
    - <argument 1> # such as '-jar'
    - ...
    - <argument _n_>
custom: # this section is optional, it is passed to the transpiler at startup
    <key 1>: <value 1> # can be pretty much anything
```

Installing a transpiler is the responsibility of its transpiler. Databricks `remorph` installs 2 transpilers: _RCT_ (Remorph Community Transpiler) and _Morpheus_, its advanced transpiler.

When `remorph` is configured, it scans the `remorph-transpilers` directory, and collects available source dialects and corresponding transpilers, such that the user can configure them as wished.

When a user runs the _transpile_ command for the first time, `remorph` sets the working directory to the configured transpiler, appends the configured environment variables, and runs the configured command line.

The transpiler is an LSP Server i.e. it listens to commands from _remorph_ until it is instructed to exit.

---
Manually installing a transpiler
---

There are situations where an installer may fail: security rules preventing downloads, pre-releases...
Following the above steps,it is straightforward to manually install a transpiler, by:
 - creating the transpiler folder in the `.databricks/labs` directory
 - creating the `lib` and `state` sub-directories
 - creating a `config.yml` file in the lib directory (see details above)
 - creating a `version.json` file in the lib directory with content like:`
   ```{"version": f"v1.3.7", "date": "2025-03-17-15:02:31Z}```
