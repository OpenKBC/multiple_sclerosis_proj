# Snakemake pipelines for routine work

#### Pipeline List
| Name | Repository data Point | Description |
|---------|---------|---------|
| Feature Extraction by Jun | data/, notebook/resultFiles | Feature extraction workflow from activation score to gene feature(Ranksum to Recursive Feature Elimination CV) |

## Guide for docker volumes
* Please mount or bind with this information
* For getting data, please ask members to have s3 access 
```yaml
## Local path:container path
    - data/:/MainData
    - notebook/resultFiles:/Output
```
