__author__ = "Junhee Yoon"
__version__ = "1.0.0"
__maintainer__ = "Junhee Yoon"
__email__ = "swiri021@gmail.com"

from flask import Flask, request, render_template, redirect, url_for, session
from flask_bootstrap import Bootstrap
from models import InitForm, YamlForm
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from flask_wtf.csrf import CSRFProtect

import yaml


app = Flask(__name__)
app.config['SECRET_KEY'] = 'swiri021swiri021'
Bootstrap(app)

# Navigation Bar
nav = Nav(app)

@nav.navigation()
def mynavbar():
    return Navbar( 'Workflow Controller', View('Home', 'home') )
nav.init_app(app)

# CSRF protector
csrf = CSRFProtect()
csrf.init_app(app)

# Actual function
@app.route("/", methods=['GET', 'POST'])
def home():
    """Landing page."""
    session.clear() # When it gets back, clear session data
    form = InitForm(request.form)

    # Getting 'data' from pipeline selector and redirect to yaml creator
    if form.validate_on_submit():
        session['selected_pipeline'] = form.pipeline_name.data # create session data for passing value
        return redirect(url_for('config_yaml_creator'))

    return render_template( 'home.html', title="Snakemake controller", form=form)

@app.route("/yamlcreator", methods=['GET', 'POST'])
def config_yaml_creator():
    val = session.get('selected_pipeline', None)
    #Parsing here
    _parsing_yamlFile(val)
    #Parsing here

    form=YamlForm(request.form)
    return render_template('config_yaml_creator.html', form=form)

def _parsing_yamlFile(workflow_path):
    with open(workflow_path+"/config.yaml", "r") as stream:
        try:
            yaml_data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    for key, value in yaml_data.items():
        if isinstance(value, dict)==True:
            print("NESTED: "+key+":"+str(value))
        else:
            print(key +":" +value)



if __name__ == '__main__':
    app.run(host='0.0.0.0')