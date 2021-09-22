__author__ = "Junhee Yoon"
__version__ = "1.0.0"
__maintainer__ = "Junhee Yoon"
__email__ = "swiri021@gmail.com"

# Flask related libraries
from flask import Flask, request, render_template, redirect, url_for, session
from flask_bootstrap import Bootstrap
from models import InitForm

# Flask apps libraries
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from flask_wtf.csrf import CSRFProtect

# Additional function libraries
import yaml
import uuid
import os
import subprocess

# Custom form making
from wtforms.validators import Required
from flask_wtf import Form
from wtforms import TextField, SubmitField


app = Flask(__name__)
app.config['SECRET_KEY'] = 'swiri021swiri021' # CSRF key
Bootstrap(app) # set Bootstrap

# setting Navigation Bar
nav = Nav(app)

@nav.navigation()
def mynavbar():
    return Navbar( 'Workflow Controller', View('Home', 'home') )
nav.init_app(app)

# setting CSRF protector
csrf = CSRFProtect()
csrf.init_app(app)


#########Route###########
# Actual function
@app.route("/", methods=['GET', 'POST'])
def home():
    """
    Landing page and selecting pipeline to control
    """
    #session.clear() # When it gets back, clear session data
    session['_id'] = uuid.uuid4().hex # random session id for recognize diffent snakemake running
    form = InitForm(request.form)

    # Getting 'data' from pipeline selector and redirect to yaml creator
    if form.validate_on_submit():
        session['selected_pipeline'] = form.pipeline_name.data # create session data for passing value
        return redirect(url_for('config_yaml_creator'))

    return render_template( 'home.html', title="Snakemake controller", form=form)


@app.route("/yamlcreator", methods=['GET', 'POST'])
def config_yaml_creator():
    """
    Making a form by parsing config.yaml
    """

    # Frame Form
    class SnakeMakeForm(Form):
        pass;

    val = session.get('selected_pipeline', None) # yaml path
    yaml_data = _parsing_yamlFile(val) # Parsing yaml data

    for key, value in yaml_data.items(): # Loop with yaml keys
        setattr(SnakeMakeForm, key, TextField(key, validators=[Required()], render_kw={'placeholder': value})) # set key with yaml key and placehoder with value
    setattr(SnakeMakeForm, 'submit', SubmitField('Submit')) # Make submit button on the bottomss
    form = SnakeMakeForm(request.form) # set form

    if form.validate_on_submit():
        result_yaml_data={} # result dictionary
        # order is same as form order
        for formData, yamlKeys in zip(form, yaml_data.keys()):
            result_yaml_data[yamlKeys]=formData.data
        
        yaml_output = _reform_yamlFile(val, result_yaml_data) # make result yaml file
        session['yaml_output'] = yaml_output
        return redirect(url_for('workflow_status'))

    return render_template('config_yaml_creator.html', form=form)

@app.route("/status")
def workflow_status():

    pipeline_path = session.get('selected_pipeline', None) # Pipeline path
    yaml_file = session.get('yaml_output', None) # yaml file

    ## Running snakemake
    cmd = 'snakemake --snakefile %s --cores 3 --configfile %s'%(pipeline_path+"Snakefile",yaml_file)
    print(cmd)
    try:
        p = subprocess.check_output([cmd], shell=True)
    except subprocess.CalledProcessError as e:
        p = "Error occur in snakemake, please check log files in pipelines folder"

    return render_template('status.html', msg=p)

#########Route###########


# Parsing function for yaml data, only work 2 layer nested yaml file
def _parsing_yamlFile(workflow_path):
    """
    Description: This function parses yaml format in config.yaml, and returns dictionary with parse data
    
    Input: yaml path
    Output: Dictionary with parse data
    """
    
    ## yaml check
    ## yaml check
    print(workflow_path)
    with open(workflow_path+"/config.yaml", "r") as stream: # Open yaml
        try:
            yaml_data = yaml.safe_load(stream) # Parse auto with pyyaml
        except yaml.YAMLError as exc:
            print(exc)
    
    new_result = {} # for new result dictionary
    for key, value in yaml_data.items():
        if isinstance(value, dict)==True: # Nested dictionary
            for nkey, nval in value.items(): # Only key name for making form
                new_result[key+"--"+nkey] = nval # Nested key has '--', making flatten
        else:
            new_result[key]=value #just pass with normal dictionary
    return new_result

# Custom yaml converting function because of pyyaml unexpected charter
def _reform_yamlFile(selected_pipeline, data_dict):
    """
    Description: This function converts dictionary to yaml for snakemake, and write yaml file on the path
    
    Input: pipeline path and dictionary data
    Output: yaml file
    """
    yamlFileName = selected_pipeline+"/config_"+str(session.get('_id', None))+".yaml"
    f = open(yamlFileName, "w") # write file with unique name

    nested_items = [] # List for handing nested items
    for key, value in data_dict.items():
        if key.find('--')>-1: # Nested key has '--'
            subkeys = key.split('--')# 2 layers keys
            nested_items.append([subkeys[0],subkeys[1],value]) #make list
        else:
            f.write(key+": "+value+"\n")

    key1_unique=list(set([x[0] for x in nested_items])) # make a list of root key
    for x in key1_unique:
        f.write(x+":"+"\n") # first line of nested key (root key)
        for y in nested_items:
            if y[0]==x:
                f.write("  "+y[1]+": "+y[2]+"\n") # sub-key and value
    
    f.close()
    return yamlFileName
    
if __name__ == '__main__':
    app.run(host='0.0.0.0')