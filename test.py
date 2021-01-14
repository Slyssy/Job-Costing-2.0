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
log_in_name = "bob"
cur.execute('SELECT password from users WHERE log_in=%s;', [log_in_name])
# cur.execute('SELECT log_in, password from users')
rows = cur.fetchall()

#creates [('password',)]
print(rows)
#creates ('password',)
print(rows[0])

tup= rows[0] 

strpass = functools.reduce(operator.add,(tup))
print(strpass)

# def convertTuple(tup):
#     str = functools.reduce(operator.add,(tup))
#     print (str)

if "passbob20" == strpass:
    print ("it matches")
else:
    print("does not match")

if "passbob20" == strpass:
    print ("it matches")
else:
    print("does not match")

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
    

cur.close()