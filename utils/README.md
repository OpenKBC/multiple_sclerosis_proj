# Utils for the project

### Requirements
```shell
conda create -n your_env python=3.9
pip install -r requirements.txt
```

#### 1. get_matrix_from_files.py
This code is for making matrix expression from files, and final output file will be [feather format](https://arrow.apache.org/docs/python/feather.html)
```shell
usage: get_matrix_from_files.py [-h] -t {genes,isoforms} -p FILEPATH -v {FPKM,TPM,expected_count} -c
                                {CD4,CD8,CD14} -o OUTPUT

optional arguments:
  -h, --help            show this help message and exit
  -t {genes,isoforms}, --ftype {genes,isoforms}
                        Mode for getting matrix (isoforms or genes), default = genes
  -p FILEPATH, --path FILEPATH
                        Directory path for input files, default = ./
  -v {FPKM,TPM,expected_count}, --value {FPKM,TPM,expected_count}
                        Value type for extraction, default = TPM
  -c {CD4,CD8,CD14}, --ctype {CD4,CD8,CD14}
                        Cell type for extraction, default = CD8
  -o OUTPUT, --output OUTPUT
                        Output file path and name
```
**Example:**
```shell
python get_matrix_from_files.py -t genes -p ../data/rsem_counts/ -v TPM -c CD8 -o ../CD8_samples
```

#### 2.cleanup_normalized_matrix.py
This code is for getting cleaned up data before running IDconverter.R, it generates new index and columns names of normalized matrix and takes care of duplicated indexes

```shell
usage: cleanup_normalized_matrix.py [-h] -i INPUT_DF -o OUTPUT

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_DF, --input INPUT_DF
                        Input data matrix
  -o OUTPUT, --output OUTPUT
                        Output file name including path

```
**Example:**
```shell
python get_matrix_from_files.py -i input.csv -o output.csv
python get_matrix_from_files.py -i input.feather -o output.feather
```