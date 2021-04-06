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

        @app.route('/')
        def index():
                return render_template('index.html')

        @app.route('/employee', methods=['GET', 'POST'])
        def employee():
                form=NewEmployeeForm()
                conn = sqlite3.connect("instance/flaskr.sqlite")
                cur = conn.cursor()
                cur.execute('''SELECT * FROM employee''')
                rv = cur.fetchall()
                conn.commit()
                cur.close()
                return str(rv)
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
                return render_template('report.html')
        

        @app.route('/employee/remove_employee', methods=['GET', 'POST'])
        def removeEmployee():
                form=NewEmployeeForm()
                return render_template('removeEmployee.html', form=form)
        
        from . import db
        db.init_app(app)


        return(app)