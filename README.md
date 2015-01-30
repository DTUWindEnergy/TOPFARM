#TOPFARM

TOPFARM is a wind farm optimization framework developed by DTU Wind Energy, based on [FUSED-Wind](http://www.fusedwind.org) and [OpenMDAO](http://www.openmdao.ord).


## Dependencies and supported Python versions

TOPFARM depends of on [OpenMDAO v0.10.3](https://github.com/OpenMDAO/OpenMDAO-Framework) and [FUSED-Wind v0.1](https://github.com/fusedwind/fusedwind) and support python
2.7.x.

## Development installation

### Automatic installation
If you are on Linux of MacOSX, you can try to run the following script to install everything in a new virtual environment

    $ install_all.sh

### Manual installation
Create a new topfarm directory

    $ mkdir topfarm
    $ cd topfarm
    
Install `virtualenv`, if you don't already have it available
 
    $ easy_install virtualenv
    
Then create a new virtual environement and activate it

    $ virtualenv topfarmv
    $ . topfarmv/bin/activate

Install the pre-requisits to OpenMDAO (if it doesn't work, make sure that you have your [latest version of pip](http://stackoverflow.com/questions/26575587/cant-install-scipy-through-pip))

    $ pip install numpy scipy

Install [OpenMDAO development v0.10.3](https://github.com/OpenMDAO/OpenMDAO-Framework/tree/0.10.3).

    $ wget https://github.com/OpenMDAO/OpenMDAO-Framework/archive/0.10.3.zip
    $ unzip 0.10.3.zip
    $ cd OpenMDAO-Framework-0.10.3
    $ go-openmdao-dev.py
    
... coffee break ...

Then install [FUSED-Wind](https://github.com/fusedwind/fusedwind) from their repositories

    $ cd ..
    $ wget https://github.com/FUSED-Wind/fusedwind/archive/v0.1.0.zip
    $ unzip v0.1.0.zip
    $ cd fusedwind
    $ plugin install
    $ cd ..

Then run the following commands to download and install TOPFARM

    $ git clone git@github.com:DTUWindEnergy/FUSED-TOPFARM.git
    $ cd topfarm
    $ plugin install

## Documentation

To view the Sphinx documentation for this distribution, type:

    $ plugin docs topfarm
    
    
## Feedbacks and Discussions
Join our [google group](https://groups.google.com/forum/#!forum/topfarm) to stay informed about the latests talks and 
software releases, to ask questions, to give us feedbacks, to 
discuss various topics related to TOPFARM platform. 

If you have specific issues to discuss such as bug report or feature request, it's probably more effective to go to the 
github issue page and create an issue there.

## Supporting TOPFARM development
We believe in Open Science, in accelerating science development by collaborating with each other through our codes. 
This is why we have put TOPFARM in open source and open access on github.com. But this requires trust that our users will 
give back to the community. We our a pilote project at DTU Wind Energy, and for that reason it is very important for us
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