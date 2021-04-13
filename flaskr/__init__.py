import os
import sqlite3
from datetime import datetime


from flask import Flask, render_template, url_for, flash, redirect, request
from forms import NewEmployeeForm, update_employee_info_form, remove_employee_form





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
                TODAYS_DATE = datetime.today().strftime('%Y-%m-%d')

                if form.validate_on_submit():
                        
                        if(len(form.employee_middle_name.data) == 0):
                                # no middle name
                                form.employee_middle_name.data = "NULL"
                        
                        conn = sqlite3.connect("instance/flaskr.sqlite")
                        c = conn.cursor()

                        #use next available ID
                        c.execute('''
                                SELECT MAX(EmployeeID)
                                FROM Employee
                                '''
                                )
                        Employee_id_dict = list(c.fetchall())
                        EMPLOYEE_ID = str(int(Employee_id_dict[0][0]) + 1)
                      
                        #Add the new employee into the 'Employee' table
                        query = 'insert into Employee VALUES (?, ?, ?, ?, ?, ?, ?,?)'
                        c.execute(query, (EMPLOYEE_ID,
                                form.employee_SIN.data,
                                form.employee_date_of_birth.data,
                                TODAYS_DATE,
                                form.employee_first_name.data,
                                form.employee_middle_name.data,
                                form.employee_last_name.data,
                                form.employee_Address.data))
                        
                        if (form.employee_role.data == "office"):
                                # add to office table
                                query = 'insert into Office VALUES (?, ?)'
                                c.execute(query, (EMPLOYEE_ID, int(form.employee_salary.data)))
                        
                        else:
                                # add to operations table
                                query = 'insert into Operations VALUES (?, ?)'
                                c.execute(query, (EMPLOYEE_ID, float(form.employee_salary.data)))

                        # Add thier Phone Number
                        query = 'insert into Phone values (?,?)'
                        c.execute(query, (form.employee_phone.data, EMPLOYEE_ID) )

                
                        conn.commit()
                        c.close()

                        flash(f'{form.employee_first_name.data} {form.employee_last_name.data}: added to database', 'success')
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
                form=remove_employee_form()
                if form.validate_on_submit():
                        conn = sqlite3.connect("instance/flaskr.sqlite")
                        c = conn.cursor()

                        #Remove the employee from the 'employee' table
                        query = 'DELETE FROM employee WHERE lname=(?)'
                        c.execute(query, (
                        form.employee_last_name.data,
                        )) #Execute the query
                        conn.commit() #Commit the changes
                        flash(f'employee {form.employee_last_name.data} removed from db', 'success')
                        # flash("New employee added to database successfully")
                        return redirect(url_for('removeEmployee'))
                
                return render_template('removeEmployee.html', form=form)

        @app.route('/report/employeeinfo', methods=['GET', 'POST'])
        def employeeinfo():
                conn = sqlite3.connect("instance/flaskr.sqlite")
                conn.row_factory = dict_factory
                cur = conn.cursor()
                # display operations employees
                cur.execute('''
                        SELECT E.*, P.PhoneNumber
                        FROM Operations O, Employee E, Phone P
                        WHERE O.ID = E.EmployeeID AND P.ID = E.EmployeeID AND O.ID = P.ID
                               ''')
                operations = cur.fetchall()

                #display office employees
                cur.execute('''
                        SELECT E.*, P.PhoneNumber  
                        FROM Office O, Employee E, Phone P
                        WHERE O.ID = E.EmployeeID AND P.ID = E.EmployeeID AND O.ID = P.ID
                               ''')
                offices = cur.fetchall()
                
                conn.commit()
                cur.close()

                return render_template('employeeinfo.html', operations=operations, offices=offices,
                                        office_len=len(offices), operations_len=len(operations))


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