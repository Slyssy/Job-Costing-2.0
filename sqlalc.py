# Setup dependencies
import os
import psycopg2
import requests
from flask import Flask, render_template, request, redirect, url_for, json, jsonify
import datetime
from pprint import pprint
import ssl
from crud import *
import hashlib
from passlib.hash import sha256_crypt
import functools
import operator
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, String, Float

# Import Postgres database details from config file
pg_ipaddress = os.getenv("pg_ipaddress")
pg_port = os.getenv("pg_port")
pg_username = os.getenv("pg_username")
pg_password = os.getenv("pg_password")
pg_dbname = os.getenv("pg_dbname")

#setup sqlalchemy connection with Posgres 

# Base = declarative_base()

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

# class Users(Base):
#     __tablename__ = "users"

#     user_id = Column(Integer, primay_key=True)
#     job_title = Column(String(50))
#     pay_rate = Column (Float)
#     name = Column(String(50))
#     email = Column(String)
#     phone = Column(String(20))
#     log_in = Column(String(30))
#     password = Column(String(150))

# engine = create_engine("")

    
 # Route for Enter New User page, saves inputs to db, then redirects to Dashboard
@app.route('/update_user', methods=['GET', 'POST'])
def userdata_html_to_db():
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
        return render_template('enterTime.html', dropdown_dict=json.dumps(dropdown_dict))


        return render_template('new_user.html')    
    
    if request.method == 'POST':
        name = request.form['employee_name']
        
        print(name)
        cur = conn.cursor() 
        # cur.execute('SELECT password FROM users ;')
        cur.execute('SELECT password FROM users WHERE log_in=%s;', [log_in])
        rows = cur.fetchall()









        print('*****************')
        print('Posting form...')
        print('*****************')
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
   