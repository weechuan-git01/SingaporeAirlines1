import Employee, Employer, Listings, Airplane, Customer, Flight, Ticket
import shelve
import os
import sys
import MySQLdb.cursors
import bcrypt

from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory, session, g, flash
from flask_mysqldb import MySQL
from cryptography.fernet import Fernet

from Forms import CreateEmployeeForm, CreateEmployerForm, CreateListingForm, CreateAirplanesForm, CreatePassengerForm, \
    CreateFlightForm, CreateMaintenanceForm, RegisterForm, LoginForm, FilterStatus, FilterRole, ChangePassword, \
    BookTicketForm, ForgetPassword

from datetime import date, datetime

from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = 'static/employer_logo'
app.secret_key = 'any_random_string'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Fccfxx322399'
app.config['MYSQL_DB'] = 'sia'

mysql = MySQL(app)

@app.before_request
def before_request():
    if 'username' in session:
        g.user = session['username']
    else:
        g.user = None
    print(g.user)


@app.route('/')
def home():
    return render_template('index.html')


# @app.route('/userHome')
# def user_home():
#     try:
#         passengers_dict = {}
#         db = shelve.open('passenger.db', 'r')
#         passengers_dict = db['Passengers']
#         db.close()
#
#         tickets_dict = {}
#         db3 = shelve.open('ticket.db', 'r')
#         tickets_dict = db3['Tickets']
#         db3.close()
#
#         flights_dict = {}
#         db2 = shelve.open('flight.db','r')
#         flights_dict = db2['Flights']
#         db2.close()
#
#     except IOError:
#         print('Error in retrieving employers.db')
#     except:
#         print("Error in retrieving Employers from employers.db.")
#     else:
#         passengers_list = []
#         tickets_list = []
#         flights_list = []
#         for key in passengers_dict:
#             passenger = passengers_dict.get(key)
#             # passengers_list.append(passenger)
#             if passenger.get_nric() == 'S9733462E':  # (session id)
#                 passengers_list.append(passenger)
#
#         for key in tickets_dict:
#             ticket = tickets_dict.get(key)
#             tickets_list.append(ticket)
#
#         for key in flights_dict:
#             flight = flights_dict.get(key)
#             flights_list.append(flight)
#
#         return render_template('user.html', passengers_list=passengers_list, tickets_list=tickets_list, flights_list=flights_list)

@app.route('/userHome')
def user_home():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM customer WHERE id = %s', (session['id'],))
        customer = cursor.fetchone()
        return render_template('user.html', customer = customer)
    return redirect(url_for('login'))

@app.route('/adminHome')
def admin_home():
    return render_template('index2.html')


@app.route('/companyHome')
def company_home():
    try:
        employers_dict = {}
        db = shelve.open('employers.db', 'r')
        employers_dict = db['Employers']
        db.close()

        listings_dict = {}
        db3 = shelve.open('listings.db', 'r')
        listings_dict = db3['Listings']
        db3.close()
    except IOError:
        print('Error in retrieving employers.db')
    except:
        print("Error in retrieving Employers from employers.db.")
    else:
        employers_list = []
        for key in employers_dict:
            employer = employers_dict.get(key)
            if employer.get_company_name() == 'Jumbo Group':
                employers_list.append(employer)
                session['employer_name'] = employer.get_company_name()
                session['employer_id'] = employer.get_employer_id()

        listings_list = []
        for key in listings_dict:
            listings = listings_dict.get(key)
            listings_list.append(listings)
        return render_template('company.html', employers_list=employers_list, company_name=session['employer_name'],
                               company_id=session['employer_id'], count=len(listings_list), listings_list=listings_list)


@app.route('/employeeHome')
def employee_home():
    try:
        employees_dict = {}
        db2 = shelve.open('employees.db', 'r')
        employees_dict = db2['Employees']
        db2.close()

    except IOError:
        print('Error in retrieving employees.db')
    except:
        print("Error in retrieving Employees from employers.db.")
    else:
        employees_list = []
        for key in employees_dict:
            employee = employees_dict.get(key)
            if employee.get_first_name() == 'Catherine':
                employees_list.append(employee)
                session['employee_name'] = employee.get_first_name()
                session['employee_id'] = employee.get_employee_id()

        return render_template('employee.html', employees_list=employees_list, name=session['employee_name'],
                               id=session['employee_id'])


# @app.route('/employeeChat')
# def employee_chat():
#     return render_template('employeeChat.html')


@app.route('/createEmployee', methods=['GET', 'POST'])
def create_employee():
    create_employee_form = CreateEmployeeForm(request.form)
    if request.method == 'POST' and create_employee_form.validate():
        employees_dict = {}
        db2 = shelve.open('employees.db', 'c')

        try:
            employees_dict = db2['Employees']

        except IOError:
            print('Error in retrieving employees.db')
        except:
            print("Error in retrieving Employees from employees.db.")
        else:
            current_id = 0
            for id in employees_dict:
                if current_id <= id < sys.maxsize:
                    current_id = id

                else:
                    current_id = 0

            Employee.Employee.count_id = current_id
            employee = Employee.Employee(
                create_employee_form.first_name.data, create_employee_form.last_name.data,
                create_employee_form.birthdate.data,
                create_employee_form.gender.data, create_employee_form.nationality.data,
                create_employee_form.photo.data,
                create_employee_form.role.data, create_employee_form.employment_status.data,
                create_employee_form.job_start_date.data,
                create_employee_form.level_of_education.data,
                create_employee_form.major.data, create_employee_form.school.data,
                create_employee_form.graduation_date.data, create_employee_form.address.data,
                create_employee_form.mobile_contact.data,
                create_employee_form.home_contact.data,
                create_employee_form.email.data, create_employee_form.remarks.data)

            str_birthdate = str(create_employee_form.birthdate.data.day) + str(
                create_employee_form.birthdate.data.month) + str(create_employee_form.birthdate.data.year)
            employee.set_login_id(str_birthdate)
            employee.set_password(str_birthdate)

            today = date.today()
            age = today.year - employee.get_birthdate().year
            print(age)
            employee.set_age(age)

            year_of_service = today.year - employee.get_job_start_date().year
            employee.set_year_of_service(year_of_service)

            timestamp_datetime = datetime.now()
            timestamp_date = timestamp_datetime.date()
            print(timestamp_datetime)
            employee.set_timestamp(timestamp_date)

            if create_employee_form.employment_status.data == 'R':
                employee.set_job_end_date(timestamp_date)
                years_of_service = employee.get_job_end_date().year - employee.get_job_start_date().year
                employee.set_year_of_service(years_of_service)

            employees_dict[employee.get_employee_id()] = employee
            db2['Employees'] = employees_dict
            db2.close()

            return redirect(url_for('retrieve_employees'))
    return render_template('createEmployee.html', form=create_employee_form)


@app.route('/employedFilter', methods=['GET', 'POST'])
def employed_filter():
    filterstatus = FilterStatus(request.form)
    employees_dict = {}
    db2 = shelve.open('employees.db', 'r')
    employees_dict = db2['Employees']
    db2.close()

    employees_list = []
    employed_list = []
    for key in employees_dict:
        employee = employees_dict.get(key)
        employees_list.append(employee)
        if employee.get_employment_status() == 'E':
            employed_list.append(employee)

    if request.method == 'POST' and filterstatus.validate():
        var = filterstatus.filter.data
        if var == 'All':
            return redirect(url_for('retrieve_employees'))
        elif var == 'E':
            return redirect(url_for('employed_filter'))
        elif var == 'R':
            return redirect(url_for('retrenched_filter'))
        elif var == 'Resigned':
            return redirect(url_for('resigned_filter'))

    return render_template('employedFilter.html', count=len(employed_list), employees_list=employees_list,
                           form=filterstatus, employed_list=employed_list)


@app.route('/retrenchedFilter', methods=['GET', 'POST'])
def retrenched_filter():
    filterstatus = FilterStatus(request.form)
    employees_dict = {}
    db2 = shelve.open('employees.db', 'r')
    employees_dict = db2['Employees']
    db2.close()

    employees_list = []
    retrenched_list = []
    for key in employees_dict:
        employee = employees_dict.get(key)
        employees_list.append(employee)
        if employee.get_employment_status() == 'R':
            retrenched_list.append(employee)

    if request.method == 'POST' and filterstatus.validate():
        var = filterstatus.filter.data
        if var == 'All':
            return redirect(url_for('retrieve_employees'))
        elif var == 'E':
            return redirect(url_for('employed_filter'))
        elif var == 'R':
            return redirect(url_for('retrenched_filter'))
        elif var == 'Resigned':
            return redirect(url_for('resigned_filter'))

    return render_template('retrenchedFilter.html', count=len(retrenched_list), employees_list=employees_list,
                           form=filterstatus, retrenched_list=retrenched_list)


