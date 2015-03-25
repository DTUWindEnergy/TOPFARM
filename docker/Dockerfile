FROM piredtu/fusedwind

MAINTAINER Pierre-Elouan Rethore <pire@dtu.dk>

ENV INSTALL_DIR /openmdao
ENV LD_LIBRARY_PATH /usr/local/lib:/usr/lib:$LD_LIBRARY_PATH
WORKDIR $INSTALL_DIR

USER root
RUN apt-get install -y subversion wget

ADD requirements.txt $INSTALL_DIR/requirements.txt
ADD build_topfarm.sh $INSTALL_DIR/build_topfarm.sh

RUN chmod +x $INSTALL_DIR/build_topfarm.sh

RUN $INSTALL_DIR/build_topfarm.sh

RUN ln -s $OPENMDAODIR/src/topfarm /topfarm
RUN chown openmdao -R $INSTALLDIR

WORKDIR /topfarm
USER openmdao

CMD omdao $INSTALLDIR/notebook.sh
