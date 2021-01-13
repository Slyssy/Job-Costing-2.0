@app.route('/update_project', methods=['GET', 'POST'])
def new_project_data():
    if request.method == 'GET':
        print('*****************')
        print('Getting form...')
        print('*****************')
        return render_template('updateExp.html')    
    
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
        material_expense = str("{:.2f}".format(float(material_expense) * float(material_expense)))
        full_values_string += ',' + material_expense
        subcontractor_expense = str("{:.2f}".format(float(subcontractor_expense) * float(subcontractor_expense)))
        full_values_string += ',' + subcontractor_expense
        misc_expense = str("{:.2f}".format(float(misc_expense) * float(misc_expense)))
        full_values_string += ',' + misc_expense
        overhead_exp = str("{:.2f}".format(float(overhead_exp) * float(overhead_exp)))
        full_values_string += ',' + overhead_exp
        if 'act_start_date' in request.form and request.form['act_start_date'] != "":
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
            cur.execute('INSERT INTO project_details (name, street, street2, city, state, zip, revenue, est_labor_rate, est_labor_hours, est_labor_expense, act_start_date) VALUES ' + full_values_string + ';')
            print('-----------------------------------')
            print('Data added to database - woohoo!')
            print('-----------------------------------')
        except:
            print('---------------------------------------')
            db_write_error = 'Oops - could not write to database!'
            print('---------------------------------------')
            return render_template('error.html', error_type=db_write_error)
        return redirect(url_for('dashboard_data'))
