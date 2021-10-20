## AWS module for running the project
* This is initial version of DEG pipeline with AWS batch, it has same function with pipeline module in this project.
* To change input, JSON file needs modification

### Requirements on local PC
```
apt-get install awscli
apt-get install jq
```

### Usage on local PC
* To change sample, please replace JSON file to calculate the score
```json
    "environment": [
        {
            "name": "msigdb",
            "value": "msigdb.v7.4.entrez.gmt(don't change this)"
        },
        {
            "name": "inputfile",
            "value": "Sample name here"
        }
      ]
```
* And run module
```
# Single job
sh batch_module_singleJob.sh 

# Parallelized job
sh batch_module_parallel.sh
```

### Multiple Jobs Flow
![flow1](../../README_resource/batch_detail.png)