@app.route('/resignedFilter', methods=['GET', 'POST'])
def resigned_filter():
    filterstatus = FilterStatus(request.form)
    employees_dict = {}
    db2 = shelve.open('employees.db', 'r')
    employees_dict = db2['Employees']
    db2.close()

    employees_list = []
    resigned_list = []
    for key in employees_dict:
        employee = employees_dict.get(key)
        employees_list.append(employee)
        if employee.get_employment_status() == 'Resigned':
            resigned_list.append(employee)

    if request.method == 'POST' and filterstatus.validate():
        var = filterstatus.filter.data
        if var == 'All':
            return redirect(url_for('retrieve_employees'))
        elif var == 'E':
            return redirect(url_for('employed_filter'))
        elif var == 'R':
            return redirect(url_for('retrenched_filter'))
        elif var == 'Resigned':
            return redirect(url_for('resigned_filter'))

    return render_template('resignedFilter.html', count=len(resigned_list), employees_list=employees_list,
                           form=filterstatus, resigned_list=resigned_list)


@app.route('/retrieveEmployees', methods=['GET', 'POST'])
def retrieve_employees():
    try:
        filterstatus = FilterStatus(request.form)
        employees_dict = {}
        db2 = shelve.open('employees.db', 'r')
        employees_dict = db2['Employees']
        db2.close()


    except IOError:
        print('Error in retrieving employees.db')
    except:
        print("Error in retrieving Employees from employees.db.")
    else:
        employees_list = []
        employed_list = []
        retrenched_list = []
        resigned_list = []
        for key in employees_dict:
            employee = employees_dict.get(key)
            employees_list.append(employee)
            if employee.get_employment_status() == 'E':
                employed_list.append(employee)
            elif employee.get_employment_status() == 'R':
                retrenched_list.append(employee)
            elif employee.get_employment_status() == 'Resigned':
                resigned_list.append(employee)

        if request.method == 'POST' and filterstatus.validate():
            var = filterstatus.filter.data
            if var == 'All':
                return redirect(url_for('retrieve_employees'))
            elif var == 'E':
                return redirect(url_for('employed_filter'))
            elif var == 'R':
                return redirect(url_for('retrenched_filter'))
            elif var == 'Resigned':
                return redirect(url_for('resigned_filter'))

        return render_template('retrieveEmployees.html', count=len(employees_list), employees_list=employees_list,
                               form=filterstatus)


@app.route('/updateEmployee/<int:id>/', methods=['GET', 'POST'])
def update_employee(id):
    update_employee_form = CreateEmployeeForm(request.form)
    if request.method == 'POST' and update_employee_form.validate():
        employees_dict = {}
        db2 = shelve.open('employees.db', 'w')
        try:
            employees_dict = db2['Employees']
        except IOError:
            print('Error in retrieving employees.db')
        except:
            print("Error in retrieving Employees from employees.db.")
        else:
            employee = employees_dict.get(id)
            # employee.set_login_id(update_employee_form.login_id.data)
            # employee.set_password(update_employee_form.password.data)
            employee.set_first_name(update_employee_form.first_name.data)
            employee.set_last_name(update_employee_form.last_name.data)
            employee.set_birthdate(update_employee_form.birthdate.data)
            employee.set_gender(update_employee_form.gender.data)
            employee.set_nationality(update_employee_form.nationality.data)
            employee.set_photo(update_employee_form.photo.data)
            employee.set_role(update_employee_form.role.data)
            employee.set_employment_status(update_employee_form.employment_status.data)
            employee.set_job_start_date(update_employee_form.job_start_date.data)
            employee.set_level_of_education(update_employee_form.level_of_education.data)
            employee.set_major(update_employee_form.major.data)
            employee.set_school(update_employee_form.school.data)
            employee.set_address(update_employee_form.address.data)
            employee.set_graduation_date(update_employee_form.graduation_date.data)
            employee.set_mobile_contact(update_employee_form.mobile_contact.data)
            employee.set_home_contact(update_employee_form.home_contact.data)
            employee.set_email(update_employee_form.email.data)
            employee.set_remarks(update_employee_form.remarks.data)

            db2['Employees'] = employees_dict
            db2.close()

            return redirect(url_for('retrieve_employees'))
    else:
        try:
            employees_dict = {}
            db2 = shelve.open('employees.db', 'r')
            employees_dict = db2['Employees']
            db2.close()
        except IOError:
            print('Error in retrieving employees.db')
        except:
            print("Error in retrieving Employees from employees.db.")
        else:
            employee = employees_dict.get(id)

            # update_employee_form.login_id.data = employee.get_login_id()
            # update_employee_form.password.data = employee.get_password()
            update_employee_form.first_name.data = employee.get_first_name()
            update_employee_form.last_name.data = employee.get_last_name()
            update_employee_form.birthdate.data = employee.get_birthdate()
            update_employee_form.gender.data = employee.get_gender()
            update_employee_form.nationality.data = employee.get_nationality()
            update_employee_form.photo.data = employee.get_photo()
            update_employee_form.role.data = employee.get_role()
            update_employee_form.employment_status.data = employee.get_employment_status()
            update_employee_form.job_start_date.data = employee.get_job_start_date()
            update_employee_form.level_of_education.data = employee.get_level_of_education()
            update_employee_form.major.data = employee.get_major()
            update_employee_form.school.data = employee.get_school()
            update_employee_form.graduation_date.data = employee.get_graduation_date()
            update_employee_form.address.data = employee.get_address()
            update_employee_form.mobile_contact.data = employee.get_mobile_contact()
            update_employee_form.home_contact.data = employee.get_home_contact()
            update_employee_form.email.data = employee.get_email()
            update_employee_form.remarks.data = employee.get_remarks()

            return render_template('updateEmployee.html', form=update_employee_form)


@app.route('/resignEmployee/<int:id>', methods=['POST'])
def resign_employee(id):
    employees_dict = {}
    db2 = shelve.open('employees.db', 'w')
    try:
        employees_dict = db2['Employees']
    except IOError:
        print('Error in retrieving employees.db')
    except:
        print("Error in retrieving Employees from employees.db.")
    else:

        employee = employees_dict.get(id)
        employee.set_employment_status('Resigned')

        timestamp_datetime = datetime.now()
        timestamp_date = timestamp_datetime.date()
        print(timestamp_datetime)
        employee.set_job_end_date(timestamp_date)

        db2['Employees'] = employees_dict
        db2.close()
        return redirect(url_for('retrieve_employees'))


@app.route('/deleteEmployee/<int:id>', methods=['POST'])
def delete_employee(id):
    employees_dict = {}
    db = shelve.open('employees.db', 'w')
    try:
        employees_dict = db['Employees']
    except IOError:
        print('Error in retrieving employers.db')
    except:
        print("Error in retrieving Employers from employers.db.")
    else:
        employees_dict.pop(id)

        db['Employees'] = employees_dict
        db.close()

        return redirect(url_for('retrieve_employees'))


@app.route('/matchEmployees', methods=['GET', 'POST'])
def match_employees():
    try:
        filterrole = FilterRole(request.form)
        employees_dict = {}
        db = shelve.open('employees.db', 'r')
        employees_dict = db['Employees']
        db.close()

    except IOError:
        print('Error in retrieving employees.db')
    except:
        print("Error in retrieving Employees from employees.db.")
    else:
        employees_list = []
        admin_list = []
        crew_list = []
        maintenance_list = []
        flights_list = []
        declaration_list = []
        for key in employees_dict:
            employee = employees_dict.get(key)
            if employee.get_employment_status() != 'Resigned' and employee.get_employment_status() != 'E':
                employees_list.append(employee)
                if employee.get_role() == 'A':
                    admin_list.append(employee)
                elif employee.get_role() == 'C':
                    crew_list.append(employee)
                elif employee.get_role() == 'M':
                    maintenance_list.append(employee)
                elif employee.get_role() == 'F':
                    flights_list.append(employee)
                elif employee.get_role() == 'D':
                    declaration_list.append(employee)

        if request.method == 'POST' and filterrole.validate():
            var = filterrole.filter.data
            if var == 'All':
                return redirect(url_for('match_employees'))
            elif var == 'C':
                return redirect(url_for('crew_filter'))
            elif var == 'A':
                return redirect(url_for('admin_filter'))
            elif var == 'M':
                return redirect(url_for('maintenance_filter'))
            elif var == 'F':
                return redirect(url_for('flights_filter'))
            elif var == 'D':
                return redirect(url_for('declaration_filter'))

        return render_template('matchEmployees.html', count=len(employees_list), employees_list=employees_list,
                               form=filterrole)


