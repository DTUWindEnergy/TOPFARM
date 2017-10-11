#!/bin/bash

ROOT=$(pwd)

echo 'INSTALL OPENMDAO'
mkdir $ROOT/topfarmv
mkdir $ROOT/topfarmv/src
SRC=$ROOT/topfarmv/src

pip install numpy scipy

cd $SRC
curl http://openmdao.org/releases/0.10.3.2/go-openmdao-0.10.3.2.py | python2
ln -s $SRC/openmdao-0.10.3.2/bin/activate $ROOT/topfarmv/activate
. $ROOT/topfarmv/activate

cd $SRC
echo 'INSTALL FUSED-Wake'
git clone http://www.github.com/DTUWindEnergy/FUSED-Wake.git
cd $SRC/FUSED-Wake/gclarsen
python setup.py install

cd $SRC/FUSED-Wake/py4we
python setup.py install

cd $SRC
echo 'INSTALL FUSED-Wind + TOPFARM'
pip install -r http://raw.githubusercontent.com/DTUWindEnergy/TOPFARM/master/remote_install.txt

echo "Did something go wrong in the installation process? Then post an issue about it on https://github.com/DTUWindEnergy/TOPFARM/issues"

echo FUSED-Wind has been installed in editable mode in $ROOT/topfarmv/src/fusedwind
echo FUSED-Wake has been installed in editable mode in $ROOT/topfarmv/src/fusedwake
echo TOPFARM has been installed in editable mode in $ROOT/topfarmv/src/topfarm

echo 'To use TOPFARM you first need to activate the virtual environment:'
echo '. $ROOT/topfarmv/activate'
ln -s  $SRC/openmdao-0.10.3.2/src/* $SRC/ 
cd $ROOT

