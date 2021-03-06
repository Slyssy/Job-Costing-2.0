import datetime
import pandas as pd


def search_by_id(project_id, conn):
    print('I am here: project_id=' + project_id)
    """Define query by project_id"""
    cur = conn.cursor()
    # Fetch data from Project_Details table based on project_id
    if project_id:
        cur.execute('SELECT * FROM project_details WHERE project_id=%s', [project_id]);
    # Fetch all data from Project_Details table if no project_id is specified
    else:
        cur.execute('SELECT * FROM project_details' + ';')
    project_details_data = cur.fetchall()
    print('*****************************************')
    print('Data fetched from Project_Details table')
    print('*****************************************')
    # Create a list of dictionaries with Project_Details table data
    for proj in project_details_data:
        project_list = {}
        project_id = str(proj[0])
        project_list['project_name'] = str(proj[1])
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
                project_list['project_address'] = street + street2 + city + ", " + state + zipcode
            else:
                project_list['project_address'] = street + city + ", " + state + zipcode
        else:
            project_list['project_address'] = city + ", " + state + zipcode
        revenue = str(proj[7])
        est_labor_rate = str(proj[8])
        est_labor_hours = str(proj[9])
        est_labor_expense = str(proj[10])
        act_start_date = str(proj[11])
        project_list['act_start_date'] = act_start_date
        if str(proj[12]):
            project_list['act_end_date'] = str(proj[12])
        est_material_expense = str(proj[15])
        est_subcontractor_expense = str(proj[16])
        est_miscellaneous_expense = str(proj[17])
        est_overhead_expense = str(proj[18])
                        
        # Fetch Time_Sheets data for given project_id
        cur = conn.cursor()
        print('Project ID = ' + str(project_id))
        cur.execute('SELECT * FROM time_sheets WHERE project_id=' + str(project_id) + ';')
        timesheet_data = cur.fetchall()
        print('------------------------------------------')
        print('Data fetched from Time_Sheets table')
        print('------------------------------------------')
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
        
        # print(exp_dict)
        print(mat_exp_list)
        print(subcon_exp_list)
        print(misc_exp_list)
        print('-----------------------------------------------------------')

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
        # total_subcontractor_exp = sum(list_subcon_values)
        # total_miscellaneous_exp = sum(list_misc_values)


        # print(exp_dict)
        print('-----------------------------------------------------------') 
        print(mat_exp_list)
        print('-----------------------------------------------------------') 
        print(mat_values_list)
        print(f'this is the total materials value {total_materials_exp}')
        print('-----------------------------------------------------------')
        print(subcon_exp_list)
        print(f'this is the total subcontractor value {total_subcontractor_exp}')
        print('-----------------------------------------------------------') 
        print(misc_exp_list)
        print(f'this is the total misc value {total_miscellaneous_exp}')
        print('-----------------------------------------------------------')

        #OLD CODE - For use with pandas
        #creating dataframes from list of dictionaries 
        # mat_df = pd.DataFrame(mat_exp_list) 
        # subcon_df = pd.DataFrame(subcon_exp_list)
        # misc_df = pd.DataFrame(misc_exp_list)


        # print("Dataframes")
        # print(mat_df)
        # print(subcon_df)
        # print(misc_df)
        # print('-----------------------------------------------------------')

        #getting the values (series?) for the amount columns in each expense dataframe

        # mat_df_values = mat_df['expense_amount'].values
        # subcon_df_values = subcon_df['expense_amount'].values
        # misc_df_values = misc_df['expense_amount'].values

        #Eds fix:
        # mat_df_values = mat_df['expense_amount'].values if 'expense_amount' in mat_df.columns else []
        # subcon_df_values = subcon_df['expense_amount'].values if 'expense_amount' in subcon_df.columns else []
        # misc_df_values = misc_df['expense_amount'].values if 'expense_amount' in misc_df.columns else []

        # list_mat_values = list(mat_df_values)
        # list_subcon_values = list(subcon_df_values)
        # list_misc_values = list(misc_df_values)
        
        #End old code#

        # Calculations for Project Financials - Budgeted/Estimated

        fin_est_revenue = revenue

        project_list['fin_est_revenue'] = f'{float(revenue):,}'
        fin_est_labor_hours = est_labor_hours
        project_list['fin_est_labor_hours'] = str(fin_est_labor_hours)
        fin_est_labor_rate = float(est_labor_rate)
        project_list['fin_est_labor_rate'] = "{:.2f}".format(fin_est_labor_rate)
        fin_est_labor_expense = float(fin_est_labor_hours) * float(fin_est_labor_rate)
        # "{:.2f}".format(fin_act_labor_rate)
        project_list['fin_est_labor_expense'] = "{:.2f}".format(fin_est_labor_expense)
        fin_est_material_expense = float(est_material_expense)
        project_list['fin_est_material_expense'] = "{:.2f}".format(fin_est_material_expense)
        fin_est_subcontractor_expense = float(est_subcontractor_expense)
        project_list['fin_est_subcontractor_expense'] = "{:.2f}".format(fin_est_subcontractor_expense)
        fin_est_miscellaneous_expense = float(est_miscellaneous_expense)
        project_list['fin_est_miscellaneous_expense'] = "{:.2f}".format(fin_est_miscellaneous_expense)
        #if we decide to keep oh expense as an amount entry (not %) in db
        fin_est_overhead_expense = float(est_overhead_expense) 
        project_list['fin_est_overhead_expense'] = "{:.2f}".format(fin_est_overhead_expense)
        # fin_est_overhead_expense = float(est_overhead_expense) / float(revenue) * 100
        # project_list['fin_est_overhead_expense'] = "{:.2f}".format(fin_est_overhead_expense) + " %"
        fin_est_gross_profit = float(fin_est_revenue) - float(fin_est_labor_expense) - float(fin_est_material_expense)- float(fin_est_subcontractor_expense)- float(fin_est_miscellaneous_expense)- float(fin_est_overhead_expense)
        # project_dict['fin_est_gross_profit'] = "{:.2f}".format(fin_est_gross_profit)
        project_list['fin_est_gross_profit'] = "{:.2f}".format(fin_est_gross_profit)
        fin_est_gross_margin = float(fin_est_gross_profit) / float(fin_est_revenue) * 100
        project_list['fin_est_gross_margin'] = "{:.2f}".format(fin_est_gross_margin) + " %"


        # Calculations for Project Financials - Actual
        fin_act_revenue = float(revenue)
        project_list['fin_act_revenue'] = "{:.2f}".format(fin_act_revenue)
        fin_act_labor_hours = act_labor_hours
        project_list['fin_act_labor_hours'] = str(fin_act_labor_hours)
        fin_act_labor_rate = act_labor_rate
        project_list['fin_act_labor_rate'] = "{:.2f}".format(fin_act_labor_rate)
        fin_act_labor_expense = float(fin_act_labor_hours) * float(fin_act_labor_rate)
        project_list['fin_act_labor_expense'] = "{:.2f}".format(fin_act_labor_expense)
        
        #added in additional expense calculations here 
        fin_act_mat_exp = float(total_materials_exp)
        project_list['fin_act_material_expense'] = "{:.2f}".format(fin_act_mat_exp)
        # fin_act_material_expense = (total_materials_exp)
        # project_list['fin_est_material_expense'] = f'{float(fin_est_material_expense):,}'
        fin_act_subcon_exp = float(total_subcontractor_exp)
        project_list['fin_act_subcontractor_expense'] = "{:.2f}".format(fin_act_subcon_exp)
        fin_act_misc_exp = float(total_miscellaneous_exp)
        project_list['fin_act_miscellaneous_expense'] = "{:.2f}".format(fin_act_misc_exp)
        #if we decide to keep oh expense as an amoutn entry (not %) in db
        fin_act_overhead_expense = float(est_overhead_expense) 
        project_list['fin_act_overhead_expense'] = "{:.2f}".format(fin_act_overhead_expense)
        # fin_act_overhead_expense = float(est_overhead_expense) / float(revenue) * 100
        # project_list['fin_act_overhead_expense'] = "{:.2f}".format(fin_act_overhead_expense) + " %" 

        #updated gp calculation to include additional expenses
        fin_act_gross_profit = round((float(fin_act_revenue) - float(fin_act_labor_expense) - fin_act_mat_exp - fin_act_subcon_exp - fin_act_misc_exp - fin_act_overhead_expense),2)
        # project_list['fin_act_gross_profit'] = "{:.2f}".format(fin_act_gross_profit)
        project_list['fin_act_gross_profit'] = "{:.2f}".format(fin_act_gross_profit)
        fin_act_gross_margin = float(fin_act_gross_profit) / float(fin_act_revenue) * 100
        project_list['fin_act_gross_margin'] = "{:.2f}".format(fin_act_gross_margin) + " %"

    return project_list

