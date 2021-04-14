import os
import sqlite3
from datetime import datetime


from flask import Flask, render_template, url_for, flash, redirect, request
from forms import NewEmployeeForm, update_employee_info_form, RemoveEmployeeForm, PayrollForm, ContactForm, RemoveContactForm



TODAYS_DATE = datetime.today().strftime('%Y-%m-%d')

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
                # form=()
                
                return render_template('employee.html')

        @app.route('/employee/add_new_employee', methods=['GET', 'POST'])
        def add_new_employee():
                form=NewEmployeeForm()
                
                global TODAYS_DATE 
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


                        # format phone number to: (xxx) xxx-xxxx
                        tmp = form.employee_phone.data
                        first = tmp[0:3]
                        second = tmp[3:6]
                        third = tmp[6:10]
                        format_number = "(" + first + ") " + second + "-" + third
                        

                        # Add their Phone Number
                        query = 'insert into Phone values (?,?)'
                        c.execute(query, (format_number, EMPLOYEE_ID) )

                
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
                form = RemoveEmployeeForm()
                conn = sqlite3.connect("instance/flaskr.sqlite")
                conn.row_factory = dict_factory
                cur = conn.cursor()

                # get emergency contact info
                cur.execute('''
                                SELECT E1.*
                                FROM Operations O, Employee E1
                                WHERE O.ID = E1.EmployeeID
                                UNION
                                SELECT E2.*
                                FROM Office Of, Employee E2
                                WHERE Of.ID = E2.EmployeeID
                                ORDER BY E2.Lname ASC

                        ''')
                employees = cur.fetchall()

                if form.validate_on_submit():
                        selected_employees = request.form.getlist('chkb')
                        for e in selected_employees:
                                #remove selected employees 
                                query = "DELETE FROM Employee WHERE EmployeeID = ?"
                                cur.execute(query,(e))

                        conn.commit()
                        cur.close()
                        return redirect(url_for('removeEmployee'))
                
                return render_template('removeEmployee.html', form=form, employees = employees)

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
                        ORDER BY UPPER(E.Lname) ASC
                               ''')
                operations = cur.fetchall()

                #display office employees
                cur.execute('''
                        SELECT E.*, P.PhoneNumber  
                        FROM Office O, Employee E, Phone P
                        WHERE O.ID = E.EmployeeID AND P.ID = E.EmployeeID AND O.ID = P.ID
                        ORDER BY UPPER(E.Lname) ASC
                               ''')
                offices = cur.fetchall()
                
                conn.commit()
                cur.close()

                return render_template('employeeinfo.html', operations=operations, offices=offices,
                                        office_len=len(offices), operations_len=len(operations))


        @app.route('/report/payroll', methods=['GET', 'POST'])
        def payroll():
                global TODAYS_DATE
                form = PayrollForm()
                conn = sqlite3.connect("instance/flaskr.sqlite")
                conn.row_factory = dict_factory
                cur = conn.cursor()

                # Populate drop down dynamically
                cur.execute(''' SELECT EmployeeID, Fname, Lname FROM Employee''')
                employees = cur.fetchall()
                employees_list=[(employee['Fname'] + " " + employee['Lname']) for employee in employees]
                employees_list.insert(0,"")
                form.employee_filter.choices = employees_list
                if form.validate_on_submit():
                        query = '''SELECT E.Fname, E.Lname, P.ChequeNumber, P.PayrollDate, P.GrossPay
                                FROM Employee E, Payroll P
                                WHERE P.ID = E.EmployeeID AND E.Fname = ? AND E.Lname = ? AND P.PayrollDate between ? and ? LIMIT ?'''
                        
                        fname = form.employee_filter.data.split(" ")[0]
                        lname = form.employee_filter.data.split(" ")[1]
                        if (form.payroll_date_range.data == "YTD"):
                                #Show pay stubs from start of year
                                start = TODAYS_DATE[0:4] + "-01-01"
                                end = TODAYS_DATE
                                limit = 100
                        else:
                                #Show up to the last 25 stubs
                                start = "2000-01-01"
                                end = TODAYS_DATE
                                limit = 25
                        cur.execute(query, (fname,lname,start ,end ,limit))
                        stubs = cur.fetchall()


                        query = '''SELECT SUM(P.GrossPay)
                                FROM Employee E, Payroll P
                                WHERE P.ID = E.EmployeeID AND E.Fname = ? AND E.Lname = ? AND P.PayrollDate between ? and ? LIMIT ?'''
                        cur.execute(query, (fname,lname,start ,end ,limit))

                        gross_pay = cur.fetchall()
                        conn.commit()
                        cur.close()

                        return render_template('payroll_data.html', stubs = stubs, gross_pay = gross_pay[0]['SUM(P.GrossPay)'])  
                return render_template('payroll.html', form = form)


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

        @app.route('/emergency', methods=['GET', 'POST'])
        def emergency():
                connection = sqlite3.connect("instance/flaskr.sqlite")
                connection.row_factory = dict_factory
                cur = connection.cursor()

                # get emergency contact info
                cur.execute('''
                                SELECT EC.ContactName, EC.PhoneNumber, 
                                EC.Relation, E.Fname, E.Lname
                                FROM EmergencyContact EC, Employee E 
                                WHERE EC.ID = E.EmployeeID 
                                ORDER BY E.Lname, E.Fname ASC
                         ''')
                emergency_contacts = cur.fetchall()

                connection.commit()
                cur.close()
                return render_template('emergency.html',  emergency_contacts = emergency_contacts)
        
        @app.route('/add_emergency_contact', methods=['GET', 'POST'])
        def add_emergency_contact():
                form =  ContactForm()

                # open database connection
                conn = sqlite3.connect("instance/flaskr.sqlite")
                conn.row_factory = dict_factory
                cur = conn.cursor()

                # Populate drop down dynamically
                cur.execute(''' SELECT EmployeeID, Fname, Lname FROM Employee''')
                employees = cur.fetchall()
                employees_list=[(employee['Fname'] + " " + employee['Lname']) for employee in employees]
                employees_list.insert(0,"")
                form.emergency_contact_employee.choices = employees_list

                if form.validate_on_submit():
                        fname = form.emergency_contact_employee.data.split(" ")[0]
                        lname = form.emergency_contact_employee.data.split(" ")[1]
                        query = '''
                                SELECT E.EmployeeID
                                FROM Employee E
                                WHERE Fname = ? AND Lname = ? 
                                '''
                        cur.execute(query,(fname,lname))
                        ID = cur.fetchall()[0]['EmployeeID']
                        
                        # format phone number to: (xxx) xxx-xxxx
                        tmp = form.emergency_contact_phone.data
                        first = tmp[0:3]
                        second = tmp[3:6]
                        third = tmp[6:10]
                        format_number = "(" + first + ") " + second + "-" + third

                        query = '''
                                INSERT INTO EmergencyContact VALUES(?,?,?,?) 
                                '''
                        cur.execute(query, (form.emergency_contact_name.data, format_number , 
                                             form.emergency_contact_relation.data, ID))
                        
                        conn.commit()
                        cur.close()

                        flash(f'{form.emergency_contact_name.data}: added as Emergency Contact for {form.emergency_contact_employee.data}', 'success')
                        return redirect(url_for('add_emergency_contact'))


                return(render_template('add_emergency_contact.html', form = form))

        
        @app.route('/delete_emergency_contact', methods=['GET', 'POST'])
        def delete_emergency_contact():
                form = RemoveContactForm()
                connection = sqlite3.connect("instance/flaskr.sqlite")
                connection.row_factory = dict_factory
                cur = connection.cursor()

                # get emergency contact info
                cur.execute('''
                                SELECT EC.ContactName, EC.PhoneNumber, 
                                EC.Relation, E.Fname, E.Lname
                                FROM EmergencyContact EC, Employee E 
                                WHERE EC.ID = E.EmployeeID 
                                ORDER BY E.Lname, E.Fname ASC
                        ''')
                emergency_contacts = cur.fetchall()

                if form.validate_on_submit():
                        selected_contacts = request.form.getlist('chk')

                        #loop over selected employees removing each one
                        for c in selected_contacts:
                                contact_name = c.split("+")[0]
                                employee_Fname = c.split("+")[1]
                                employee_Lname = c.split("+")[2]

                                # find the ID to remove
                                query = "SELECT E.EmployeeID FROM Employee E WHERE E.Fname = ? AND E.Lname =?"
                                cur.execute(query,(employee_Fname, employee_Lname))
                                ID = cur.fetchall()[0]['EmployeeID']
                                print(ID)
                                # delete contact
                                query = '''DELETE FROM EmergencyContact 
                                        WHERE ContactName = ? AND ID = ?  '''
                                cur.execute(query,(contact_name, ID))


                        connection.commit()
                        cur.close()
                        
                        return(redirect(url_for('emergency')))

                return(render_template('delete_emergency_contact.html', form = form, emergency_contacts = emergency_contacts))



        

        from . import db
        db.init_app(app)

        return(app)