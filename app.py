# Setup dependencies
import os
import psycopg2
import requests
from flask import Flask, render_template, request, redirect, url_for, json, jsonify, flash
import datetime
from pprint import pprint
import ssl
from crud import *
import hashlib
from passlib.hash import sha256_crypt
import functools
import operator
from collections import OrderedDict


# Import Postgres database details from config file
pg_ipaddress = os.getenv("pg_ipaddress")
pg_port = os.getenv("pg_port")
pg_username = os.getenv("pg_username")
pg_password = os.getenv("pg_password")
pg_dbname = os.getenv("pg_dbname")



# Setup connection with Postgres
try:
       conn = psycopg2.connect(dbname=pg_dbname, host=pg_ipaddress, user=pg_username, password=pg_password)
       print('------------------------------------')
       print('PostgreSQL database now connected')
       print('------------------------------------')
except (Exception, psycopg2.DatabaseError) as error:
       print('----------------------------------------------------')
       print ("Error while fetching data from PostgreSQL", error)
       print('----------------------------------------------------')

if conn:
    conn.autocommit = True
    cur = conn.cursor()
    cur.close()

# Create Flask app instance
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'



# Route for Index page -- Homepage/Intro to the App/Log-In page 
# @app.route("/", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        print('*****************')
        print('Getting form...')
        print('*****************')
        return render_template('logIndex.html') 
    error = None
    if request.method == 'POST':
        input_log_in = request.form['username']
        in_password = request.form['password']
        print(in_password)

        # grabbing log_in names from db to check against input
        cur = conn.cursor() 
        cur.execute('SELECT log_in FROM users;')
        login_fetch = cur.fetchall()
        print("this is the fetch")
        print(login_fetch)
        print("----------------------------------") 

        length = len(login_fetch)
        
        login_names_list = []
        for db_row in login_fetch:
            login_name_dict = {}
            login_name_dict['log_name'] = db_row[0]
            login_names_list.append(login_name_dict)
            
        print(login_names_list) 

        res = [] 
        for key, value in ( 
            itertools.chain.from_iterable( 
                [itertools.product((k, ), v) for k, v in test_dict.items()])): 
                    res.append(value) 
      
        # printing result  
        print("The list values of keys are : " + str(res))

        # cur = conn.cursor()
        # cur.execute('SELECT log_in FROM users;')
        # user_login_fetch = cur.fetchall()

        # #prints a tupple
        # print(user_login_fetch)
        # log_in = request.form['username']
        # for login in user_login_fetch:
        #     print(login)
        #     login = functools.reduce(operator.add,(login))
        #     print(login)
        #     if login == log_in: 
            
                # cur = conn.cursor() 
                # cur.execute('SELECT password FROM users ;')
                # cur.execute('SELECT password FROM users WHERE log_in=%s;', [input_log_in])
                # rows = cur.fetchall()
                # print("this is the rows(fetch)")
                # print(rows)
                # print("----------------------------------")
                # tup=rows[0]
                # print("this is the tup")
                # print(tup)
                # strpass = functools.reduce(operator.add,(tup))
                # print(strpass)
                # print(hashed_in_pass)
                # hashed_in_pass = sha256_crypt.verify(in_password, strpass)
                # if hashed_in_pass:
                #     return redirect(url_for('dashboard_data'))
                    # print("matched")
            #     else:
            #         error = 'Invalid p Credentials. Please try again.'
            #         print(error)
            #         return render_template('logIndex.html', error=error)
            # else:
            #     error = 'Invalid login. Please try again.'
            #     print(error)
            #     return render_template('logIndex.html', error=error)
    return render_template('logIndex.html')

# def index():
#     error = None
#     if request.method == 'POST':
#         log_in = request.form['username']
#         in_password = request.form['password']
#         # hashed_in_pass = sha256_crypt.hash("in_password")
#         hashed_in_pass = sha256_crypt.hash(request.form['password'])

#         cur = conn.cursor() 
#         cur.execute('SELECT password FROM users WHERE log_in=%s;', [log_in])

#         rows = cur.fetchall()
#         tup=rows[0] 
#         strpass = functools.reduce(operator.add,(tup))
#         print(strpass)
#         print(hashed_in_pass)
#         hashed_strpass = sha256_crypt.hash("strpass")
#         print(type(hashed_strpass))
#         print(type(hashed_in_pass))


#         if hashed_in_pass != in_password or hashed_strpass:
#             error = 'Invalid Credentials. Please try again.'
#             print(error)
#         else:
#             return redirect(url_for('new_project_data'))
#             print("matched")
#     return render_template('logINdex.html', error=error)



    # return render_template("logINdex.html")



