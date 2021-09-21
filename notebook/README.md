## Instruction
* Please use notebook_lib and notebook utils to analysis, if you want to create new function, just add it on folder
* If you added new function and library in folders, please update README file for instruction

## Guide for docker volumes
* Please mount or bind with this information
* For getting data, please ask members to have s3 access 
```yaml
## Local path:container path
- notebook/notebook_lib:/home/jovyan/work/notebook_lib
- notebook/notebook_utils:/home/jovyan/work/notebook_utils
- notebook/resultFiles:/home/jovyan/work/resultFiles
- data:/home/jovyan/data
```

## Library List
| Name | Description | Language |Reference or link |
|---------|---------|---------|---------|
| NWPV2 | DEG function with pvalue integration | Python |[github](https://github.com/swiri021/NWPV2), [paper](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3135688/) |
| gene_zscore | Getting Gene-set Zscore(Activation Score) for data| Python | [github](https://github.com/swiri021/Threaded_gsZscore), [paper](https://genomebiology.biomedcentral.com/articles/10.1186/gb-2006-7-10-r93) |


## Utils List
| Name | Description | Language |Reference or link |
|---------|---------|---------|---------|
| OpenKbcMSToolkit | Handy toolkit for data extraction | Python | No reference |
| OpenKbcMSCalculator | Advanced calculators for getting result| Python | No reference |