@app.route('/crewFilter', methods=['GET', 'POST'])
def crew_filter():
    filterrole = FilterRole(request.form)
    employees_dict = {}
    db2 = shelve.open('employees.db', 'r')
    employees_dict = db2['Employees']
    db2.close()

    employees_list = []
    crew_list = []
    for key in employees_dict:
        employee = employees_dict.get(key)
        employees_list.append(employee)
        if employee.get_role() == 'C' and employee.get_employment_status() == 'R':
            crew_list.append(employee)

    if request.method == 'POST' and filterrole.validate():
        var = filterrole.filter.data
        if var == 'All':
            return redirect(url_for('match_employees'))
        elif var == 'C':
            return redirect(url_for('crew_filter'))
        elif var == 'A':
            return redirect(url_for('admin_filter'))
        elif var == 'M':
            return redirect(url_for('maintenance_filter'))
        elif var == 'F':
            return redirect(url_for('flights_filter'))
        elif var == 'D':
            return redirect(url_for('declaration_filter'))

    return render_template('crewFilter.html', count=len(crew_list), employees_list=employees_list,
                           form=filterrole, crew_list=crew_list)


@app.route('/adminFilter', methods=['GET', 'POST'])
def admin_filter():
    filterrole = FilterRole(request.form)
    employees_dict = {}
    db2 = shelve.open('employees.db', 'r')
    employees_dict = db2['Employees']
    db2.close()

    employees_list = []
    admin_list = []
    for key in employees_dict:
        employee = employees_dict.get(key)
        employees_list.append(employee)
        if employee.get_role() == 'A' and employee.get_employment_status() == 'R':
            admin_list.append(employee)

    if request.method == 'POST' and filterrole.validate():
        var = filterrole.filter.data
        if var == 'All':
            return redirect(url_for('match_employees'))
        elif var == 'C':
            return redirect(url_for('crew_filter'))
        elif var == 'A':
            return redirect(url_for('admin_filter'))
        elif var == 'M':
            return redirect(url_for('maintenance_filter'))
        elif var == 'F':
            return redirect(url_for('flights_filter'))
        elif var == 'D':
            return redirect(url_for('declaration_filter'))

    return render_template('adminFilter.html', count=len(admin_list), employees_list=employees_list,
                           form=filterrole, admin_list=admin_list)


@app.route('/maintenanceFilter', methods=['GET', 'POST'])
def maintenance_filter():
    filterrole = FilterRole(request.form)
    employees_dict = {}
    db2 = shelve.open('employees.db', 'r')
    employees_dict = db2['Employees']
    db2.close()

    employees_list = []
    maintenance_list = []
    for key in employees_dict:
        employee = employees_dict.get(key)
        employees_list.append(employee)
        if employee.get_role() == 'M' and employee.get_employment_status() == 'R':
            maintenance_list.append(employee)

    if request.method == 'POST' and filterrole.validate():
        var = filterrole.filter.data
        if var == 'All':
            return redirect(url_for('match_employees'))
        elif var == 'C':
            return redirect(url_for('crew_filter'))
        elif var == 'A':
            return redirect(url_for('admin_filter'))
        elif var == 'M':
            return redirect(url_for('maintenance_filter'))
        elif var == 'F':
            return redirect(url_for('flights_filter'))
        elif var == 'D':
            return redirect(url_for('declaration_filter'))

    return render_template('maintenanceFilter.html', count=len(maintenance_list), employees_list=employees_list,
                           form=filterrole, maintenance_list=maintenance_list)


@app.route('/flightsFilter', methods=['GET', 'POST'])
def flights_filter():
    filterrole = FilterRole(request.form)
    employees_dict = {}
    db2 = shelve.open('employees.db', 'r')
    employees_dict = db2['Employees']
    db2.close()

    employees_list = []
    flights_list = []
    for key in employees_dict:
        employee = employees_dict.get(key)
        employees_list.append(employee)
        if employee.get_role() == 'F' and employee.get_employment_status() == 'R':
            flights_list.append(employee)

    if request.method == 'POST' and filterrole.validate():
        var = filterrole.filter.data
        if var == 'All':
            return redirect(url_for('match_employees'))
        elif var == 'C':
            return redirect(url_for('crew_filter'))
        elif var == 'A':
            return redirect(url_for('admin_filter'))
        elif var == 'M':
            return redirect(url_for('maintenance_filter'))
        elif var == 'F':
            return redirect(url_for('flights_filter'))
        elif var == 'D':
            return redirect(url_for('declaration_filter'))

    return render_template('flightsFilter.html', count=len(flights_list), employees_list=employees_list,
                           form=filterrole, flights_list=flights_list)


@app.route('/declarationFilter', methods=['GET', 'POST'])
def declaration_filter():
    filterrole = FilterRole(request.form)
    employees_dict = {}
    db2 = shelve.open('employees.db', 'r')
    employees_dict = db2['Employees']
    db2.close()

    employees_list = []
    declaration_list = []
    for key in employees_dict:
        employee = employees_dict.get(key)
        employees_list.append(employee)
        if employee.get_role() == 'D' and employee.get_employment_status() == 'R':
            declaration_list.append(employee)

    if request.method == 'POST' and filterrole.validate():
        var = filterrole.filter.data
        if var == 'All':
            return redirect(url_for('match_employees'))
        elif var == 'C':
            return redirect(url_for('crew_filter'))
        elif var == 'A':
            return redirect(url_for('admin_filter'))
        elif var == 'M':
            return redirect(url_for('maintenance_filter'))
        elif var == 'F':
            return redirect(url_for('flights_filter'))
        elif var == 'D':
            return redirect(url_for('declaration_filter'))

    return render_template('declarationFilter.html', count=len(declaration_list), employees_list=employees_list,
                           form=filterrole, declaration_list=declaration_list)


@app.route('/selectEmployee/<int:id>', methods=['POST'])
def select_employee(id):
    employees_dict = {}
    db2 = shelve.open('employees.db', 'w')
    try:
        employees_dict = db2['Employees']
    except IOError:
        print('Error in retrieving employees.db')
    except:
        print("Error in retrieving Employees from employees.db.")
    else:

        employee = employees_dict.get(id)
        employee.set_match('Matched')
        print(employee.get_match())
        employee.set_no_of_matches(employee.get_no_of_matches() + 1)
        print(employee.get_no_of_matches())

        db2['Employees'] = employees_dict
        db2.close()
        return redirect(url_for('match_employees'))


@app.route('/matchedEmployees')
def matched_employees():
    employees_dict = {}
    db2 = shelve.open('employees.db', 'r')
    employees_dict = db2['Employees']
    db2.close()

    matched_employees_list = []
    for key in employees_dict:
        employee = employees_dict.get(key)
        if employee.get_match() == 'Matched':
            matched_employees_list.append(employee)

    return render_template('matchedEmployees.html', count=len(matched_employees_list),
                           matched_employees_list=matched_employees_list)


# @app.route('/employeePassword', methods=['GET', 'POST'])
# def update_employee_pw(id):
#     update_employee_pw_form = ChangePassword(request.form)
#     if request.method == 'POST' and update_employee_pw_form.validate():
#         employees_dict = {}
#         db2 = shelve.open('employees.db', 'w')
#         try:
#             employees_dict = db2['Employees']
#         except IOError:
#             print('Error in retrieving employees.db')
#         except:
#             print("Error in retrieving Employees from employees.db.")
#         else:
#             employee = employees_dict.get(id)
#             if update_employee_pw_form.current_password.data == employee.get_password():
#                 employee.set_password(update_employee_pw_form.new_password.data)
#                 print(employee.get_password())
#
#             db2['Employees'] = employees_dict
#             db2.close()
#
#             return redirect(url_for('employee_home'))