# Route for Project Dashboard -- fetches project data from database for display, writes an input field to database
@app.route("/dashboard", methods=['GET'])
def dashboard_data():
    if request.method == 'GET':
        cur = conn.cursor()
        # Fetch data from Project_Details table
        cur.execute('SELECt * FROM project_details' + ';')
        project_details_data = cur.fetchall()

        # Create a dictionary of dictionaries with Project_Details table data
        project_list = {}
        for proj in project_details_data:
            project_dict = {}
            project_id = str(proj[0])
            project_dict['project_name'] = str(proj[1])
            street = str(proj[2])
            if street == 'None':
                street = None
            street2 = str(proj[3])
            if street2 == 'None':
                street2 = None
            city = str(proj[4])
            state = str(proj[5])
            zipcode = str(proj[6])
            zipcode = " " + zipcode
            if street:
                street = street + ", "
                if street2:
                    street2 = street2 + ", "            
                    project_dict['project_address'] = street + street2 + city + ", " + state + zipcode
                else:
                    project_dict['project_address'] = street + city + ", " + state + zipcode
            else:
                project_dict['project_address'] = city + ", " + state + zipcode
            URL = "https://geocode.search.hereapi.com/v1/geocode"
            location = project_dict['project_address']
            
            api_key = os.getenv("api_key")
            PARAMS = {'apikey':api_key,'q':location} 

            # sending get request and saving the response as response object 
            r = requests.get(url = URL, params = PARAMS) 
            data = r.json()

            latitude = data['items'][0]['position']['lat']
            longitude = data['items'][0]['position']['lng']
            project_dict['lat'] = ""
            project_dict['lng'] = ""
            if location: 
                project_dict['lat'] = latitude
                project_dict['lng'] = longitude
            revenue = str(proj[7])
            est_labor_rate = str(proj[8])
            est_labor_hours = str(proj[9])
            est_labor_expense = str(proj[10])
            act_start_date = str(proj[11])
            project_dict['act_start_date'] = act_start_date
            if str(proj[12]) != "":
                project_dict['act_end_date'] = str(proj[12])
            est_material_expense = str(proj[15])
            est_subcontractor_expense = str(proj[16])
            est_miscellaneous_expense = str(proj[17])
            est_overhead_expense = str(proj[18])
            

            #adding calculations from work on expense route to try to get expenses into the project dict
            cur = conn.cursor()
            cur.execute('SELECT * FROM expenses WHERE project_id=' + str(project_id) + ';')   
            expenses_fetch = cur.fetchall()
            print('-----------------------------------------------------------') 
            print(expenses_fetch)

            #empty lists
            mat_exp_list = []
            subcon_exp_list = []
            misc_exp_list = []
            #creating dictionaries of material expenses and appending to empty lists
            for db_row in expenses_fetch:
                mat_exp_dict = {}
                subcon_exp_dict = {}
                misc_exp_dict = {}
                if db_row[1] == "Materials":
                # if mat_exp_dict and db_row[1] == "Materials":
                    mat_exp_dict['exp_type'] = db_row[1]
                    mat_exp_dict['project_id'] = db_row[2]
                    mat_exp_dict['expense_amount'] = db_row[4]
                    mat_exp_list.append(mat_exp_dict)
                # if subcon_exp_dict and db_row[1] == "Subcontractor":
                elif db_row[1] == "Subcontractor":
                    subcon_exp_dict['exp_type'] = db_row[1]
                    subcon_exp_dict['project_id'] = db_row[2]
                    subcon_exp_dict['expense_amount'] = db_row[4]
                    subcon_exp_list.append(subcon_exp_dict)
                else:
                # if misc_exp_dict and db_row[1] == "Miscellaneous" :
                    misc_exp_dict['exp_type'] = db_row[1]
                    misc_exp_dict['project_id'] = db_row[2]
                    misc_exp_dict['expense_amount'] = db_row[4]
                    misc_exp_list.append(misc_exp_dict)


            #newstuff on saturday
            #putting expense values in list 
            mat_values_list = []
            for dict_row in mat_exp_list:
                mat_values = dict_row['expense_amount']
                mat_values_list.append(mat_values)
            
            subcon_values_list = []
            for dict_row in subcon_exp_list:
                subcon_values = dict_row['expense_amount']
                subcon_values_list.append(subcon_values)
            
            misc_values_list = []
            for dict_row in misc_exp_list:
                misc_values = dict_row['expense_amount']
                misc_values_list.append(misc_values)

            #expense totals
            total_materials_exp = round((sum(mat_values_list)),2)
            total_subcontractor_exp = round((sum(subcon_values_list)),2)
            total_miscellaneous_exp = round((sum(misc_values_list)),2)                 
            
            fin_act_mat_exp = float(total_materials_exp)
            fin_act_misc_exp = float(total_miscellaneous_exp)
            fin_act_sub_exp = float(total_subcontractor_exp)
            
            project_dict['fin_act_material_expense'] = "{:,.2f}".format(fin_act_mat_exp)
            project_dict['fin_act_miscellaneous_expense'] = "{:,.2f}".format(float(fin_act_misc_exp))
            project_dict['fin_act_subcontractor_expense'] = "{:,.2f}".format(float(fin_act_sub_exp))
            project_dict['fin_act_overhead_expense'] = "{:,.2f}".format(float(est_overhead_expense)) 


            # Fetch Time_Sheets data for given project_id
            cur = conn.cursor()
            cur.execute('SELECT * FROM time_sheets WHERE project_id=' + str(project_id) + ';')
            timesheet_data = cur.fetchall()

            # Create a list of dictionaries with Time_Sheets table data
            timesheet_all = []
            act_labor_hours = float(0)
            # Get individual timesheet_dict for display
            if not len(timesheet_data):
                print('No timesheets entered in database for this project, therefore skipping Project ID ' + str(project_id))
            for timesheet in timesheet_data:
                # Calling the pre-defined function
                (timesheet_dict, act_labor_hours) = get_timesheet_dict(timesheet, act_labor_hours, conn)
                timesheet_all.append(timesheet_dict)
            # Using the predefined function for actual labor hours, calculate actual labor rate
            act_labor_rate = get_actual_labor_rate(timesheet_all, act_labor_hours, conn)
            project_dict['act_material_expense'] = "{:,.2f}".format(total_materials_exp)
            project_dict['act_subcontractor_expense'] = total_subcontractor_exp
            project_dict['act_miscellaneous_expense'] = total_miscellaneous_exp
            project_dict["timesheets"] = timesheet_all
            project_list["project_id: "+ str(project_id)] = project_dict
            project_dict['id'] = str(project_id)
            

            # Calculations for Project Financials - Budgeted/Estimated
            fin_est_revenue = float(revenue)
            project_dict['fin_est_revenue'] = f'{float(revenue):,}'
            fin_est_labor_hours = est_labor_hours
            project_dict['fin_est_labor_hours'] = str(fin_est_labor_hours)
            fin_est_labor_rate = est_labor_rate
            project_dict['fin_est_labor_rate'] = f'{float(fin_est_labor_rate):,}'
            fin_est_labor_expense = float(fin_est_labor_hours) * float(fin_est_labor_rate)
            project_dict['fin_est_labor_expense'] = "{:,.2f}".format(fin_est_labor_expense)
            fin_est_material_expense = float(est_material_expense)
            project_dict['fin_est_material_expense'] = "{:,.2f}".format(fin_est_material_expense)
            fin_est_subcontractor_expense = float(est_subcontractor_expense)
            project_dict['fin_est_subcontractor_expense'] = "{:,.2f}".format(fin_est_subcontractor_expense)
            fin_est_miscellaneous_expense = float(est_miscellaneous_expense)
            project_dict['fin_est_miscellaneous_expense'] = "{:,.2f}".format(fin_est_miscellaneous_expense)
            fin_est_overhead_expense = float(est_overhead_expense)
            project_dict['fin_est_overhead_expense'] = "{:,.2f}".format(fin_est_overhead_expense)
            fin_est_gross_profit = float(fin_est_revenue) - float(fin_est_labor_expense) - float(fin_est_material_expense)- float(fin_est_subcontractor_expense)- float(fin_est_miscellaneous_expense)- float(fin_est_overhead_expense)
            # project_dict['fin_est_gross_profit'] = "{:.2f}".format(fin_est_gross_profit)
            project_dict['fin_est_gross_profit'] = "{:,.2f}".format(fin_est_gross_profit)
            fin_est_gross_margin = float(fin_est_gross_profit) / float(fin_est_revenue) * 100
            project_dict['fin_est_gross_margin'] = "{:,.2f}".format(fin_est_gross_margin) + " %"

            fin_est_gross_margin = float(fin_est_gross_profit) / float(fin_est_revenue) * 100
            project_dict['fin_est_gross_margin'] = "{:,.2f}".format(fin_est_gross_margin) + " %"


            # Calculations for Project Financials - Actual
            fin_act_revenue = float(revenue)
            project_dict['fin_act_revenue'] = "{:,.2f}".format(fin_act_revenue)
            fin_act_labor_hours = act_labor_hours
            project_dict['fin_act_labor_hours'] = str(fin_act_labor_hours)
            fin_act_labor_rate = act_labor_rate
            project_dict['fin_act_labor_rate'] = "{:,.2f}".format(fin_act_labor_rate)
            fin_act_labor_expense = float(fin_act_labor_hours) * float(fin_act_labor_rate)
            project_dict['fin_act_labor_expense'] = "{:,.2f}".format(fin_act_labor_expense)
            fin_act_gross_profit = float(fin_act_revenue) - float(fin_act_labor_expense)
            # project_dict['fin_act_gross_profit'] = "{:.2f}".format(fin_act_gross_profit)
            project_dict['fin_act_gross_profit'] = f'{float(fin_act_gross_profit):,}'
            fin_act_gross_margin = float(fin_act_gross_profit) / float(fin_act_revenue) * 100
            project_dict['fin_act_gross_margin'] = "{:.2f}".format(fin_act_gross_margin) + " %"
        pprint(project_list)     
        
        # Create a dictionary of dictionaries with project_details table data chosen, and output as a JSON
        return render_template('dashboard.html', project_list=json.dumps(project_list))
           
    else:
        db_read_error = 'Oops - could not read from database!'
        return render_template('error.html', error_type=db_read_error) 

      

