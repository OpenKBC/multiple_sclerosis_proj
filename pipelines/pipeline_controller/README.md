## Pipeline Controller
This is pipeline controller(SnakeMake) for pipeline container by using Flask, Jinja2 and Bootstrap. This controller provides config.yaml form for executing snakemake and it will execute the workflow after submission.

**Current version(v1.0.0) does not have loading spinner, please wait for browser spinne instead of itr**

### Requirements
- The controller should be located to same root folder with pipeline folders
- All pipelines should have same snakefile name(Snakemake) and configuration name(config.yaml)
- Structure example:
```
pipelines/(root)
|--pipeline_controller/
|--Pipeline1/
|--Pipeline2/
```
- Install requirements.txt

```
pip install -r requirements.txt
```

### Usage

- Flask development
```
export FLASK_APP=app
flask run
```
- Docker
```
docker-compose up
```
- On browser(after docker-compose up)
```
http://localhost:80/
```

### Importing pipeline
- Create pipeline folder inside root directory
- Make snakefile and check all the path is **absolute path**
- Make **config.yaml** for template