@app.route('/createEmployer', methods=['GET', 'POST'])
def create_employer():
    create_employer_form = CreateEmployerForm(request.form)
    if request.method == 'POST' and create_employer_form.validate():
        employers_dict = {}
        db = shelve.open('employers.db', 'c')

        try:
            employers_dict = db['Employers']
        except IOError:
            print('Error in retrieving employers.db')
        except:
            print("Error in retrieving Employers from employers.db.")
        else:
            current_id = 0
            for id in employers_dict:
                if id >= current_id and id < sys.maxsize:
                    current_id = id

                else:
                    current_id = 0

            Employer.Employer.count_id = current_id
            employer = Employer.Employer(
                create_employer_form.company_name.data,
                create_employer_form.company_location.data,
                create_employer_form.industry.data,
                create_employer_form.establishment_date.data,
                create_employer_form.company_logo.data,
                create_employer_form.email.data,
                create_employer_form.contact.data,
                create_employer_form.facebook.data,
                create_employer_form.instagram.data,
                create_employer_form.social_media.data,
                create_employer_form.website.data,
                create_employer_form.remarks.data)

            employers_dict[employer.get_employer_id()] = employer
            db['Employers'] = employers_dict
            db.close()

            return redirect(url_for('employer_profiles'))
    return render_template('createEmployer.html', form=create_employer_form)


@app.route('/retrieveEmployers')
def retrieve_employers():
    try:
        employers_dict = {}
        db = shelve.open('employers.db', 'r')
        employers_dict = db['Employers']
        db.close()

    except IOError:
        print('Error in retrieving employers.db')
    except:
        print("Error in retrieving Employers from employers.db.")
    else:
        employers_list = []

        for key in employers_dict:
            employer = employers_dict.get(key)
            employers_list.append(employer)

        return render_template('retrieveEmployers.html', count=len(employers_list), employers_list=employers_list)
    # try:
    #     listings_dict = {}
    #     db3 = shelve.open('listings.db', 'r')
    #     listings_dict = db3['Listings']
    #     db3.close()
    # except IOError:
    #     print('Error in retrieving listings.db')
    # except:
    #     print("Error in retrieving Listings from listings.db.")
    # else:
    #     listings_list = []
    #     for key in listings_dict:
    #         listings = listings_dict.get(key)
    #         listings_list.append(listings)
    #
    #     return render_template('retrieveListings.html', count=len(listings_list), listings_list=listings_list)


@app.route('/employerProfile')
def employer_profiles():
    try:
        employers_dict = {}
        db = shelve.open('employers.db', 'r')
        employers_dict = db['Employers']
        db.close()

    except IOError:
        print('Error in retrieving employers.db')
    except:
        print("Error in retrieving Employers from employers.db.")
    else:
        employers_list = []
        for key in employers_dict:
            employer = employers_dict.get(key)
            if employer.get_company_name() == 'Jumbo Group':
                employers_list.append(employer)
        return render_template('employerProfile.html', count=len(employers_list), employers_list=employers_list)


@app.route('/updateEmployer/<int:id>/', methods=['GET', 'POST'])
def update_employer(id):
    update_employer_form = CreateEmployerForm(request.form)
    if request.method == 'POST' and update_employer_form.validate():
        employers_dict = {}
        db = shelve.open('employers.db', 'w')
        try:
            employers_dict = db['Employers']
        except IOError:
            print('Error in retrieving employers.db')
        except:
            print("Error in retrieving Employers from employers.db.")
        else:
            employer = employers_dict.get(id)
            employer.set_company_name(update_employer_form.company_name.data)
            employer.set_company_location(update_employer_form.company_location.data)
            employer.set_establishment_date(update_employer_form.establishment_date.data)
            employer.set_industry(update_employer_form.industry.data)
            employer.set_company_logo(update_employer_form.company_logo.data)
            employer.set_email(update_employer_form.email.data)
            employer.set_contact(update_employer_form.contact.data)
            employer.set_facebook(update_employer_form.facebook.data)
            employer.set_instagram(update_employer_form.instagram.data)
            employer.set_social_media(update_employer_form.social_media.data)
            employer.set_website(update_employer_form.website.data)
            employer.set_remarks(update_employer_form.remarks.data)

            db['Employers'] = employers_dict
            db.close()

        return redirect(url_for('retrieve_employers'))
    else:
        try:
            employers_dict = {}
            db = shelve.open('employers.db', 'r')
            employers_dict = db['Employers']
            db.close()
        except IOError:
            print('Error in retrieving employers.db')
        except:
            print("Error in retrieving Employers from employers.db.")
        else:
            employer = employers_dict.get(id)

            update_employer_form.company_name.data = employer.get_company_name()
            update_employer_form.company_location.data = employer.get_company_location()
            update_employer_form.industry.data = employer.get_industry()
            update_employer_form.establishment_date.data = employer.get_establishment_date()
            update_employer_form.company_logo.data = employer.get_company_logo()
            update_employer_form.email.data = employer.get_email()
            update_employer_form.contact.data = employer.get_contact()
            update_employer_form.facebook.data = employer.get_facebook()
            update_employer_form.instagram.data = employer.get_instagram()
            update_employer_form.social_media.data = employer.get_social_media()
            update_employer_form.website.data = employer.get_website()
            update_employer_form.remarks.data = employer.get_remarks()

            return render_template('updateEmployer.html', form=update_employer_form)


@app.route('/deleteEmployer/<int:id>', methods=['POST'])
def delete_employer(id):
    employers_dict = {}
    db = shelve.open('employers.db', 'w')
    try:
        employers_dict = db['Employers']
    except IOError:
        print('Error in retrieving employers.db')
    except:
        print("Error in retrieving Employers from employers.db.")
    else:
        employers_dict.pop(id)

        db['Employers'] = employers_dict
        db.close()

        return redirect(url_for('retrieve_employers'))


@app.route('/createListing/<int:id>', methods=['GET', 'POST'])
def create_listing(id):
    create_listing_form = CreateListingForm(request.form)
    if request.method == 'POST' and create_listing_form.validate():
        employers_dict = {}
        db = shelve.open('employers.db', 'w')

        listings_dict = {}
        db3 = shelve.open('listings.db', 'c')

        try:
            listings_dict = db3['Listings']
            employers_dict = db['Employers']
        except IOError:
            print('Error in retrieving listings.db')
        except:
            print("Error in retrieving Listings from listings.db.")
        else:
            current_id = 0
            for id in listings_dict:
                if id >= current_id and id < sys.maxsize:
                    current_id = id

                else:
                    current_id = 0
            employer = employers_dict.get(id)

            Listings.Listings.count_id = current_id
            listing = Listings.Listings(create_listing_form.job_title.data,
                                        create_listing_form.no_of_hires.data,
                                        create_listing_form.job_description.data,
                                        create_listing_form.job_requirements.data,
                                        create_listing_form.position_required.data)

            listing.set_company(employer.get_company_name())
            listings_dict[listing.get_listing_no()] = listing
            db3['Listings'] = listings_dict
            db3.close()

            employer.set_no_of_listings(len(listings_dict))
            db['Employers'] = employers_dict
            db.close()

            return redirect(url_for('company_home'))
    return render_template('createListing.html', form=create_listing_form)


@app.route('/retrieveListings')
def retrieve_listings():
    try:
        listings_dict = {}
        db3 = shelve.open('listings.db', 'r')
        listings_dict = db3['Listings']
        db3.close()
    except IOError:
        print('Error in retrieving listings.db')
    except:
        print("Error in retrieving Listings from listings.db.")
    else:
        listings_list = []
        for key in listings_dict:
            listings = listings_dict.get(key)
            listings_list.append(listings)
            session['company'] = listings.get_company()
        return render_template('retrieveListings.html', count=len(listings_list), listings_list=listings_list,
                               company=session['company'])


@app.route('/updateListing/<int:id>/', methods=['GET', 'POST'])
def update_listing(id):
    update_listing_form = CreateListingForm(request.form)
    if request.method == 'POST' and update_listing_form.validate():
        listings_dict = {}
        db3 = shelve.open('listings.db', 'w')
        try:
            listings_dict = db3['Listings']
        except IOError:
            print('Error in retrieving listings.db')
        except:
            print("Error in retrieving Listings from listings.db.")
        else:
            listing = listings_dict.get(id)
            listing.set_job_title(update_listing_form.job_title.data)
            listing.set_no_of_hires(update_listing_form.no_of_hires.data)
            listing.set_job_description(update_listing_form.job_description.data)
            listing.set_job_requirements(update_listing_form.job_requirements.data)
            listing.set_position_required(update_listing_form.position_required.data)

            db3['Listings'] = listings_dict
            db3.close()

            return redirect(url_for('company_home'))
    else:
        try:
            listings_dict = {}
            db3 = shelve.open('listings.db', 'r')
            listings_dict = db3['Listings']
            db3.close()
        except IOError:
            print('Error in retrieving listings.db')
        except:
            print("Error in retrieving Listing from listings.db.")
        else:
            listing = listings_dict.get(id)
            update_listing_form.job_title.data = listing.get_job_title()
            update_listing_form.no_of_hires.data = listing.get_no_of_hires()
            update_listing_form.job_description.data = listing.get_job_description()
            update_listing_form.job_requirements.data = listing.get_job_requirements()
            update_listing_form.position_required.data = listing.get_position_required()

            return render_template('updateListing.html', form=update_listing_form)


