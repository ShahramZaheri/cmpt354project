from flask import Flask, render_template, url_for, flash, redirect
from forms import NewEmployeeForm, update_employee_info_form
import sqlite3
import os.path
# print(os.path)
print(os.getcwd())
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# print("======================")
# print(BASE_DIR)
# db_path = os.path.join(BASE_DIR, "hungfung.db")
conn = sqlite3.connect('hungfung.db')
app = Flask(__name__)
app.config['SECRET_KEY'] = 'cmpt354'
#Turn the results from the database into a dictionary
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/employee', methods=['GET', 'POST'])
def employee():
    form=NewEmployeeForm()
    return render_template('employee.html')

@app.route('/employee/add_new_employee', methods=['GET', 'POST'])
def add_new_employee():
    form=NewEmployeeForm()
    return render_template('add_new_employee.html',form=form)

@app.route('/employee/update_employee_info', methods=['GET', 'POST'])
def update_employee_info():
    form=update_employee_info_form()
    return render_template('update_employee_info.html',form=form)

@app.route('/report')
def report():
    # conn = sqlite3.connect('hungfung.db')
    # conn.row_factory = dict_factory
    # c = conn.cursor()
    # c.execute("SELECT * FROM employee")
    # employees = c.fetchall()
    return render_template('report.html')
   

@app.route('/employee/remove_employee', methods=['GET', 'POST'])
def removeEmployee():
    form=NewEmployeeForm()
    return render_template('removeEmployee.html', form=form)


@app.route('/report/employeeinfo', methods=['GET', 'POST'])
def employeeinfo():
    #form=NewEmployeeForm()
    return render_template('employeeinfo.html')


@app.route('/report/payroll', methods=['GET', 'POST'])
def payroll():
    #form=NewEmployeeForm()
    return render_template('payroll.html')


@app.route('/report/tax', methods=['GET', 'POST'])
def tax():
    #form=NewEmployeeForm()
    return render_template('tax.html')

@app.route('/shift', methods=['GET', 'POST'])
def shift():
    #form=NewEmployeeForm()
    return render_template('shift.html')

@app.route('/shift/timecard', methods=['GET', 'POST'])
def timecard():
    #form=NewEmployeeForm()
    return render_template('timecard.html')