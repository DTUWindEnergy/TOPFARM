#!/bin/bash
# Strict mode
set -euo pipefail
IFS=$'\n\t'


# Create the hash to pass to the IPython notebook, but don't export it so it doesn't appear
# as an environment variable within IPython kernels themselves
#HASH=$(python3 -c "from IPython.lib import passwd; print(passwd('${PASSWORD}'))")
HASH=$(python3 -c "from IPython.lib import passwd; print(passwd('topfarm'))")
unset PASSWORD

bash -c "source $OPENMDAODIR/bin/activate; ipython2 notebook --no-browser --port 8888 --ip=*  --NotebookApp.password='$HASH' --matplotlib=inline"
