
================
Package Metadata
================

- **author:** Pierre-Elouan Rethore

- **author-email:** pire@dtu.dk

- **classifier**:: 

    Intended Audience :: Science/Research
    Topic :: Scientific/Engineering

- **copyright:** (C) DTU-Wind Energy, TOPFARM Development Team

- **description-file:** README.md

- **download-url:** https://github.com/DTUWindEnergy/TOPFARM.git

- **entry_points**:: 

    [openmdao.component]
    src.topfarm.optimizers.GeneticOpt=src.topfarm.optimizers:GeneticOpt
    src.topfarm.plot.OffshorePlot=src.topfarm.plot:OffshorePlot
    src.topfarm.optimizers.COBYLAOpt=src.topfarm.optimizers:COBYLAOpt
    pyopt_driver.pyopt_driver.pyOptDriver=pyopt_driver.pyopt_driver:pyOptDriver
    src.topfarm.topfarm.Topfarm=src.topfarm.topfarm:Topfarm
    src.topfarm.optimizers.SLSQPOpt=src.topfarm.optimizers:SLSQPOpt
    src.topfarm.optimizers.PyoptOpt=src.topfarm.optimizers:PyoptOpt
    src.topfarm.layout_distribution.DistributeSpiral=src.topfarm.layout_distribution:DistributeSpiral
    src.topfarm.tlib.DistFromTurbines=src.topfarm.tlib:DistFromTurbines
    src.topfarm.tlib.ConverHullArea=src.topfarm.tlib:ConverHullArea
    src.topfarm.elnet.ElNetLength=src.topfarm.elnet:ElNetLength
    src.topfarm.optimizers.CONMINOpt=src.topfarm.optimizers:CONMINOpt
    src.topfarm.optimizers.NEWSUMTOpt=src.topfarm.optimizers:NEWSUMTOpt
    src.topfarm.foundation.FoundationLength=src.topfarm.foundation:FoundationLength
    src.topfarm.layout_distribution.DistributeXY=src.topfarm.layout_distribution:DistributeXY
    src.topfarm.tlib.DistFromBorders=src.topfarm.tlib:DistFromBorders
    src.topfarm.elnet.ElNetLayout=src.topfarm.elnet:ElNetLayout
    src.topfarm.aep.AEP=src.topfarm.aep:AEP
    [openmdao.driver]
    src.topfarm.optimizers.PyoptOpt=src.topfarm.optimizers:PyoptOpt
    src.topfarm.optimizers.SLSQPOpt=src.topfarm.optimizers:SLSQPOpt
    src.topfarm.optimizers.COBYLAOpt=src.topfarm.optimizers:COBYLAOpt
    src.topfarm.optimizers.CONMINOpt=src.topfarm.optimizers:CONMINOpt
    pyopt_driver.pyopt_driver.pyOptDriver=pyopt_driver.pyopt_driver:pyOptDriver
    src.topfarm.optimizers.NEWSUMTOpt=src.topfarm.optimizers:NEWSUMTOpt
    src.topfarm.optimizers.GeneticOpt=src.topfarm.optimizers:GeneticOpt
    [openmdao.container]
    src.topfarm.optimizers.GeneticOpt=src.topfarm.optimizers:GeneticOpt
    src.topfarm.plot.OffshorePlot=src.topfarm.plot:OffshorePlot
    src.topfarm.optimizers.COBYLAOpt=src.topfarm.optimizers:COBYLAOpt
    src.topfarm.tlib.DistFromBorders=src.topfarm.tlib:DistFromBorders
    src.topfarm.topfarm.Topfarm=src.topfarm.topfarm:Topfarm
    pyopt_driver.pyopt_driver.pyOptDriver=pyopt_driver.pyopt_driver:pyOptDriver
    src.topfarm.optimizers.SLSQPOpt=src.topfarm.optimizers:SLSQPOpt
    src.topfarm.optimizers.PyoptOpt=src.topfarm.optimizers:PyoptOpt
    src.topfarm.layout_distribution.DistributeSpiral=src.topfarm.layout_distribution:DistributeSpiral
    src.topfarm.tlib.ConverHullArea=src.topfarm.tlib:ConverHullArea
    src.topfarm.elnet.ElNetLength=src.topfarm.elnet:ElNetLength
    src.topfarm.optimizers.CONMINOpt=src.topfarm.optimizers:CONMINOpt
    src.topfarm.tlib.DistFromTurbines=src.topfarm.tlib:DistFromTurbines
    src.topfarm.optimizers.NEWSUMTOpt=src.topfarm.optimizers:NEWSUMTOpt
    src.topfarm.foundation.FoundationLength=src.topfarm.foundation:FoundationLength
    src.topfarm.layout_distribution.DistributeXY=src.topfarm.layout_distribution:DistributeXY
    src.topfarm.elnet.ElNetLayout=src.topfarm.elnet:ElNetLayout
    src.topfarm.aep.AEP=src.topfarm.aep:AEP

- **home-page:** https://github.com/DTUWindEnergy/TOPFARM

- **keywords:** openmdao, TOPFARM, FUSED-Wind

- **license:** AGPL v3.0

- **maintainer:** Pierre-Elouan Rethore

- **maintainer-email:** pire@dtu.dk

- **name:** topfarm

- **project-url:** https://github.com/DTUWindEnergy/TOPFARM

- **requires-dist**:: 

    openmdao.main=0.10.3
    openmdao.lib=0.10.3
    fusedwind=0.1.0
    numpy
    scipy
    matplotlib
    pandas
    seaborn
    pyopt_driver

- **requires-python**:: 

    >=2.6
    <3.0

- **static_path:** [ '_static' ]

- **summary:** Wind plant optimization tool based on FUSED-Wind and OpenMDAO

- **version:** 0.1.0

