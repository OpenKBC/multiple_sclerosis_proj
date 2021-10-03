## DEG pipeline(DESeq2) by Jun
* This workflow generates DEG result by using DESeq2, and it is working for only GEO styles of dataset

#### Version history
* It has memory issue in Docker
* v1.0.0 is on the pipeline workflow

#### Requirement
```shell
pip install -r ../pipelines/pipeline_contoller/requirements.txt
Rscript ../pipelines/pipeline_contoller/installer_Rpackage.R
```

#### Usage
* Please change config.yaml for standalone usage

```shell
snakemake --cores 3
```