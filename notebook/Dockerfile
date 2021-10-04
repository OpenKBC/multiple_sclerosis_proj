FROM jupyter/datascience-notebook

COPY installers/installer_Rpackage.R /installer_Rpackage.R
COPY installers/requirements.txt /requirements.txt

RUN Rscript /installer_Rpackage.R
RUN pip install -r /requirements.txt