@app.route('/deleteListing/<int:id>', methods=['POST'])
def delete_listing(id):
    listings_dict = {}
    db3 = shelve.open('listings.db', 'w')

    employers_dict = {}
    db = shelve.open('employers.db', 'w')

    try:
        listings_dict = db3['Listings']
        employers_dict = db['Employers']
    except IOError:
        print('Error in retrieving listings.db')
    except:
        print("Error in retrieving Listings from listings.db.")
    else:
        listings_dict.pop(id)
        listing = listings_dict.get(id)
        # for key in employers_dict:
        #     employer = employers_dict.get(key)
        #     if employer.get_company_name() == listing.get_company():
        #         employer.set_no_of_listings(employer.get_no_of_listings() - 1)

        db3['Listings'] = listings_dict
        db3.close()

        db['Employers'] = employers_dict
        db.close()

        return redirect(url_for('company_home'))


@app.route('/matchListings')
def match_listings():
    try:
        listings_dict = {}
        db3 = shelve.open('listings.db', 'r')
        listings_dict = db3['Listings']
        db3.close()
    except IOError:
        print('Error in retrieving listings.db')
    except:
        print("Error in retrieving Listings from listings.db.")
    else:
        listings_list = []
        for key in listings_dict:
            listings = listings_dict.get(key)
            listings_list.append(listings)
            session['company'] = listings.get_company()
        return render_template('matchListings.html', count=len(listings_list), listings_list=listings_list,
                               company=session['company'])


@app.route('/selectListings/<int:id>', methods=['POST'])
def select_listings(id):
    listings_dict = {}
    db2 = shelve.open('listings.db', 'w')
    try:
        listings_dict = db2['Listings']
    except IOError:
        print('Error in retrieving listings.db')
    except:
        print("Error in retrieving Listings from listings.db.")
    else:

        listing = listings_dict.get(id)
        listing.set_match('Matched')
        print(listing.get_match())
        listing.set_no_of_matches(listing.get_no_of_matches() + 1)
        print(listing.get_no_of_matches())

        db2['Listings'] = listings_dict
        db2.close()
        return redirect(url_for('match_listings'))


@app.route('/matchedListings')
def matched_listings():
    listings_dict = {}
    db2 = shelve.open('listings.db', 'r')
    listings_dict = db2['Listings']
    db2.close()

    matched_listings_list = []
    for key in listings_dict:
        listing = listings_dict.get(key)
        session['company'] = listing.get_company()
        if listing.get_match() == 'Matched':
            matched_listings_list.append(listing)

    print(len(matched_listings_list))

    return render_template('matchedListings.html', count=len(matched_listings_list),
                           matched_listings_list=matched_listings_list, company=session['company'])


@app.route('/createAirplane', methods=['GET', 'POST'])
def create_airplane():
    create_airplane_form = CreateAirplanesForm(request.form)
    if request.method == 'POST' and create_airplane_form.validate():
        airplanes_dict = {}
        db = shelve.open('airplane.db', 'c')

        try:
            airplanes_dict = db['Airplanes']

        except IOError:
            print('Error in retrieving airplane.db')

        except ValueError:
            print('Value Error')

        except:
            print("Error in retrieving airplanes from airplane.db.")

        else:
            current_id = 0
            for id in airplanes_dict:
                if current_id <= id < sys.maxsize:
                    current_id = id

                else:
                    current_id = 0

            today = date.today()
            maintenance_date = create_airplane_form.last_maintenance.data
            date_diff = today - maintenance_date
            print(today, maintenance_date, date_diff.days)
            Airplane.Airplane.count_id = current_id
            airplane = Airplane.Airplane(create_airplane_form.tail_number.data, create_airplane_form.operation_status.data,
                                         create_airplane_form.model.data, create_airplane_form.airline.data,
                                         create_airplane_form.hanger.data, create_airplane_form.remarks.data,
                                         create_airplane_form.last_maintenance.data, create_airplane_form.in_charge.data, date_diff.days)
            airplanes_dict[airplane.get_airplane_id()] = airplane
            db['Airplanes'] = airplanes_dict

            db.close()

            return redirect(url_for('retrieve_airplanes'))
    return render_template('createAirplane.html', form=create_airplane_form)


@app.route('/retrieveAirplanes')
def retrieve_airplanes():
    airplanes_dict = {}
    db = shelve.open('airplane.db', 'r')
    list = []
    airplanes_dict = db['Airplanes']

    for x in db['Airplanes']:
        print(x)
        airplane = airplanes_dict.get(x)
        last_maintenance = airplane.get_last_maintenance()
        today = date.today()
        date_diff = today - last_maintenance
        date_diff_days = date_diff.days
        airplane.set_date_diff(date_diff_days)
        print(airplane.get_date_diff())
        print(today, 'last maintenance:', last_maintenance, 'date difference:', date_diff.days)
        if date_diff.days >= 90:
            flash('You have to do maintenance on plane')
        else:
            pass
        x += 1
        db.close()

    airplanes_list = []
    for key in airplanes_dict:
        airplane = airplanes_dict.get(key)
        airplanes_list.append(airplane)

    return render_template('retrieveAirplanes.html', count=len(airplanes_list), airplanes_list=airplanes_list)


@app.route('/updateAirplane/<int:id>/', methods=['GET', 'POST'])
def update_airplane(id):
    update_airplane_form = CreateAirplanesForm(request.form)
    if request.method == 'POST' and update_airplane_form.validate():
        airplanes_dict = {}
        db = shelve.open('airplane.db', 'w')

        try:
            airplanes_dict = db['Airplanes']

        except IOError:
            print('Error in retrieving airplane.db')

        except ValueError:
            print('Value Error')

        except:
            print("Error in retrieving airplanes from airplane.db.")

        else:
            airplane = airplanes_dict.get(id)
            airplane.set_tail_number(update_airplane_form.tail_number.data)
            airplane.set_operation_status(update_airplane_form.operation_status.data)
            airplane.set_model(update_airplane_form.model.data)
            airplane.set_airline(update_airplane_form.airline.data)
            airplane.set_hanger(update_airplane_form.hanger.data)
            airplane.set_remarks(update_airplane_form.remarks.data)
            airplane.set_last_maintenance(airplane.get_last_maintenance())
            airplane.set_in_charge(airplane.get_in_charge())

            db['Airplanes'] = airplanes_dict
            db.close()

            return redirect(url_for('retrieve_airplanes'))
    else:
        airplanes_dict = {}
        db = shelve.open('airplane.db', 'r')
        airplanes_dict = db['Airplanes']
        db.close()

        airplane = airplanes_dict.get(id)
        update_airplane_form.tail_number.data = airplane.get_tail_number()
        update_airplane_form.operation_status.data = airplane.get_operation_status()
        update_airplane_form.model.data = airplane.get_model()
        update_airplane_form.airline.data = airplane.get_airline()
        update_airplane_form.hanger.data = airplane.get_hanger()
        update_airplane_form.remarks.data = airplane.get_remarks()
        update_airplane_form.last_maintenance.data = airplane.get_last_maintenance()
        update_airplane_form.in_charge.data = airplane.get_in_charge()

        return render_template('updateAirplane.html', form=update_airplane_form)


