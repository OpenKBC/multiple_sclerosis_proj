## DEG pipeline(DESeq2) by Jun
* This workflow generates DEG result by using DESeq2, and it is working for only GEO styles of dataset

#### Version history
* It has memory issue in Docker
* v1.0.0 is on the pipeline workflow

#### Requirement
```shell
pip install -r requirements.txt
Rscript installer_Rpackage.R
```

#### Usage
* Please change config.yaml for standalone usage

```shell
snakemake --cores 3
```