# Route for Enter New Project page -- saves inputs to db, then redirects to Dashboard
@app.route('/new_project', methods=['GET', 'POST'])
def new_project_data():
    if request.method == 'GET':
        print('*****************')
        print('Getting form...')
        print('*****************')
        return render_template('new_project.html')    
    
    if request.method == 'POST':
        print('*****************')
        print('Posting form...')
        print('*****************')
        full_values_string = ''
        name = request.form['project_name']
        full_values_string += "(" + "'" + name + "'"
        street = request.form['street']
        full_values_string += ',' + "'" + street + "'"
        street2 = request.form['street2']
        full_values_string += ',' + "'" + street2 + "'"
        city = request.form['city']
        full_values_string += ',' + "'" + city + "'"
        state = request.form['state']
        full_values_string += ',' + "'" + state + "'"
        zipcode = request.form['zipcode']  
        full_values_string += ',' + "'" + zipcode + "'"
        revenue = str("{:.2f}".format(float(request.form['revenue'])))
        full_values_string += ',' + revenue
        est_labor_rate = str("{:.2f}".format(float(request.form['est_labor_rate'])))
        full_values_string += ',' + est_labor_rate
        est_labor_hours = request.form['est_labor_hours']
        full_values_string += ',' + est_labor_hours
        est_labor_expense = str("{:.2f}".format(float(est_labor_hours) * float(est_labor_rate)))
        full_values_string += ',' + est_labor_expense
        #adding in new expenses to grab from user input 
        est_material_expense = str("{:.2f}".format(float(request.form['est_material_expense'])))
        full_values_string += ',' + est_material_expense
        est_subcontractor_expense = str("{:.2f}".format(float(request.form['est_subcontractor_expense'])))
        full_values_string += ',' + est_subcontractor_expense
        est_miscellaneous_expense = str("{:.2f}".format(float(request.form['est_miscellaneous_expense'])))
        full_values_string += ',' + est_miscellaneous_expense
        est_overhead_rate = request.form['est_overhead_expense']
        est_overhead_expense =  float(est_overhead_rate) * float(revenue)
        est_overhead_expense = str(est_overhead_expense)
        full_values_string += ',' + est_overhead_expense
        if 'act_start_date' in request.form and request.form['act_start_date'] != "":
        # if request.form['act_start_date'] != "":
            act_start_date = datetime.datetime.strptime(request.form['act_start_date'], '%m/%d/%Y').date()
        else:
            act_start_date = datetime.datetime.now()
        full_values_string += ',' + "'" + str(act_start_date) + "'" + ')'
        

        # Print data list for database entry
        print('-------------------------------------------------------------------')
        print('Data list prepared for entry to Project_Details table in database')
        print('-------------------------------------------------------------------')
        print(full_values_string)
        print('-------------------------------------------------------------------')
        cur = conn.cursor()
        # Adding form input data to PostgreSQL database
        try:
            # cur.execute('INSERT INTO project_details (name, street, street2, city, state, zip, revenue, est_labor_rate, est_labor_hours, est_labor_expense, act_start_date, est_material_expense, est_subcontractor_expense, est_miscellaneous_expense, est_overhead_expense) VALUES ' + full_values_string + ';')
            cur.execute('INSERT INTO project_details (name, street, street2, city, state, zip, revenue, est_labor_rate, est_labor_hours, est_labor_expense,  est_material_expense, est_subcontractor_expense, est_miscellaneous_expense, est_overhead_expense, act_start_date) VALUES ' + full_values_string + ';')

           
            print('-----------------------------------')
            print('Data added to database - woohoo!')
            print('-----------------------------------')
        except:
            print('---------------------------------------')
            db_write_error = 'Oops - could not write to database!'
            print('---------------------------------------')
            return render_template('error.html', error_type=db_write_error)
        return redirect(url_for('dashboard_data'))



