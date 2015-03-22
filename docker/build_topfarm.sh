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

### Installing DAKOTA driver


### Installing Ipopt
cd $INSTALL_DIR
git clone -branch stable/3.12 https://github.com/coin-or/Ipopt.git
cd Ipopt
cd ThirdParty/Metis
./get-Metis
cd ..
cd Mumps
./get-Mumps
cd ..
./configure --prefix=/usr/local
make
make install

### Installing the pyipopt
cd $INSTALL_DIR
git clone https://github.com/xuy/pyipopt.git
cd pyipopt

# Fix dependencies from docker_openmdao is deleting the tornado and ipython and replacing it with the new ones
# It also calls `pip install -r requirements.txt`
$INSTALL_DIR/fix_dependencies.sh

echo 'export $LD_LIBRARY_PATH=/usr/local/lib'>>/home/fusedwind/.bashrc
echo 'export $LD_LIBRARY_PATH=/usr/local/lib'>>/root/.bashrc
