## Instruction
* Please use notebook_lib and notebook utils to analysis, if you want to create new function, just add it on folder
* If you added new function and library in folders, please update README file for instruction

## Guide for docker volumes
* Please mount or bind with this information
```yaml
## Local path:container path
- notebook/notebook_lib:/home/jovyan/work/notebook_lib
- notebook/notebook_utils:/home/jovyan/work/notebook_utils
- notebook/resultFiles:/home/jovyan/work/resultFiles
- data:/home/jovyan/data
```

## Library List
| Name | Description | Reference or link |
|---------|---------|---------|
| NWPV2 | DEG function with pvalue integration | [github](https://github.com/swiri021/NWPV2/blob/master/README.md), [paper](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3135688/) |

## Utils List
| Name | Description | Reference or link |
|---------|---------|---------|
| OpenKbcMSToolkit | Handy toolkit for data extraction | No reference |
