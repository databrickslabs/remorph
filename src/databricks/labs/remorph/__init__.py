from databricks.labs.remorph.reconcile.cli import entry_point as reconcile
from databricks.labs.remorph.transpiler.cli import entry_point as transpile

if __name__ == "__main__":
    transpile()
    reconcile()
