#!/bin/bash


if [ ! -x "$(type -p virtualenv)" ]; then
    echo 'INSTALL Virtualenv'
    sudo easy_install virtualenv
fi

echo 'INSTALL own TOPFARM virtual environment'
virtualenv topfarmv
. topfarmv/bin/activate

pip install pip --upgrade
pip install numpy
pip install scipy

echo 'INSTALL OPENMDAO'
mkdir topfarmv/src
cd topfarmv/src
git clone https://github.com/OpenMDAO/OpenMDAO-Framework.git
cd OpenMDAO-Framework
git checkout 0.10.3.2
./go-openmdao-dev.py
cd ..

echo 'INSTALL FUSED-Wake'
git clone http://www.github.com/DTUWindEnergy/FUSED-Wake.git
cd FUSED-Wake/gclarsen
python setup.py install
cd ..
cd py4we
python setup.py install
cd ../../..


echo 'INSTALL FUSED-Wind + TOPFARM'
pip install -r http://raw.githubusercontent.com/DTUWindEnergy/TOPFARM/master/remote_install.txt

echo "Did something go wrong in the installation process? Then post an issue about it on https://github.com/DTUWindEnergy/TOPFARM/issues"

echo FUSED-Wind has been installed in editable mode in $(pwd)/topfarmv/src/fusedwind
echo FUSED-Wake has been installed in editable mode in $(pwd)/topfarmv/src/fusedwake
echo TOPFARM has been installed in editable mode in $(pwd)/topfarmv/src/topfarm

echo 'To use TOPFARM you first need to activate the virtual environment:'
echo '$ . topfarmv/bin/activate'