# Route for Enter New User page, saves inputs to db, then redirects to Dashboard
@app.route('/new_user', methods=['GET', 'POST'])
def userdata_html_to_db():
    if request.method == 'GET':
        print('*****************')
        print('Getting form...')
        print('*****************')
        return render_template('new_user.html')    
    
    if request.method == 'POST':
        print('*****************')
        print('Posting form...')
        print('*****************')
        cur = conn.cursor()
        cur.execute('SELECT log_in FROM users;')
        user_login_fetch = cur.fetchall()

        #prints a tupple
        print(user_login_fetch)
        log_in = request.form['log_in']
        for login in user_login_fetch:
            login = functools.reduce(operator.add,(login))
            print(login)
            if login == log_in: 
                error = 'Log-in name already taken Please choose another.'
                flash('Log-in name already taken Please choose another')
                print(error)
                return render_template('new_user.html', error=error)
            else:
                full_values_string = ''
                name = request.form['user_name']
                full_values_string += "(" + "'" + name + "'"
                job_title = request.form['job_title']
                full_values_string += ',' + "'" + job_title + "'"
                pay_rate = request.form['pay_rate']
                full_values_string += ',' + "'" + pay_rate + "'"
                email = request.form['email']
                full_values_string += ',' + "'" + email + "'"
                phone = request.form['phone']
                full_values_string += ',' + "'" + phone + "'"
                #log-in and hashing password 
                log_in = request.form['log_in']
                full_values_string += ',' + "'" + log_in + "'"
                password = request.form['password']
                passw = sha256_crypt.hash(password)
                full_values_string += ',' + "'" + passw + "'" + ")"
                # Print data list for database entry
                print('-------------------------------------------------------------------')
                print('Data list prepared for entry to Users table in database')
                print('-------------------------------------------------------------------')
                print(full_values_string)
                print('-------------------------------------------------------------------')
        cur = conn.cursor()
        # Adding form input data to PostgreSQL database
        try:
            cur.execute('INSERT INTO users (name, job_title, pay_rate, email, phone, log_in, password) VALUES ' + full_values_string + ';')
            print('-----------------------------------')
            print('Data added to database - woohoo!')
            print('-----------------------------------')
        except:
            print('---------------------------------------')
            db_write_error = 'Oops - could not write to database!'
            print('---------------------------------------')
            return render_template('error.html', error_type=db_write_error)
        return redirect(url_for('dashboard_data'))


# Route for new Time Entry -- saves inputs to Time_Sheets table in db, then redirects to Dashboard
@app.route('/new_time', methods=['GET', 'POST'])
def time_html_to_db():     
    if request.method == 'GET':
        # Fetch all employee names from database for dropdown menu
        cur = conn.cursor()
        cur.execute('SELECT name FROM users ORDER BY name ASC')
        employee_names_fetch = cur.fetchall()
        print('------------------------------------------------------------')   
        print('All employee names fetched from database for dropdown list')   
        print('------------------------------------------------------------')   
        print(employee_names_fetch)
        print('------------------------------------------------------------')   
        # Convert employee names to a JSON
        employee_list = []
        for db_row in employee_names_fetch:
            employee_dict = {}
            employee_dict['name'] = db_row[0]
            employee_list.append(employee_dict)
        
        # sorted_emp_list = employee_list.sort()  
        
        # Fetch all project names from database for dropdown menu
        cur.execute('SELECT name FROM project_details ORDER BY name ASC')    
        project_names_fetch = cur.fetchall()
        print('-----------------------------------------------------------')   
        print('All project names fetched from database for dropdown list')   
        print('-----------------------------------------------------------')   
        print(project_names_fetch)
        print('-----------------------------------------------------------') 
        # Convert project names to a list
        project_list = []
        for db_row in project_names_fetch:
            project_dict = {}
            project_dict['name'] = db_row[0]
            project_list.append(project_dict)
        
        # Create a dictionary for employee and project names, and convert to a JSON for the dropdown menus
        dropdown_dict = {}
        dropdown_dict['employee_list'] = employee_list
        dropdown_dict['project_list'] = project_list
        pprint(dropdown_dict)
        return render_template('enterTime.html', dropdown_dict=json.dumps(dropdown_dict))
        
    if request.method == 'POST':
        # Required fields, and missing fields check
        required_fields_list = ['employee_name', 'project_name', 'start_time', 'finish_time']
        missing_fields = []
        for req_field in required_fields_list:
            if req_field not in request.form:
                missing_fields.append(req_field)
        if len(missing_fields):
            missing_fields_error = 'Oops - could not find these fields ' + ' '.join(missing_fields)
            return render_template('error.html', error_type=missing_fields_error)
        
        # Fetching employee and project names from form input    
        employee_name = request.form['employee_name']
        project_name = request.form['project_name']
        # Fetching user_id and project_id from Users and Project Details tables in database  
        cur = conn.cursor() 
        cur.execute('SELECT user_id FROM users WHERE name=%s;', [employee_name])
        user_id_fetch = cur.fetchall()
        for user in user_id_fetch:
            user_id = user[0]  
        cur.execute('SELECT project_id FROM project_details WHERE name=%s;', [project_name])
        project_id_data = cur.fetchall()        
        for project in project_id_data:
            project_id = project[0]

        # Fetching time data from form input, and formatting it for database entry
        start_time = request.form['start_time']
        start_time = " ".join(reversed(start_time.split(" ")))
        start_time = datetime.datetime.strptime(start_time, "%m/%d/%Y %H:%M").strftime('%Y-%m-%d %H:%M:%S')
        print('Start timestamp = ' + start_time)
        start_time = str(start_time)
        finish_time = request.form['finish_time']
        finish_time = " ".join(reversed(finish_time.split(" ")))
        finish_time = datetime.datetime.strptime(finish_time, "%m/%d/%Y %H:%M").strftime('%Y-%m-%d %H:%M:%S')
        print('Finish timestamp = ' + finish_time)
        finish_time=str(finish_time)

        # Adding data to Time_Sheets table in database:
        try:
            cur = conn.cursor() 
            cur.execute("INSERT INTO time_sheets (user_id, project_id, start_time, finish_time) VALUES (%s, %s, %s, %s)", (user_id, project_id, start_time, finish_time))
            print('-----------------------------------')
            print('Data added to database - woohoo!')
            print('-----------------------------------')
        except:
            db_write_error = 'Oops - could not write to database!'
            return render_template('error.html', error_type=db_write_error)
        return redirect(url_for('dashboard_data'))

