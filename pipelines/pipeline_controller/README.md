## Pipeline Controller
This is pipeline controller(SnakeMake) for pipeline container by using Flask, Jinja2 and Bootstrap. This controller provides config.yaml form for executing snakemake and it will execute the workflow after submission.

### Version history
* version(v1.0.2) docker-compose is ready
* version(v1.0.1) imported celery-redis for workers and communication
* version(v1.0.0) does not have loading spinner, please wait for browser spinne instead of it

### Requirements
- The controller should be located to same root folder with pipeline folders
- All pipelines should have same snakefile name(Snakemake) and configuration(config.yaml)
- Memory usage: 4-5gb for DEG pipeline (Please change your docker manager setting for this)
- Structure example:
```
pipelines/(root)
|--pipeline_controller/
|--Pipeline1/
|--Pipeline2/
```
- Install requirements

```
pip install -r pipeline_controller/requirements.txt
Rscript pipeline_controller/installer_Rpackage.R
```

### Usage
* Using docker-compose is highly recommended, but you can run pipeline manually by modifying snakefile and launching flask, celery in local
* After ```docker-compose -f docker-compose.yaml up --build```, go to the browser and http://localhost for pipeline, http://localhost:8888/?token= for jupyter notebook
* Don't use docker-compose.AWS.yaml in local

### Importing pipeline
- Create pipeline folder inside root directory
- Make snakefile and check all the path is **absolute path**
- For example, ```pipeline_path = '/pipelines/deg_pipeline/'``` pipeline_path always has to be absolute path in docker **(NOT LOCAL PATH)**
- Make **config.yaml** for template