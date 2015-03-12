FROM piredtu/fusedwind

MAINTAINER Pierre-Elouan Rethore <pire@dtu.dk>

WORKDIR /openmdao

ADD requirements.txt /openmdao/requirements.txt
ADD topfarm.sh /topfarm.sh

RUN git clone http://github.com/DTUWindEnergy/FUSED-Wake.git /openmdao/FUSED-Wake
RUN bash -c "source $OPENMDAODIR/bin/activate; python /openmdao/FUSED-Wake/gclarsen/setup.py install"
RUN bash -c "source $OPENMDAODIR/bin/activate; python /openmdao/FUSED-Wake/py4we/setup.py install"

RUN bash -c "source $OPENMDAODIR/bin/activate; pip install -r /openmdao/requirements.txt"

RUN ln -s $OPENMDAODIR/src/topfarm /topfarm

WORKDIR /

CMD ["/topfarm.sh"]
