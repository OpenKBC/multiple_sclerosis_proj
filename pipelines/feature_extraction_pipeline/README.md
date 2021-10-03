## Feature Extraction by Jun
* This workflow generates feature extracted gene expression data by CD4, CD8 and CD14. It starts with vst(or DEseq2) normalized expression and it makes activation scores as interim result automatically. Activation scores is used for the first step of feature extraction, and the workflow generates gene matrix witht final genes list.

#### Version history
* v1.0.1 has more functions of sample spliter(step1: _LoadDiseaseDuration)
* v1.0.0 is on the pipeline workflow

#### Requirement
* Naming of Input file should be count_vst_cellType.csv ex) count_vst_CD4.csv, count_vst_CD8.csv 
```shell
pip install -r ../pipelines/pipeline_contoller/requirements.txt
Rscript ../pipelines/pipeline_contoller/installer_Rpackage.R
```

#### Usage
* Please change config.yaml for standalone usage

```shell
snakemake --cores 3
```