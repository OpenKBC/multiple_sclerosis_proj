## Feature Extraction by Jun
* This workflow generates feature extracted gene expression data by CD4, CD8 and CD14. It starts with vst(or DEseq2) normalized expression and it makes activation scores as interim result automatically. Activation scores is used for the first step of feature extraction, and the workflow generates gene matrix witht final genes list.

#### Requirement
```shell
pip install -r requirements.txt
```

#### Usage
```shell
snakemake --cores 3
```