@app.route('/updateMaintenance/<int:id>/', methods=['GET', 'POST'])
def update_maintenance(id):
    update_maintenance_form = CreateMaintenanceForm(request.form)
    if request.method == 'POST' and update_maintenance_form.validate():
        airplanes_dict = {}
        db = shelve.open('airplane.db', 'w')

        try:
            airplanes_dict = db['Airplanes']

        except IOError:
            print('Error in retrieving airplane.db')

        except ValueError:
            print('Value Error')

        except:
            print("Error in retrieving airplanes from airplane.db.")

        else:
            airplane = airplanes_dict.get(id)
            airplane.set_last_maintenance(update_maintenance_form.last_maintenance.data)
            airplane.set_in_charge(update_maintenance_form.in_charge.data)

            today = date.today()
            maintenance_date = airplane.get_last_maintenance()
            date_diff = today - maintenance_date
            print(today, maintenance_date, date_diff.days)

            if date_diff.days == 90 or date_diff.days > 90:
                flash('You have to do maintenance on plane')

            db['Airplanes'] = airplanes_dict
            db.close()

            return redirect(url_for('retrieve_airplanes'))
    else:
        try:
            airplanes_dict = {}
            db = shelve.open('airplane.db', 'r')
            airplanes_dict = db['Airplanes']
            db.close()

        except IOError:
            print('Error in retrieving airplane.db')

        except ValueError:
            print('Value Error')

        except:
            print("Error in retrieving airplanes from airplane.db.")

        else:
            airplane = airplanes_dict.get(id)
            update_maintenance_form.last_maintenance.data = airplane.get_last_maintenance()
            update_maintenance_form.in_charge.data = airplane.get_in_charge()

            return render_template('updateMaintenance.html', form=update_maintenance_form)


@app.route('/deleteAirplane/<int:id>', methods=['POST'])
def delete_airplane(id):
    airplanes_dict = {}
    db = shelve.open('airplane.db', 'w')
    try:
        airplanes_dict = db['Airplanes']

    except IOError:
        print('Error in retrieving airplane.db')

    except ValueError:
        print('Value Error')

    else:
        airplanes_dict.pop(id)

        db['Airplanes'] = airplanes_dict
        db.close()

        return redirect(url_for('retrieve_airplanes'))


@app.route('/createPassenger', methods=['GET', 'POST'])
def create_passenger():
    create_passenger_form = CreatePassengerForm(request.form)
    if request.method == 'POST' and create_passenger_form.validate():
        passengers_dict = {}
        db = shelve.open('passenger.db', 'c')

        try:
            passengers_dict = db['Passengers']
        except:
            print("Error in retrieving Passengers from passenger.db.")

        passenger = Customer.Passenger(create_passenger_form.first_name.data, create_passenger_form.last_name.data,
                                       create_passenger_form.nric.data, create_passenger_form.phone_no.data,
                                       create_passenger_form.email.data, create_passenger_form.flight_no.data,
                                       create_passenger_form.seat_no.data, create_passenger_form.gender.data,
                                       create_passenger_form.health_declaration.data,
                                       create_passenger_form.pcr_test.data, create_passenger_form.pre_book.data,
                                       create_passenger_form.remarks.data)
        passengers_dict[passenger.get_passenger_id()] = passenger
        db['Passengers'] = passengers_dict

        db.close()

        session['username'] = 'Anthony'

        return redirect(url_for('user_home'))
    return render_template('createCustomer.html', form=create_passenger_form)


@app.route('/retrievePassengers')
def retrieve_passengers():
    try:
        passengers_dict = {}
        db = shelve.open('passenger.db', 'r')
        passengers_dict = db['Passengers']
        db.close()

    except IOError:
        print('Error in retrieving passenger.db')

    except ValueError:
        print('Value Error')

    except:
        print("Error in retrieving Passengers from passenger.db.")

    else:
        passengers_list = []
        for key in passengers_dict:
            passenger = passengers_dict.get(key)
            passengers_list.append(passenger)
            if passenger.get_nric() == 'S9733462E':  # (session id)
                passengers_list.append(passenger)

        return render_template('retrieveCustomer.html', count=len(passengers_list), passengers_list=passengers_list)


@app.route('/updatePassenger/<int:id>/', methods=['GET', 'POST'])
def update_customer(id):
    update_customer_form = CreatePassengerForm(request.form)
    if request.method == 'POST' and update_customer_form.validate():
        passengers_dict = {}
        db = shelve.open('passenger.db', 'w')
        passengers_dict = db['Passengers']

        passenger = passengers_dict.get(id)
        passenger.set_first_name(update_customer_form.first_name.data)
        passenger.set_last_name(update_customer_form.last_name.data)
        passenger.set_nric(update_customer_form.nric.data)
        passenger.set_phone_no(update_customer_form.phone_no.data)
        passenger.set_flight_no(update_customer_form.flight_no.data)
        passenger.set_seat_no(update_customer_form.seat_no.data)
        passenger.set_email(update_customer_form.email.data)
        passenger.set_gender(update_customer_form.gender.data)
        passenger.set_health_declaration(update_customer_form.health_declaration.data)
        passenger.set_pcr_test(update_customer_form.pcr_test.data)
        passenger.set_pre_book(update_customer_form.pre_book.data)
        passenger.set_remarks(update_customer_form.remarks.data)

        db['Passengers'] = passengers_dict
        db.close()
        return redirect(url_for('user_home'))
    else:
        passengers_dict = {}
        db = shelve.open('passenger.db', 'r')
        passengers_dict = db['Passengers']
        db.close()

        passenger = passengers_dict.get(id)
        update_customer_form.first_name.data = passenger.get_first_name()
        update_customer_form.last_name.data = passenger.get_last_name()
        update_customer_form.nric.data = passenger.get_nric()
        update_customer_form.phone_no.data = passenger.get_phone_no()
        update_customer_form.email.data = passenger.get_email()
        update_customer_form.flight_no.data = passenger.get_flight_no()
        update_customer_form.seat_no.data = passenger.get_seat_no()
        update_customer_form.gender.data = passenger.get_gender()
        update_customer_form.health_declaration.data = passenger.get_health_declaration()
        update_customer_form.pcr_test.data = passenger.get_pcr_test()
        update_customer_form.pre_book.data = passenger.get_pre_book()
        update_customer_form.remarks.data = passenger.get_remarks()

        return render_template('updateCustomer.html', form=update_customer_form)


@app.route('/deletePassenger/<int:id>', methods=['POST'])
def delete_passenger(id):
    passengers_dict = {}
    db = shelve.open('passenger.db', 'w')
    passengers_dict = db['Passengers']

    passengers_dict.pop(id)

    db['Passengers'] = passengers_dict
    db.close()

    return redirect(url_for('retrieve_management'))


@app.route('/incompletedFilter', methods=['GET', 'POST'])
def incompleted_filter():
    passengers_dict = {}
    db = shelve.open('passenger.db', 'r')
    passengers_dict = db['Passengers']
    db.close()

    passengers_list = []
    for key in passengers_dict:
        passenger = passengers_dict.get(key)
        if passenger.get_health_declaration() == 'N' or passenger.get_pcr_test() == 'N' or passenger.get_pre_book() == 'N':
            passengers_list.append(passenger)

    return render_template('incompletedFilter.html', count=len(passengers_list), passengers_list=passengers_list)


@app.route('/completedFilter', methods=['GET', 'POST'])
def completed_filter():
    passengers_dict = {}
    db = shelve.open('passenger.db', 'r')
    passengers_dict = db['Passengers']
    db.close()

    passengers_list = []
    for key in passengers_dict:
        passenger = passengers_dict.get(key)
        if passenger.get_health_declaration() == 'Y' and passenger.get_pcr_test() == 'Y' and passenger.get_pre_book() == 'Y':
            passengers_list.append(passenger)

    return render_template('completedFilter.html', count=len(passengers_list), passengers_list=passengers_list)


@app.route('/createFlight', methods=['GET', 'POST'])
def create_flight():
    create_flight_form = CreateFlightForm(request.form)
    if request.method == 'POST' and create_flight_form.validate():
        flights_dict = {}
        flightdb = shelve.open('flight.db', 'c')

        try:
            flights_dict = flightdb['Flights']
        except ValueError:
            print("Please enter a valid number.")
        except:
            print("Error in retrieving Flights from flight.db.")

        current_id = 0
        for id in flights_dict:
            if current_id <= id < sys.maxsize:
                current_id = id
            else:
                current_id = 0

        Flight.Flight.count_id = current_id
        flight = Flight.Flight(create_flight_form.flight_number.data, create_flight_form.departure_country.data,
                               create_flight_form.arrival_country.data, create_flight_form.departure_date.data,
                               create_flight_form.fly.data, create_flight_form.flight_type.data)
        flights_dict[flight.get_flight_id()] = flight
        flightdb['Flights'] = flights_dict

        flightdb.close()

        return redirect(url_for('retrieve_flights'))
    return render_template('createFlight.html', form=create_flight_form)