def get_timesheet_dict(timesheet, act_labor_hours, conn):
    """Function for individual timesheet calculations - used later for Dashboard route"""
    timesheet_dict = {}
    timesheet_dict['project_id'] = str(timesheet[2])
    user_id = str(timesheet[1])
    timesheet_dict['user_id'] = user_id
    # Fetch user data from Users table
    cur = conn.cursor()
    cur.execute('SELECT user_id, name, pay_rate FROM users WHERE user_id=' + str(user_id));
    user_data = cur.fetchall()
    for user in user_data:
        employee_name = user[1]
        timesheet_dict['employee_name'] = employee_name
        hourly_pay_rate = user[2]
        timesheet_dict['hourly_pay_rate'] = hourly_pay_rate
                
    # Time Calculations
    timesheet_dict['start_time'] = str(timesheet[3])
    timesheet_dict['finish_time'] = str(timesheet[4])
    # Calculate difference of two Datetime objects to find hours worked
    start_time = str(timesheet[3])
    start_time = datetime.datetime.strptime(start_time,'%Y-%m-%d %H:%M:%S')
    finish_time = str(timesheet[4])
    finish_time = datetime.datetime.strptime(finish_time,'%Y-%m-%d %H:%M:%S')     
    # Outputs a timedelta object   
    time_difference = finish_time - start_time
    # Convert time worked into hours worked
    hours_worked = float("{:.2f}".format(time_difference.total_seconds() / 3600))
    timesheet_dict['hours_worked'] = hours_worked    
    act_labor_hours += hours_worked
    return (timesheet_dict, act_labor_hours)

