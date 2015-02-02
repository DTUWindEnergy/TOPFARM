$!/bin/bash

mkdir install_prerequisits
cd install_prerequisits

echo 'INSTALL Virtualenv'
easy_install virtualenv
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
cd ..
git clone https://github.com/FUSED-Wind/fusedwind.git
cd fusedwind
git checkout v0.1.0
plugin install
cd ..

echo 'INSTALL FUSED-Wake'
git clone git@github.com:DTUWindEnergy/FUSED-Wake.git
cd FUSED-Wake
git checkout 0.1.0
plugin install
cd ..

echo 'INSTALL TOPFARM'
git clone git@github.com:DTUWindEnergy/TOPFARM.git
cd TOPFARM
plugin install