# Route for actual_expense pages -- saves inputs to db, then redirects to Dashboard
# @app.route("/enter_expense", methods=['GET', 'POST'])
@app.route("/enter_expense", methods=['GET', 'POST'])
def project_expense():
    if request.method == 'GET':
        cur = conn.cursor()            
        # Fetch all project names from database for dropdown menu
        cur.execute('SELECT name FROM project_details ORDER BY name ASC')    
        project_names_fetch = cur.fetchall()
        print('-----------------------------------------------------------')   
        print('All project names fetched from database for dropdown list')   
        print('-----------------------------------------------------------')   
        print(project_names_fetch)
        print('-----------------------------------------------------------') 
        # Convert project names to a list
        project_list = []
        for db_row in project_names_fetch:
            project_dict = {}
            project_dict['name'] = db_row[0]
            project_list.append(project_dict)
        
        # Create a dictionary for  project names, and convert to a JSON for the dropdown menus
        dropdown_dict = {}
        dropdown_dict['project_list'] = project_list
        pprint(dropdown_dict)
      
        

        return render_template('enter_expense.html', dropdown_dict=json.dumps(dropdown_dict))
    # if request.method == 'GET':
    #     print('*****************')
    #     print('Getting form...')
    #     print('*****************')
    #     cur.execute('SELECT name FROM project_details ORDER BY name ASC')    
    #     project_names_fetch = cur.fetchall()
    #     print('-----------------------------------------------------------')   
    #     print('All project names fetched from database for dropdown list')   
    #     print('-----------------------------------------------------------')   
    #     print(project_names_fetch)
    #     print('-----------------------------------------------------------') 
        # Convert project names to a list
        # project_list = []
        # for db_row in project_names_fetch:
        #     project_dict = {}
        #     project_dict['name'] = db_row[0]
        #     project_list.append(project_dict)
        # return render_template('enter_expense.html')    
    
    if request.method == 'POST':
        print('*****************')
        print('Posting form...')
        print('*****************')
        # Fetching exp type and project names from form input    
        expense_type = request.form['exp_typ']
        project_name = request.form['project_name']

         # Fetching project_id from Project Details tables in database  
        cur = conn.cursor()
        cur.execute('SELECT project_id FROM project_details WHERE name=%s;', [project_name])
        project_id_data = cur.fetchall()        
        for project in project_id_data:
            project_id = project[0]

        # Fetching data from form input for database entry
        full_values_string = ''
        expense_type = request.form['exp_typ']
        full_values_string =  "(" + "'" + expense_type + "'"
        # expense_date = datetime.datetime.strptime(request.form['expDate'], '%m/%d/%Y').date()
        # full_values_string += ',' + "'" + expense_date + "'"
        
        expense_amount = request.form['expenseAmount']
        full_values_string += ',' + "'" + expense_amount + "'"
        project_id = str(project_id)
        full_values_string += ',' + "'" + project_id + "'"  + ")"
        
        
        # Print data list for database entry
        print('-------------------------------------------------------------------')
        print('Data list prepared for entry to Project_Expense table in database')
        print('-------------------------------------------------------------------')
        print(full_values_string)
        print('-------------------------------------------------------------------')
        cur = conn.cursor()
        # Adding form input data to PostgreSQL database
        try:
            cur.execute('INSERT INTO expenses (expense_type, expense_amount, project_id) VALUES ' + full_values_string + ';')
            print('-----------------------------------')
            print('Data added to database - woohoo!')
            print('-----------------------------------')
        except:
            print('---------------------------------------')
            db_write_error = 'Oops - could not write to database!'
            print('---------------------------------------')
            return render_template('error.html', error_type=db_write_error)
        return redirect(url_for('dashboard_data'))


# Michaels route: 
# def project_expense():
#     if request.method == 'GET':
#         print('*****************')
#         print('Getting form...')
#         print('*****************')
#         return render_template('enter_expense.html')    
    
#     if request.method == 'POST':
#         print('*****************')
#         print('Posting form...')
#         print('*****************')
#         full_values_string = ''
#         name = request.form['project_name']
#         full_values_string = ''
#         act_material_expense = request.form['act_material_expense']
#         full_values_string = ''
#         act_miscellaneous_expense = request.form['act_miscellaneous_expense']
#         full_values_string = ''
#         act_overhead_expense = request.form['act_overhead_expense']
        
