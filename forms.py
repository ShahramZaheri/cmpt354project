from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo



#Form for inserting new employee
class NewEmployeeForm(FlaskForm):
    employee_first_name = StringField('First Name', validators=[DataRequired(), Length(min=1, max=10)]) 
    employee_middle_name = StringField('Middle Name', validators=[DataRequired(), Length(min=1, max=25)]) 
    employee_last_name = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=25)])
    employee_email = StringField('Email',validators=[DataRequired(), Email()])
    employee_SIN = StringField('Social Insurance Number (SIN)', validators=[DataRequired(), Length(min=1, max=25)])
    employee_phone = StringField('Phone Number', validators=[DataRequired(), Length(min=1, max=25)])
    employee_Address= StringField('Home Address', validators=[DataRequired(), Length(min=1, max=25)])
    employee_date_of_hire = StringField('Date of Hire', validators=[DataRequired(), Length(min=1, max=25)])
    employee_date_of_birth = StringField('Date of Birth', validators=[DataRequired(), Length(min=1, max=25)])
    submit = SubmitField('Add New Employee')

# class removeEmployee(FlaskForm):

