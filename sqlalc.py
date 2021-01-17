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
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

# Import Postgres database details from config file
pg_ipaddress = os.getenv("pg_ipaddress")
pg_port = os.getenv("pg_port")
pg_username = os.getenv("pg_username")
pg_password = os.getenv("pg_password")
pg_dbname = os.getenv("pg_dbname")

#setup sqlalchemy connection with Posgres 

Base = declarative_base()

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

class Users(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primay_key=True)
    job_title = Column(String(50))
    pay_rate = Column (Float)
    name = Column(String(50))
    email = Column(String)
    phone = Column(String(20))
    log_in = Column(String(30))
    password = Column(String(150))

engine = create_engine("")

    
    