#         # Print data list for database entry
#         print('-------------------------------------------------------------------')
#         print('Data list prepared for entry to Project_Details table in database')
#         print('-------------------------------------------------------------------')
#         print(full_values_string)
#         print('-------------------------------------------------------------------')
#         cur = conn.cursor()
#         # Adding form input data to PostgreSQL database
#         try:
#             cur.execute('INSERT INTO expense (act_material_expense, act_subcontractor_expense, act_miscellaneous_expense) VALUES ' + full_values_string + ';')
#             print('-----------------------------------')
#             print('Data added to database - woohoo!')
#             print('-----------------------------------')
#         except:
#             print('---------------------------------------')
#             db_write_error = 'Oops - could not write to database!'
#             print('---------------------------------------')
#             return render_template('error.html', error_type=db_write_error)
#         return redirect(url_for('dashboard_data'))


# Route for queried Project_Details pages -- fetches project data from database for display, writes an input field to database
@app.route("/search", methods=['GET', 'POST'])
def project_search():    
    if request.method == 'GET':
        project_id = request.args.get("project_id")
        project_dict = search_by_id(project_id, conn)
        pprint(project_dict)

        # Create a dictionary with project_details table data chosen, and output as a JSON      
        if project_id:
            return render_template('search.html', project_dict=project_dict)
        else:
            return redirect(url_for('dashboard_data'))

        if not project_dict:
            db_read_error = 'Oops - could not read from database!'
            return render_template('error.html', error_type=db_read_error)  

    if request.method == 'POST':
        act_end_date = request.form['end_date']
        cur = conn.cursor()
        # Adding project end date to Project_Details table in database
        project_id = request.form['project_id']
        pprint(project_id)
       
        try:
            sql_insert_string = "UPDATE project_details SET act_comp_date = TO_DATE('" + act_end_date + "', 'MM/DD/YYYY') WHERE project_id=" + project_id + ";"
            print(sql_insert_string)
            cur.execute(sql_insert_string)                  
            print('-----------------------------------')
            print('Data added to database - woohoo!')
            print('-----------------------------------')
            project_dict = search_by_id(project_id, conn)
            pprint(project_dict)
            return render_template('search.html', project_dict=project_dict)
        except:
            db_write_error = 'Oops - could not write to database!'
            return render_template('error.html', error_type=db_write_error)
        return render_template('search.html')

 # Route for Enter New User page, saves inputs to db, then redirects to Dashboard
@app.route('/update_user', methods=['GET', 'POST'])
def user_data_update_db():
    if request.method == 'GET':
        print('*****************')
        print('Getting form...')
        print('*****************')
    # Fetch all employee names from database for dropdown menu
        cur = conn.cursor()
        cur.execute('SELECT name FROM users ORDER BY name ASC')
        employee_names_fetch = cur.fetchall()
        print('------------------------------------------------------------')   
        print('All employee names fetched from database for dropdown list')   
        print('------------------------------------------------------------')   
        print(employee_names_fetch)
        print('------------------------------------------------------------')   
        # Convert employee names to a JSON
        employee_list = []
        for db_row in employee_names_fetch:
            employee_dict = {}
            employee_dict['name'] = db_row[0]
            employee_list.append(employee_dict)

        # Create a dictionary for employee and convert to a JSON for the dropdown menus
        dropdown_dict = {}
        dropdown_dict['employee_list'] = employee_list
        pprint(dropdown_dict)
        return render_template('updateUser.html', dropdown_dict=json.dumps(dropdown_dict))


        # return render_template('new_user.html')    
    
    if request.method == 'POST':
        drop_name = request.form['employee_name']
        
        print(drop_name)
        cur = conn.cursor() 
        # cur.execute('SELECT password FROM users ;')
        cur.execute('SELECT * FROM users WHERE name=%s;', [drop_name])
        user_info_fetch = cur.fetchall()
        print(user_info_fetch)
        print('*****************')
        print('Posting form...')
        print('*****************')
        user_dict_list = []
        for db_row in user_info_fetch:
            user_dict = {}
            db_user_id = db_row[0]
            
            db_name = db_row[3]
            user_dict['name'] = db_name
            db_job_title = db_row[1]
            user_dict['job_title'] = db_job_title
            db_pay_rate = db_row[2]
            user_dict['pay_rate'] = db_pay_rate
            db_email = db_row[4]
            user_dict['email'] = db_email
            db_phone = db_row[5]
            user_dict['phone'] = db_phone
            db_log_in = db_row[6]
            user_dict['log_in'] = db_log_in
            db_password = db_row[7]
            user_dict_list.append(user_dict)

        print(db_user_id)
        print(db_name)
        print(db_job_title)
        print(db_pay_rate)
        print(db_email)
        print(db_phone)
        print(db_log_in)
        print(db_password)


        name = request.form['user_name']
        if name != "" :
            name = request.form['user_name']
        else:
            name = db_name
        
        job_title = request.form['job_title']
        if job_title != "" :
            job_title = request.form['job_title']
        else:
            job_title = db_job_title

        pay_rate = request.form['pay_rate']
        if pay_rate != "" :
            pay_rate = request.form['pay_rate']
        else:
            pay_rate = db_pay_rate
                
        email = request.form['email']
        if email != "" :
            email = request.form['email']
        else:
            email = db_email

        phone = request.form['phone']
        if phone != "" :
            phone = request.form['phone']
        else:
            phone = db_phone


        log_in = request.form['log_in']
        if log_in != "" :
            log_in = request.form['log_in']
        else:
            log_in = db_log_in

        password = request.form['password']
        if password != "" :
            passw = sha256_crypt.hash(password)
        else:
            passw = db_password



        full_values_string = ''
        # name = request.form['user_name']
        full_values_string += "(" + "'" + name + "'"
        # job_title = request.form['job_title']
        full_values_string += ',' + "'" + job_title + "'"
        # pay_rate = request.form['pay_rate']
        full_values_string += ',' + "'" + str(pay_rate) + "'"
        # email = request.form['email']
        full_values_string += ',' + "'" + email + "'"
        # phone = request.form['phone']
        full_values_string += ',' + "'" + phone + "'"
        # #log-in and hashing password 
        # log_in = request.form['log_in']
        full_values_string += ',' + "'" + log_in + "'"
        # password = request.form['password']
        # passw = sha256_crypt.hash(password)
        full_values_string += ',' + "'" + passw + "'" + ")"
        # # Print data list for database entry
        print('-------------------------------------------------------------------')
        print('Data list prepared for entry to Users table in database')
        print('-------------------------------------------------------------------')
        print(full_values_string)
        print('-------------------------------------------------------------------')
        cur = conn.cursor()
        print(f"UPDATE users SET name ='{name}', job_title ='{job_title}' , pay_rate ='{pay_rate}', email ='{email}', phone = '{phone}', log_in ='{log_in}', password = '{passw}'  WHERE user_id = {db_user_id}")
        # Adding form input data to PostgreSQL database
        try:
            cur.execute(f"UPDATE users SET name ='{name}', job_title ='{job_title}' , pay_rate ='{pay_rate}', email ='{email}', phone = '{phone}', log_in ='{log_in}', password = '{passw}'  WHERE user_id = {db_user_id}")

            # cur.execute('UPDATE  users SET (name, job_title, pay_rate, email, phone, log_in, password) VALUES ' + full_values_string + ';')
            # cur.execute('UPDATE  users SET job_title = job_title , pay_rate = pay_rate , name = name , email = email, phone = phone, log_in = log_in, password = passw WHERE user_id = db_user_id ;')
            # cur.execute('UPDATE users SET name = name WHERE user_id = db_user_id ;')
            # cur.execute('UPDATE users SET name=%s',[name], ' WHERE user_id=%s;', [db_user_id])
            # cur.execute('UPDATE users SET name=%s',[name], ' WHERE user_id=' + [db_user_id] + ";")
            # sql_insert_string = "UPDATE users SET name = ('" + name + "') WHERE project_id=" + db_user_id + ";"
            # print(sql_insert_string)
            # cur.execute(sql_insert_string)
           # cur.execute('UPDATE  users SET (name = name, job_title = job_title , pay_rate = pay_rate , email = email, phone = phone, log_in = log_in, password = passw) WHERE user_id = db_user_id ;')
            print('-----------------------------------')
            print('Data added to database - woohoo!')
            print('-----------------------------------')
        except:
            print('---------------------------------------')
            db_write_error = 'Oops - could not write to database!'
            print('---------------------------------------')
            return render_template('error.html', error_type=db_write_error)
        return redirect(url_for('dashboard_data'))