@app.route('/retrieveFlights')
def retrieve_flights():
    try:
        flights_dict = {}
        flightdb = shelve.open('flight.db', 'r')
        flights_dict = flightdb['Flights']
        flightdb.close()

        tickets_dict = {}
        ticketdb = shelve.open('ticket.db', 'r')
        tickets_dict = ticketdb['Tickets']
        ticketdb.close()
    except:
        print("Error in retrieving Flights from flight.db")
    else:
        flights_list = []
        for key in flights_dict:
            flight = flights_dict.get(key)
            if flight.get_flight_number() == 'SQ882':
                flights_list.append(flight)
                session['flight_number'] = flight.get_flight_number()
                session['flight_id'] = flight.get_flight_id()
            elif flight.get_flight_number() == 'SQ964':
                flights_list.append(flight)
                session['flight_number'] = flight.get_flight_number()
                session['flight_id'] = flight.get_flight_id()
            elif flight.get_flight_number() == 'SQ285':
                flights_list.append(flight)
                session['flight_number'] = flight.get_flight_number()
                session['flight_id'] = flight.get_flight_id()

        hongkong_tickets_list = []
        hongkong_flying_list = []
        hongkong_rebooked_list = []
        hongkong_postpones_list = []
        taiwan_tickets_list = []
        taiwan_flying_list = []
        taiwan_rebooked_list = []
        taiwan_postpones_list = []
        malaysia_tickets_list = []
        malaysia_flying_list = []
        malaysia_rebooked_list = []
        malaysia_postpones_list = []
        for key in tickets_dict:
            ticket = tickets_dict.get(key)
            if ticket.get_arrival_country() == 'Hong Kong':
                hongkong_tickets_list.append(ticket)
                if ticket.get_type() == 'rebook':
                    hongkong_rebooked_list.append(ticket)
                elif ticket.get_type() == 'postpone':
                    hongkong_postpones_list.append(ticket)
                elif ticket.get_type() == 'fly':
                    hongkong_flying_list.append(ticket)
            elif ticket.get_arrival_country() == 'Taipei':
                taiwan_tickets_list.append(ticket)
                if ticket.get_type() == 'rebook':
                    taiwan_rebooked_list.append(ticket)
                elif ticket.get_type() == 'postpone':
                    taiwan_postpones_list.append(ticket)
                elif ticket.get_type() == 'fly':
                    taiwan_flying_list.append(ticket)
            elif ticket.get_arrival_country() == 'Jakarta':
                malaysia_tickets_list.append(ticket)
                if ticket.get_type() == 'rebook':
                    malaysia_rebooked_list.append(ticket)
                elif ticket.get_type() == 'postpone':
                    malaysia_postpones_list.append(ticket)
                elif ticket.get_type() == 'fly':
                    malaysia_flying_list.append(ticket)

        return render_template('retrieveFlights.html', flights_list=flights_list,
                               flight_number=session['flight_number'], flight_id=session['flight_id'],
                               hongkong_count=len(hongkong_tickets_list), taiwan_count=len(taiwan_tickets_list),
                               malaysia_count=len(malaysia_tickets_list),
                               hongkong_calculations=len(hongkong_tickets_list) * 435,
                               taiwan_calculations=len(taiwan_tickets_list) * 592,
                               malaysia_calculations=len(malaysia_tickets_list) * 251,
                               hongkong_tickets_list=hongkong_tickets_list, hongkong_flying_list=hongkong_flying_list,
                               hongkong_rebooked_list=hongkong_rebooked_list,
                               hongkong_postpones_list=hongkong_postpones_list, taiwan_tickets_list=taiwan_tickets_list,
                               taiwan_flying_list=taiwan_flying_list, taiwan_rebooked_list=taiwan_rebooked_list,
                               taiwan_postpones_list=taiwan_postpones_list, malaysia_flying_list=malaysia_flying_list,
                               malaysia_rebooked_list=malaysia_rebooked_list,
                               malaysia_postpones_list=malaysia_postpones_list)


@app.route('/updateFlight/<int:id>/', methods=['GET', 'POST'])
def update_flight(id):
    update_flight_form = CreateFlightForm(request.form)
    if request.method == 'POST' and update_flight_form.validate():
        flights_dict = {}
        flightdb = shelve.open('flight.db', 'w')
        try:
            flights_dict = flightdb['Flights']
        except ValueError:
            print("Please enter a valid number.")
        except:
            print("Error in retrieving Flights from flight.db.")

        flight = flights_dict.get(id)
        flight.set_flight_number(update_flight_form.flight_number.data)
        flight.set_departure_country(update_flight_form.departure_country.data)
        flight.set_arrival_country(update_flight_form.arrival_country.data)
        flight.set_departure_date(update_flight_form.departure_date.data)
        flight.set_fly(update_flight_form.fly.data)
        flight.set_flight_type(update_flight_form.flight_type.data)

        flightdb['Flights'] = flights_dict
        flightdb.close()

        return redirect(url_for('retrieve_flights'))
    else:
        flights_dict = {}
        flightsdb = shelve.open('flight.db', 'r')

        try:
            flights_dict = flightsdb['Flights']
        except ValueError:
            print("Please enter a valid number.")
        except:
            print("Error in retrieving Flights from flight.db.")

        flightsdb.close()

        flight = flights_dict.get(id)
        update_flight_form.flight_number.data = flight.get_flight_number()
        update_flight_form.departure_country.data = flight.get_departure_country()
        update_flight_form.arrival_country.data = flight.get_arrival_country()
        update_flight_form.departure_date.data = flight.get_departure_date()
        update_flight_form.fly.data = flight.get_fly()
        update_flight_form.flight_type.data = flight.get_flight_type()

        return render_template('updateFlight.html', form=update_flight_form)


# @app.route('/Ticket')
# def ticket():
#     flights_dict = {}
#     flightdb = shelve.open('flight.db', 'r')
#
#     try:
#         flights_dict = flightdb['Flights']
#     except ValueError:
#         print("Please enter a valid number.")
#     except:
#         print("Error in retrieving Flights from flight.db.")
#
#     flightdb.close()
#
#     flights_list = []
#     for key in flights_dict:
#         flight = flights_dict.get(key)
#         flights_list.append(flight)
#
#     return render_template('Ticket.html', count=len(flights_list), flights_list=flights_list)


# @app.route('/Bookings')
# def bookings():
#     tickets_dict = {}
#     ticketdb = shelve.open('ticket.db', 'r')
#
#     try:
#         tickets_dict = ticketdb['Tickets']
#     except ValueError:
#         print("Please enter a valid number.")
#     except:
#         print("Error in retrieving Tickets from ticket.db.")
#
#     ticketdb.close()
#
#     tickets_list = []
#     for key in tickets_dict:
#         ticket = tickets_dict.get(key)
#         tickets_list.append(ticket)
#
#     return render_template('Bookings.html', count=len(tickets_list), tickets_list=tickets_list)


@app.route('/bookFlight', methods=['GET', 'POST'])
def book_flight():
    book_flight_form = BookTicketForm(request.form)
    if request.method == 'POST' and book_flight_form.validate():
        tickets_dict = {}
        ticketdb = shelve.open('ticket.db', 'c')

        try:
            tickets_dict = ticketdb['Tickets']
        except:
            print("Error in retrieving Ticket from ticket.db.")

        current_id = 0
        for id in tickets_dict:
            if id >= current_id and id < sys.maxsize:
                current_id = id
            else:
                current_id = 0

        Ticket.Ticket.count_id = current_id
        ticket = Ticket.Ticket(book_flight_form.departure_country.data, book_flight_form.arrival_country.data,
                               book_flight_form.return_date.data, book_flight_form.flight_class.data,
                               book_flight_form.adults.data, book_flight_form.children.data)
        ticket.set_type("fly")
        tickets_dict[ticket.get_ticket_id()] = ticket
        ticketdb['Tickets'] = tickets_dict

        ticketdb.close()

        return redirect(url_for('create_passenger'))
    return render_template('bookFlight.html', form=book_flight_form)


