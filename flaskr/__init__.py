import os
import sqlite3

from flask import Flask, render_template, url_for, flash, redirect, request
from forms import NewEmployeeForm, update_employee_info_form


def create_app(test_config=None):
        # create and configure the app
        app = Flask(__name__, instance_relative_config=True)
        app.config.from_mapping(
                SECRET_KEY='cmpt354',
                DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        )

        if test_config is None:
                # load the instance config, if it exists, when not testing
                app.config.from_pyfile('config.py', silent=True)
        else:
                # load the test config if passed in
                app.config.from_mapping(test_config)

        # ensure the instance folder exists
        try:
                os.makedirs(app.instance_path)
        except OSError:
                pass
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
                # form=NewEmployeeForm()
                
                return render_template('employee.html')

        @app.route('/employee/add_new_employee', methods=['GET', 'POST'])
        def add_new_employee():
                form=NewEmployeeForm()
                if form.validate_on_submit():
                        conn = sqlite3.connect("instance/flaskr.sqlite")
                        c = conn.cursor()
                        #Add the new employee into the 'employee' table
                        query = 'insert into employee VALUES (?, ?, ?,?)'
                        c.execute(query, (form.employee_first_name.data, 
                        form.employee_last_name.data, 
                        form.employee_middle_name.data,
                        form.employee_role.data)) #Execute the query
                        conn.commit() #Commit the changes
                        flash(f'New employee {form.employee_first_name.data} added to db', 'success')
                        # flash("New employee added to database successfully")
                        return redirect(url_for('add_new_employee'))
                return render_template('add_new_employee.html',form=form)

        @app.route('/employee/update_employee_info', methods=['GET', 'POST'])
        def update_employee_info():
                form=update_employee_info_form()
                return render_template('update_employee_info.html',form=form)

        @app.route('/report')
        def report():
                return render_template('report.html')
        

        @app.route('/employee/remove_employee', methods=['GET', 'POST'])
        def removeEmployee():
                form=NewEmployeeForm()
                return render_template('removeEmployee.html', form=form)

        @app.route('/report/employeeinfo', methods=['GET', 'POST'])
        def employeeinfo():
                conn = sqlite3.connect("instance/flaskr.sqlite")
                conn.row_factory = dict_factory
                cur = conn.cursor()
                cur.execute('''SELECT * FROM employee''')
                employees = cur.fetchall()
                cur.execute('''SELECT employee_role, COUNT(*)  
                FROM employee 
                GROUP BY employee_role''')
                number_of_employees = cur.fetchall()
                #print(number_of_employees[0]['COUNT(*)'])
                conn.commit()
                cur.close()
                # return str(number_of_employees)
                # return str(len(employees))

                return render_template('employeeinfo.html', employees=employees,
                number_of_employees=number_of_employees)


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
        
        from . import db
        db.init_app(app)


        return(app)