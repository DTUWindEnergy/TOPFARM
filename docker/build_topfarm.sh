#!/bin/bash
# function: build topfarm
# needs to be called with the command:
# bash -c "source $OPENMDAODIR/bin/activate; build_topfarm.sh"

cd $INSTALL_DIR
git clone http://github.com/DTUWindEnergy/FUSED-Wake.git
cd $INSTALL_DIR/FUSED-Wake/gclarsen
omdao python setup.py install
cd $INSTALL_DIR/FUSED-Wake/py4we
omdao python setup.py install

### Installing DAKOTA driver


### Installing Ipopt
cd $INSTALL_DIR
wget http://www.coin-or.org/download/source/Ipopt/Ipopt-3.12.1.tgz
tar xvf Ipopt-3.12.1.tgz
cd Ipopt-3.12.1
cd ThirdParty/Metis
./get.Metis
cd ..
cd Mumps
./get.Mumps
cd ../..
./configure --prefix=/usr/local
make
make install

# Fix dependencies from docker_openmdao is deleting the tornado and ipython and replacing it with the new ones
# It also calls `pip install -r requirements.txt`
omdao $INSTALL_DIR/fix_dependencies.sh

touch /root/.bashrc
touch /home/fusedwind/.bashrc
echo 'export $LD_LIBRARY_PATH=/usr/local/lib'>>/home/fusedwind/.bashrc
echo 'export $LD_LIBRARY_PATH=/usr/local/lib'>>/root/.bashrc
