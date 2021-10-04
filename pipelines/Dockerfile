FROM continuumio/miniconda

COPY pipeline_controller/requirements.txt .
COPY pipeline_controller/installer_Rpackage.R .

RUN conda create -n pipeline_controller_base python=3.8.2 R=3.6
SHELL ["conda", "run", "-n", "pipeline_controller_base", "/bin/bash", "-c"]

RUN conda install -n pipeline_controller_base -c anaconda -y graphviz
RUN pip install -r requirements.txt
RUN Rscript installer_Rpackage.R

RUN python -c "import flask"