## Snakemake pipelines for routine work

* Pipeline list:

| Name | Repository data Point | Description |
|---------|---------|---------|
| Feature Extraction by Jun | data/, notebook/resultFiles | Feature extraction workflow from activation score to gene feature(Ranksum to Recursive Feature Elimination CV) |
| DEG Pipeline(DESeq2) by Jun | data/, notebook/resultFiles | Base DEG workflow from count files(raw files), (**Has memory issue**) |

### Guide for docker volumes
* Please mount or bind with this information
* For getting data, please ask members to have s3 access 
```yaml
## Local path:container path
    - data/:/MainData
    - notebook/resultFiles:/Output
```

### Controller
* After container up, access to localhost url for using controller
```
http://localhost/
```

