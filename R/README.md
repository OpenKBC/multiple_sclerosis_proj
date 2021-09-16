# Utils for the project

### Requirements
```shell
Rscript notebook/installers/installer_Rpackage.R
```

#### 1. deseq2_normalizaiton.R
This code is an example to get normalized matrix from raw files, it does not have instruction

#### 2. IDconverter.R
This code is converter for Ensembl ID to Entrez ID, and input should be cleaned up. Input file should be CSV format.

**Example:**
```shell
Rscript IDconverter.R inputpath/input.csv outputpath/output.csv
```
