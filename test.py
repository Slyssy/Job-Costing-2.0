import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for, json, jsonify
import datetime
from pprint import pprint
import certifi
import ssl
import geopy.geocoders
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from crud import *
import hashlib
from passlib.hash import sha256_crypt
import functools
import operator

ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx

geolocator = Nominatim(scheme='http', user_agent='proj_job_costing')

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
    

# Create Flask app instance
app = Flask(__name__)



# Route for Index page -- Homepage and Intro to the App
# @app.route("/", methods=['GET'])
# def index():
#     return render_template("index.html")

# log_in_name = request.form['employee_name']
# log_in_name = "bob"
# cur.execute('SELECT password from users WHERE log_in=%s;', [log_in_name])
# cur.execute('SELECT log_in, password from users')
# rows = cur.fetchall()

#creates [('password',)]
# print(rows)
#creates ('password',)
# print(rows[0])

# tup= rows[0] 

# strpass = functools.reduce(operator.add,(tup))
# print(strpass)
# hashed_strpass = sha256_crypt.hash("strpass")
# print(hashed_strpass)

#will need to hash string to match (most) passwords in db

# def convertTuple(tup):
#     str = functools.reduce(operator.add,(tup))
#     print (str)

# if "passbob20" == strpass:
#     print ("it matches")
# else:
#     print("does not match")

# if "passbob20" == strpass:
#     print ("it matches")
# else:
#     print("does not match")

# for r in rows:
#     password = r[0]

# # if "bob" == rows[0]:
# #     print ("it matches")
# # else:
# #     print("does not match")

# for r in rows:
#     if "bob" == r[0]:
#         print ("it matches")
#     else:
#         print ("does not match")    
    

# cur.close()

# Route for new Time Entry -- saves inputs to Time_Sheets table in db, then redirects to Dashboard
@app.route('/new_time', methods=['GET', 'POST'])
def time_html_to_db():     
    if request.method == 'GET':
        # Fetch all employee names from database for dropdown menu
        cur = conn.cursor()
        cur.execute('SELECT name FROM users')
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
        
        # Fetch all project names from database for dropdown menu
        cur.execute('SELECT name FROM project_details')    
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

