# Unstable, not running yet....

--------


#TOPFARM

TOPFARM is a wind farm optimization tool under development by DTU Wind Energy, based on [FUSED-Wind](http://www.fusedwind.org) and [OpenMDAO](http://www.openmdao.org).


## Dependencies and supported Python versions

TOPFARM depends of on [OpenMDAO v0.10.3](https://github.com/OpenMDAO/OpenMDAO-Framework),
 [FUSED-Wind v0.1.0](https://github.com/fusedwind/fusedwind),
 [FUSED-Wake v0.1.0](https://github.com/DTUWindEnergy/FUSED-Wake), pandas, matplotlib, seaborn, [pyopt 1.2](http://pyopt.org)
  and supports python 2.7.x.


# Installation

## Automatic installation
If you are on Linux of MacOSX, you can try to [download](https://raw.githubusercontent.com/DTUWindEnergy/TOPFARM/master/install_all.sh)
 and run the following script to install everything, including OpenMDAO and FUSED-Wind in a new virtual environment

    $ wget https://raw.githubusercontent.com/DTUWindEnergy/TOPFARM/master/install_all.sh
    $ chmod +x install_all.sh
    $ ./install_all.sh

If you happen to have already OpenMDAO v0.10.3 installed and activated, you can install everything in one command line

    $ pip install -r http://raw.githubusercontent.com/DTUWindEnergy/TOPFARM/master/remote_install.txt
    

## Manual installation
### [Optional] Create your own TOPFARM virtual environment:
  
Install `virtualenv`, if you don't already have it available
 
    $ easy_install virtualenv
    
Then create a new virtual environement and activate it

    $ virtualenv topfarmv
    $ . topfarmv/bin/activate

Install the pre-requisits to OpenMDAO (pip probably needs to be upgraded to the latest version).

    $ pip install pip --upgrade 
    $ pip install numpy scipy

### Install OpenMDAO v0.10.3

Install [OpenMDAO development v0.10.3](https://github.com/OpenMDAO/OpenMDAO-Framework/tree/0.10.3).

    $ git clone https://github.com/OpenMDAO/OpenMDAO-Framework.git
    $ cd OpenMDAO-Framework
    $ git checkout 0.10.3.2  
    $ go-openmdao-dev.py
    
... coffee break ...

    $ cd ..

### Install FUSED-Wind and TOPFARM plugins and all their dependencies
    $ pip install pandas matplotlib seaborn
    $ pip install -e git+http://github.com/FUSED-Wind/fusedwind.git@0.1.0#egg=fusedwind
    $ pip install svn+http://svn.pyopt.org/tags/release-1.1.0#egg=pyopt
    $ pip install git+http://github.com/OpenMDAO-Plugins/pyopt_driver.git@0.19#egg=pyopt_driver
    $ pip install -e git+http://github.com/DTUWindEnergy/FUSED-Wake.git#egg=fusedwake    
    $ pip install -e git+http://github.com/DTUWindEnergy/TOPFARM.git#egg=topfarm

## TOPFARM Developer version

Note that TOPFARM and FUSED-Wind have been installed in "editable" mode (-e) in the virtual environment source directory
(`topfarmv/src` or `OpenMDAO-Framework/devenv/src`). Which means that they are actually installed in a 
cloned directory from their respective github account. From there, you can edit them, commit, push, pull etc..

## Using TOPFARM

Once TOPFARM is installed correctly, you have to activate the corresponding virtual environment before being able to use it.
If you installed your own virtual environment you have to do:

    $ . topfarmv/bin/activate

If you installed OpenMDAO directly, you have to use the virtual environment provided by OpenMDAO

    $ . OpenMDAO-Framework/devenv/bin/activate
    
## Testing TOPFARM installation

You can check if everything is installed correctly by running the tests

    $ 

## Documentation

To view the Sphinx documentation for this distribution, type:

    $ plugin docs topfarm
    
    
## Feedbacks and Discussions
Join our [google group](https://groups.google.com/forum/#!forum/topfarm) to stay informed about the latests talks and 
software releases, to ask questions, to give us feedbacks, to 
discuss various topics related to TOPFARM platform. 

If you have specific issues to discuss such as bug report or feature request, it's probably more effective to go to the 
github issue page and create an issue there.

## License

TOPFARM is available both under the [GNU Affero General Public License v3.0](http://en.wikipedia.org/wiki/Affero_General_Public_License) 
(AGPL3) and under a custom based commercial license available upon request. 
The AGPL3 license is an open source license, so you are welcome to use and modify the code as you wish. 
Note that AGPL3 is also a copyleft license, which means that derived works can only be distributed (or made available
as an online service) as open source, under the same license terms. For more information about this issue, feel free to contact us.


## Supporting TOPFARM development
We believe in Open Science, in accelerating science development by collaborating with each other through our codes. 
This is why we have put TOPFARM in open source and open access on github.com. But this requires trust that our users will 
give back to the community. We are a pilote project at DTU Wind Energy, and for that reason it is very important for us
to prove to our administration that this is the way forward, and that sharing codes does not mean being ripped off by the
users. You can support our efforts in the following ways.
 
We need to have quantitative metrics on how effective we are at disseminating 
our knowledge. So, please, help us getting recognition from our administration:

* "star" and "follow" us on github
* join our [google group](https://groups.google.com/forum/#!forum/topfarm)
* tell us what you are using TOPFARM for on the forum or by private email
* cite which TOPFARM version you are using in your articles and presentations with the appropriate zenodo DOI
* announce when you have published a new piece work (e.g. articles, abstract, report, slides, code) based on TOPFARM on 
the [google group](https://groups.google.com/forum/#!forum/topfarm). 
* Use [Zenodo](http:/zenodo.org) as much as possible to put your work in open access (based on the pre/post-prints if necessary to avoid copyright issues with the journals). 
* Upload your zenodo publication to the [TOPFARM Community hosted on Zenodo](https://zenodo.org/collection/user-topfarm).
* Link to the version of TOPFARM you are using inside zenodo (i.e. the *Related publications and datasets* section)
 
You are of course welcome to contribute to the development of TOPFARM itself, for that purpose you should follow the standard
github methodology: 

* create a fork of TOPFARM, 
* make the modifications, 
* create some tests, 
* commit & push to your own fork
* submit a pull request to be reviewed by the TOPFARM development team


Furthermore, we are academics employees, so you can also support our efforts by inviting us 

* as active co-authors on your paper
* to present TOPFARM at your workshop / conference
* to be a partner in your project application
* to co-supervise a MSc or PhD topic
* to be a subcontractor in a commercial work

Finally we need funding for further developing TOPFARM. Our business model is to sell tailored commercial version of 
TOPFARM to the industry, and to provide training both for industry and academia (e.g. webinars, online and face-to-face 
courses).
