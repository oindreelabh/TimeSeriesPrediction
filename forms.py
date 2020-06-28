from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length , EqualTo
import pandas as pd


class OutputForm(FlaskForm):
    df = pd.read_csv(r'C:/Users/User/Desktop/project 3/processed_data.csv')
    cl = df['Client Name'].unique()
    clientName = SelectField('clientName' , choices = cl)
    Legal = SelectField('Le')