#THIS ROUTE DOES NOT WORK YET       
# @app.route('/update_project', methods=['GET', 'POST'])
# def project_data_update_db():
#     if request.method == 'GET':
#         print('*****************')
#         print('Getting form...')
#         print('*****************')
    # Fetch all project names from database for dropdown menu
        # cur = conn.cursor()
        # cur.execute('SELECT name FROM project_details ORDER BY name ASC')    
        # project_names_fetch = cur.fetchall()
        # print('-----------------------------------------------------------')   
        # print('All project names fetched from database for dropdown list')   
        # print('-----------------------------------------------------------')   
        # print(project_names_fetch)
        # print('-----------------------------------------------------------') 
        # Convert project names to a list
        # project_list = []
        # for db_row in project_names_fetch:
        #     project_dict = {}
        #     project_dict['name'] = db_row[0]
        #     project_list.append(project_dict)
        
        # Create a dictionary for employee and project names, and convert to a JSON for the dropdown menus
        # dropdown_dict = {}
        # dropdown_dict['project_list'] = project_list
        # pprint(dropdown_dict)
        # return render_template('updateProject.html', dropdown_dict=json.dumps(dropdown_dict))


        # return render_template('new_user.html')    
    
    # if request.method == 'POST':
    #     drop_name = request.form['project_name']
        
    #     print(drop_name)
    #     cur = conn.cursor() 
        # cur.execute('SELECT password FROM users ;')
        # cur.execute('SELECT * FROM project_details WHERE name=%s;', [drop_name])
        # project_info_fetch = cur.fetchall()
        # print(project_info_fetch)
        # print('*****************')
        # print('Posting form...')
        # print('*****************')
        # project_dict_list = []
        # for db_row in project_info_fetch:
        #     project_dict = {}
        #     db_project_id = db_row[0]
            
        #     db_name = db_row[1]
        #     user_dict['name'] = db_name

        #     db_street = db_row[2]
        #     user_dict['street'] = db_street

        #     db_street2 = db_row[3]
        #     user_dict['street2'] = db_street2

        #     db_city = db_row[4]
        #     user_dict['city'] = db_city

        #     db_state = db_row[5]
        #     user_dict['state'] = db_state

        #     db_zip = db_row[6]
        #     user_dict['zip'] = db_zip

        #     db_revenue = db_row[7]
        #     user_dict['revenue'] = db_revenue

        #     db_est_labor_rate = db_row[8]
        #     user_dict['est_labor_rate'] = db_est_labor_rate

        #     db_est_labor_hours = db_row[9]
        #     user_dict['est_labor_hours'] = db_est_labor_hours

        #     db_est_labor_expense = db_row[10]
        #     user_dict['est_labor_rate'] = db_est_labor_rate

        #     db_act_start_date = db_row[11]
        #     user_dict['act_start_date'] = db_act_start_date

        #     db_act_comp_date = db_row[12]
        #     user_dict['act_comp_date'] = db_act_comp_date
            
            #13 lat
            #14 lon

        #     db_est_material_expense = db_row[15]
        #     user_dict['est_material_expense'] = db_est_material_expense

        #     db_est_subcontractor_expense = db_row[16]
        #     user_dict['est_subcontractor_expense'] = db_est_subcontractor_expense

        #     db_est_miscellaneous_expense = db_row[17]
        #     user_dict['est_miscellaneous_expense'] = db_est_miscellaneous_expense

        #     db_est_overhead_expense = db_row[17]
        #     user_dict['est_overhead_expense'] = db_est_overhead_expense




        #     project_dict_list.append(project_dict)

        # print(db_project_id)
        # print(db_name)
        # print(db_revenue)
        # print(db_est_labor_hours)
        # print(db_est_labor_rate)
        # print(db_est_labor_expense)
        # print(db_act_start_date)
        # print(db_act_comp_date)
        # print(db_est_material_expense)
        # print(db_est_subcontractor_expense)
        # print(db_est_miscellaneous_expense)
        # print(db_est_overhead_expense)


        # name = request.form['project_name']
        # if name != "" :
        #     name = request.form['project_name']
        # else:
        #     name = db_name
        
        # street = request.form['street']
        # if street != "" :
        #     street = request.form['street']
        # else:
        #     street = db_street

        # street2 = request.form['street2']
        # if pay_rate != "" :
        #     pay_rate = request.form['street2']
        # else:
        #     street2 = db_street2
                
        # city = request.form['city']
        # if city != "" :
        #     city = request.form['city']
        # else:
        #     city = db_city

        # state = request.form['state']
        # if state != "" :
        #     state = request.form['state']
        # else:
        #     state = db_state


        # zipcode = request.form['zipcode']
        # if zipcode != "" :
        #     zipcode = request.form['zipcode']
        # else:
        #     zipcode = db_zip

        # revenue = request.form['revenue']
        # if revenue != "" :
        #     revenue = request.form['revenue']
        # else:
        #     revenue = db_revenue

        # est_labor_rate = request.form['est_labor_rate']
        # if est_labor_rate != "" :
        #     est_labor_rate = request.form['est_labor_rate']
        # else:
        #     est_labor_rate = db_est_labor_rate
        
        # est_labor_hours = request.form['est_labor_hours']
        # if est_labor_hours != "" :
        #     est_labor_hours = request.form['est_labor_hours']
        # else:
        #     est_labor_hours = db_est_labor_hours

        #calulation of est_expense_labor based on est hours and rate
        # est_labor_expense = str((float(est_labor_hours) * float(est_labor_rate)))
        # est_labor_expense = request.form['est_labor_expense']
        # if est_labor_expense != "" :
        #     est_labor_expense = request.form['est_labor_expense']
        # else:
        #     est_labor_expense = db_est_labor_expense

        # est_material_expense = request.form['est_material_expense']
        # if est_material_expense != "" :
        #     est_material_expense = request.form['est_material_expense']
        # else:
        #     est_material_expense = db_est_material_expense

        # est_subcontractor_expense = request.form['est_subcontractor_expense']
        # if est_subcontractor_expense != "" :
        #     est_subcontractor_expense = request.form['est_subcontractor_expense']
        # else:
        #     est_subcontractor_expense = db_est_subcontractor_expense
        
        # est_miscellaneous_expense = request.form['est_miscellaneous_expense']
        # if est_miscellaneous_expense != "" :
        #     est_miscellaneous_expense = request.form['est_miscellaneous_expense']
        # else:
        #     est_miscellaneous_expense = db_est_miscellaneous_expense

        # est_overhead_expense = request.form['est_overhead_expense']
        # if est_overhead_expense != "" :
        #     est_overhead_expense = request.form['est_overhead_expense']
        # else:
        #     est_overhead_expense = db_est_overhead_expense

        
        # if 'act_start_date' in request.form and request.form['act_start_date'] != "":
        #     act_start_date = datetime.datetime.strptime(request.form['act_start_date'], '%m/%d/%Y').date()
        # else:
        #     act_start_date = db_act_start_date
        
        # if 'act_comp_date' in request.form and request.form['act_comp_date'] != "":
        #     act_comp_date = datetime.datetime.strptime(request.form['act_comp_date'], '%m/%d/%Y').date()
        # else:
        #     act_comp_date = db_act_comp_date          

        # print('-------------------------------------------------------------------')
        # cur = conn.cursor()
        # print(f"UPDATE project_details SET name ='{name}', street ='{street}' , street2 ='{street2}', city ='{city}', state = '{state}', zip ='{zipcode}', revenue = '{revenue}', est_labor_rate = '{est_labor_rate}', est_labor_hours = '{est_labor_hours}', est_labor_expense = '{est_labor_expense}', act_start_date = '{act_start_date}', act_comp_date = '{act_comp_date}', est_material_expense = '{est_material_expense}', est_subcontractor_expense = '{est_subcontractor_expense}', est_miscellaneous_expense = '{est_miscellaneous_expense}', est_overhead_expense = '{est_overhead_expense}'  WHERE project_id = {db_project_id}")
        # Adding form input data to PostgreSQL database
        # try:
            # cur.execute(f"UPDATE users SET name ='{name}', job_title ='{job_title}' , pay_rate ='{pay_rate}', email ='{email}', phone = '{phone}', log_in ='{log_in}', password = '{passw}'  WHERE user_id = {db_user_id}")
        #     cure.execute(f"UPDATE project_details SET name ='{name}', street ='{street}' , street2 ='{street2}', city ='{city}', state = '{state}', zip ='{zipcode}', revenue = '{revenue}', est_labor_rate = '{est_labor_rate}', est_labor_hours = '{est_labor_hours}', est_labor_expense = '{est_labor_expense}', act_start_date = '{act_start_date}', act_comp_date = '{act_comp_date}', est_material_expense = '{est_material_expense}', est_subcontractor_expense = '{est_subcontractor_expense}', est_miscellaneous_expense = '{est_miscellaneous_expense}', est_overhead_expense = '{est_overhead_expense}'  WHERE project_id = {db_project_id}")
        #     print('-----------------------------------')
        #     print('Data added to database - woohoo!')
        #     print('-----------------------------------')
        # except:
        #     print('---------------------------------------')
        #     db_write_error = 'Oops - could not write to database!'
        #     print('---------------------------------------')
        #     return render_template('error.html', error_type=db_write_error)
        # return redirect(url_for('dashboard_data'))



# Close database connection
    if(conn):
        cur.close()
        conn.close()
        print('PostgreSQL connection is closed')

if __name__ == "__main__":
    app.run(debug=True)