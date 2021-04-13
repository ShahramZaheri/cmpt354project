from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField, BooleanField, TextField, TextAreaField, SelectField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo



#Form for inserting new employee
class NewEmployeeForm(FlaskForm):
    employee_first_name = StringField('First Name', validators=[DataRequired(), Length(min=1, max=25)]) 
    employee_middle_name = StringField('Middle Name',validators=[ Length(max=25)]) 
    employee_last_name = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=25)])
    # employee_email = StringField('Email',validators=[DataRequired(), Email()])
    employee_SIN = StringField('Social Insurance Number (SIN)', validators=[DataRequired(), Length(min=9, max=9)])
    employee_phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=10)])
    employee_Address= StringField('Home Address', validators=[DataRequired(), Length(min=1, max=25)])
    employee_date_of_birth = StringField('Date of Birth', validators=[DataRequired(), Length(min=1, max=25)])
    roles=["office", "operation"]
    employee_role = SelectField('Employee works at', choices = roles, validators = [DataRequired()])
    employee_salary = DecimalField('Employee Salary/Wage', places=2, validators=[DataRequired()])
    
    
    
    # first_emergency_contact_full_name = StringField('Emergency Contact Full Name', validators=[DataRequired(), Length(min=1, max=25)])
    # first_emergency_contact_relationship = StringField('Relationship with Employee', validators=[DataRequired(), Length(min=1, max=25)]) 
    # first_emergency_contact_phone_number = StringField('Emergency Contact Phone Number', validators=[DataRequired(), Length(min=1, max=25)])

    submit = SubmitField('Add New Employee')

class PayrollForm(FlaskForm):
    employee_filter = SelectField('Employee', coerce=str)
    start_date = StringField('From')
    end_date = StringField('To')
    submit = SubmitField('Filter')

class update_employee_info_form(FlaskForm):
    employee_SIN = StringField('Social Insurance Number (SIN)', validators=[DataRequired(), Length(min=1, max=25)])
    submit = SubmitField('Find Employee')

class remove_employee_form(FlaskForm):
    employee_last_name = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=25)])
    submit = SubmitField('Remove Employee')
