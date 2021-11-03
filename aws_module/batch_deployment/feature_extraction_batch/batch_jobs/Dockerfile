FROM continuumio/miniconda

RUN mkdir /data
RUN mkdir /output

COPY . .
RUN conda create -n pipeline_controller_base python=3.8.2 R=3.6
SHELL ["conda", "run", "-n", "pipeline_controller_base", "/bin/bash", "-c"]

RUN pip install -r requirements.txt
RUN Rscript installer_Rpackage.R
RUN chmod +x pipeline_controller.sh