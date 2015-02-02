#!/bin/bash

mkdir TOPFARM
cd TOPFARM

echo 'INSTALL Virtualenv'
sudo easy_install virtualenv

virtualenv topfarmv
. topfarmv/bin/activate
pip install numpy scipy

echo 'INSTALL OPENMDAO'
git clone https://github.com/OpenMDAO/OpenMDAO-Framework.git
cd OpenMDAO-Framework
git checkout 0.10.3
go-openmdao-dev.py
cd ..

echo 'INSTALL FUSED-Wind'
git clone https://github.com/FUSED-Wind/fusedwind.git
cd fusedwind
git checkout v0.1.0
plugin install
cd ..

echo 'INSTALL FUSED-Wake'
#git clone git@github.com:DTUWindEnergy/FUSED-Wake.git
#cd FUSED-Wake
#git checkout 0.1.0
#plugin install
#cd ..

echo 'INSTALL other pre-requisits'
pip install pandas matplotlib seaborn

echo 'INSTALL TOPFARM'
git clone git@github.com:DTUWindEnergy/TOPFARM.git
cd TOPFARM
plugin install
cd ..


echo 'To activate the virtual environment type:'
echo '$ . activate'
ln -s topfarmv/bin/activate .