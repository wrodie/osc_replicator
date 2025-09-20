import sys
import os
import subprocess

def main():
    # Find the python executable (venv or system)
    python = sys.executable
    # Build the command to run the package as a module
    cmd = [python, "-m", "osc_replicator_pkg"] + sys.argv[1:]
    # Run from the parent directory of osc_replicator
    parent = os.path.dirname(os.path.abspath(__file__))
    result = subprocess.run(cmd, cwd=parent)
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
