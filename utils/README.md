# Utils for the project

### Requirements
```shell
conda create -n your_env python=3.9
pip install -r requirements.txt
```

### 1. get_matrix_from_files.py
This code is for making matrix expression from files, and final output file will be [feather format](https://arrow.apache.org/docs/python/feather.html)
```shell
python get_matrix_from_files.py --help

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
