from flask_wtf import Form
from wtforms import TextField, SubmitField, TextAreaField, SelectField
from wtforms.validators import Length, Required

import glob

# Form ORM
class InitForm(Form):

    # Internal function to create form
    def _get_directory_name():
        dir_list = glob.glob("../*/") # Get DIR list
        dir_names = [x.replace("../","")[:-1] for x in dir_list] # Cleanup names of dir

        # SelectField: choices=[(value, showing key on page)]
        choice_output = [(x, y) for x, y in zip(dir_list, dir_names) if y!='pipeline_controller']
        return choice_output

    pipeline_name = SelectField('Please select your pipeline to run: ', choices=_get_directory_name())
    #essay_question = TextAreaField('Who do you think won the console wars of 1991, Sega Genesis or Super Nintendo? (2048 characters)', validators=[Required(),Length(max=2047)] )
    #email_addr = TextField('Enter Your Email', validators=[Required()])
    #submit = SubmitField('Submit')

    submit = SubmitField('Submit')

class YamlForm(Form):
    inputPath = TextField('Enter Input path which has sample file', validators=[Required()], render_kw={'placeholder': '/home/samples/'})