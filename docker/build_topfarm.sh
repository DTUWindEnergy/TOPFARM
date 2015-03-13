#!/bin/bash
# function: build topfarm
# needs to be called with the command:
# bash -c "source $OPENMDAODIR/bin/activate; build_topfarm.sh"

cd $INSTALL_DIR
git clone http://github.com/DTUWindEnergy/FUSED-Wake.git
cd $INSTALL_DIR/FUSED-Wake/gclarsen
python setup.py install
cd $INSTALL_DIR/FUSED-Wake/py4we
python setup.py install

pip install -r $INSTALL_DIR/requirements.txt
pip install tornado --upgrade