def get_actual_labor_rate(timesheet_all, act_labor_hours, conn):
    """ Function for actual labor rate calculations from timesheets - used later for Dashboard route"""
    sum_of_hours_t_rate = 0
    if not len(timesheet_all):
        print('Empty array - project has no timesheets')
        return 0
    for timesheet_dict in timesheet_all:
        sum_of_hours_t_rate += float(timesheet_dict['hours_worked']) * float(timesheet_dict['hourly_pay_rate'])
    return (float(sum_of_hours_t_rate)/act_labor_hours)


#started making changes here. If doesn't work -- delete and keep what was done on the add expense route
    # def get_act_expenses(project_expense, act_project_expense, conn):
    # """Function for individual timesheet calculations - used later for Dashboard route"""
    # timesheet_dict = {}
    # timesheet_dict['project_id'] = str(timesheet[2])
    # user_id = str(timesheet[1])
    # timesheet_dict['user_id'] = user_id
    # # Fetch user data from Users table
    # cur = conn.cursor()
    # cur.execute('SELECT user_id, name, pay_rate FROM users WHERE user_id=' + str(user_id));
    # user_data = cur.fetchall()
    # for user in user_data:
    #     employee_name = user[1]
    #     timesheet_dict['employee_name'] = employee_name
    #     hourly_pay_rate = user[2]
    #     timesheet_dict['hourly_pay_rate'] = hourly_pay_rate
    
#this isn't being used - jg 
# def act_exp_by_id(project_id, conn):
#     print('I am here: project_id=' + project_id)
#     """Define query by project_id"""
#     cur = conn.cursor()
#     # Fetch data from Expenses table based on project_id
#     if project_id:
#         cur.execute('SELECT * FROM expenses WHERE project_id=%s', [project_id]);
#     # Fetch all data from Project_Details table if no project_id is specified
#     else:
#         cur.execute('SELECT * FROM project_details' + ';')
#     project_details_data = cur.fetchall()
#     print('*****************************************')
#     print('Data fetched from Project_Details table')
#     print('*****************************************')
#     print(project_details_data)