@app.route('/postponeTicket/<int:id>/', methods=['GET', 'POST'])
def postpone_ticket(id):
    postpone_ticket_form = BookTicketForm(request.form)
    if request.method == 'POST' and postpone_ticket_form.validate():
        tickets_dict = {}
        ticketdb = shelve.open('ticket.db', 'w')
        try:
            tickets_dict = ticketdb['Tickets']
        except ValueError:
            print("Please enter a valid number.")
        except:
            print("Error in retrieving Tickets from ticket.db.")

        ticket = tickets_dict.get(id)
        ticket.set_departure_country(postpone_ticket_form.departure_country.data)
        ticket.set_arrival_country(postpone_ticket_form.arrival_country.data)
        ticket.set_return_date(postpone_ticket_form.return_date.data)
        ticket.set_flight_class(postpone_ticket_form.flight_class.data)
        ticket.set_adults(postpone_ticket_form.adults.data)
        ticket.set_children(postpone_ticket_form.children.data)
        ticket.set_type("postpone")

        ticketdb['Tickets'] = tickets_dict
        ticketdb.close()

        return redirect(url_for('user_home'))
    else:
        tickets_dict = {}
        ticketdb = shelve.open('ticket.db', 'r')

        try:
            tickets_dict = ticketdb['Tickets']
        except ValueError:
            print("Please enter a valid number.")
        except:
            print("Error in retrieving Flights from flight.db.")

        ticketdb.close()

        ticket = tickets_dict.get(id)
        postpone_ticket_form.departure_country.data = ticket.get_departure_country()
        postpone_ticket_form.arrival_country.data = ticket.get_arrival_country()
        postpone_ticket_form.return_date.data = ticket.get_return_date()
        postpone_ticket_form.flight_class.data = ticket.get_flight_class()
        postpone_ticket_form.adults.data = ticket.get_adults()
        postpone_ticket_form.children.data = ticket.get_children()

        return render_template('postponeTicket.html', form=postpone_ticket_form)


@app.route('/rebookTicket/<int:id>/', methods=['GET', 'POST'])
def rebook_ticket(id):
    rebook_ticket_form = BookTicketForm(request.form)
    if request.method == 'POST' and rebook_ticket_form.validate():
        tickets_dict = {}
        ticketdb = shelve.open('ticket.db', 'w')
        try:
            tickets_dict = ticketdb['Tickets']
        except ValueError:
            print("Please enter a valid number.")
        except:
            print("Error in retrieving Tickets from ticket.db.")

        ticket = tickets_dict.get(id)
        ticket.set_departure_country(rebook_ticket_form.departure_country.data)
        ticket.set_arrival_country(rebook_ticket_form.arrival_country.data)
        ticket.set_return_date(rebook_ticket_form.return_date.data)
        ticket.set_flight_class(rebook_ticket_form.flight_class.data)
        ticket.set_adults(rebook_ticket_form.adults.data)
        ticket.set_children(rebook_ticket_form.children.data)
        ticket.set_type("rebook")

        ticketdb['Tickets'] = tickets_dict
        ticketdb.close()

        return redirect(url_for('user_home'))
    else:
        tickets_dict = {}
        ticketdb = shelve.open('ticket.db', 'r')

        try:
            tickets_dict = ticketdb['Tickets']
        except ValueError:
            print("Please enter a valid number.")
        except:
            print("Error in retrieving Flights from flight.db.")

        ticketdb.close()

        ticket = tickets_dict.get(id)
        rebook_ticket_form.departure_country.data = ticket.get_departure_country()
        rebook_ticket_form.arrival_country.data = ticket.get_arrival_country()
        rebook_ticket_form.return_date.data = ticket.get_return_date()
        rebook_ticket_form.flight_class.data = ticket.get_flight_class()
        rebook_ticket_form.adults.data = ticket.get_adults()
        rebook_ticket_form.children.data = ticket.get_children()

        return render_template('rebookTicket.html', form=rebook_ticket_form)


@app.route('/refundTicket/<int:id>/', methods=['POST'])
def refund_ticket(id):
    ticket_dict = {}
    ticketdb = shelve.open('ticket.db', 'w')
    ticket_dict = ticketdb['Tickets']

    ticket_dict.pop(id)

    ticketdb['Tickets'] = ticket_dict
    ticketdb.close()

    return redirect(url_for('user_home'))


@app.route('/retrieveManagement')
def retrieve_management():
    try:
        passengers_dict = {}
        db = shelve.open('passenger.db', 'r')
        passengers_dict = db['Passengers']
        db.close()

    except IOError:
        print('Error in retrieving passenger.db')

    except ValueError:
        print('Value Error')

    except:
        print("Error in retrieving Passengers from passenger.db.")

    else:
        passengers_list = []
        for key in passengers_dict:
            passenger = passengers_dict.get(key)
            passengers_list.append(passenger)

        return render_template('retrieveManagement.html', count=len(passengers_list), passengers_list=passengers_list)


# @app.route('/uploadLogo', methods=['POST'])
# def upload_files():
#    uploaded_file = request.files['file']
#    filename = secure_filename(uploaded_file.filename)
#    if filename != '':
#        file_ext = os.path.splitext(filename)[1]
#            abort(400)
#        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
#    return redirect(url_for('retrieve_users'))


# @app.route('/uploads/<filename>')
# def upload(filename):
#    return send_from_directory(app.config['UPLOAD_PATH'], filename)


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     login_form = LoginForm(request.form)
#     if request.method == 'GET':
#         print(session)
#         session.pop('username', None)
#         print(session)
#     if request.method == 'POST' and login_form.validate():
#         print(session)
#         employees_dict = {'Anthony': 'password', 'Benny': 'password', 'Jumbo': 'password', 'Catherine': 'password'}
#
#         if request.form['login_id'] == 'Anthony' in employees_dict:
#             if employees_dict['Anthony'] == request.form['password']:
#                 session['username'] = request.form['login_id']
#                 return redirect(url_for('user_home'))
#             else:
#                 flash("Incorrect user or password!")
#         elif request.form['login_id'] == 'Benny' in employees_dict:
#             if employees_dict['Benny'] == request.form['password']:
#                 session['username'] = request.form['login_id']
#                 return redirect(url_for('admin_home'))
#             else:
#                 flash("Incorrect user or password!")
#         elif request.form['login_id'] == 'Jumbo' in employees_dict:
#             if employees_dict['Jumbo'] == request.form['password']:
#                 session['username'] = request.form['login_id']
#                 return redirect(url_for('company_home'))
#             else:
#                 flash("Incorrect user or password!")
#         elif request.form['login_id'] == 'Catherine' in employees_dict:
#             if employees_dict['Catherine'] == request.form['password']:
#                 session['username'] = request.form['login_id']
#                 return redirect(url_for('employee_home'))
#             else:
#                 flash("Incorrect user or password!")
#         else:
#             flash("Incorrect user or password!")
#     print(session)
#     print(g.user)
#     return render_template('login.html', form=login_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM customer WHERE username = %s', (username,))
        customer = cursor.fetchone()
        if customer:
            hashAndSalt = customer['password']
            if bcrypt.checkpw(password.encode(), hashAndSalt.encode()):
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = customer['id']
                session['username'] = customer['username']
            # return 'Logged in successfully!'
            return redirect(url_for('user_home'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html', form=login_form)

# @app.route('/logout')
# def logout():
#     if 'username' in session:
#         session.pop('username', None)
#         flash("You have logged out")
#         return render_template('logout.html')
#     else:
#         return '<p>user already logged out</p>' and render_template('index.html')
#     print(g.user)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     register_form = RegisterForm(request.form)
#     if request.method == 'POST' and register_form.validate():
#         if register_form.type.data == 'P':
#             return redirect(url_for('create_passenger'))
#         elif register_form.type.data == 'Er':
#             return redirect(url_for('create_employer'))
#         else:
#             return redirect(url_for('/'))
#     return render_template('register.html', form=register_form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    register_form = RegisterForm(request.form)
    if request.method == 'POST' and 'username' in register_form and 'password' in register_form and 'email' in register_form and 'confirm' in register_form and register_form.validate():
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        confirm = request.form['confirm']
        if password == confirm:
            salt = bcrypt.gensalt(rounds=16)
            hash_password = bcrypt.hashpw(password.encode(), salt)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO customer VALUES (NULL, %s, %s, NULL, NULL, NULL, NULL, NULL, NULL, NULL, %s, NULL, %s)',(username, hash_password, email, "Some Keys"))
            #cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s, %s)',(username, password, email, "Some Keys"))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
        return redirect(url_for('retrieve_passengers'))
    return render_template('register.html', form=register_form)

@app.route('/forgetPassword', methods=['GET', 'POST'])
def forgetpassword():
    forgetpassword_form = ForgetPassword(request.form)
    if request.method == 'POST' and forgetpassword_form.validate():
        employees_dict = {'Anthony': 'password', 'Benny': 'password', 'Jumbo': 'password', 'Catherine': 'password'}
        if forgetpassword_form.login_id.data in employees_dict:
            print('Valid')
            return redirect(url_for('home'))
        else:
            print('Invalid')
    return render_template('forgetPassword.html', form=forgetpassword_form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404


if __name__ == '__main__':
    app.run()
