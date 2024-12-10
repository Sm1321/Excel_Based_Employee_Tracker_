import streamlit as st
import pandas as pd
import os
import datetime
from PIL import Image



# Display the image
# Open and resize the image
image = Image.open("SSA_Logo.jpg")
resized_image = image.resize((250, 90)) # Resize to 200x200 pixels
# Display the resized image
st.image(resized_image)

# import os
# st.write(os.listdir())
# # Get the current working directory
# current_directory = os.getcwd()
# # List the files in the current directory
# files_in_directory = os.listdir(current_directory)
# # Display the directory and files in Streamlit
# st.write(f"Current Directory: {current_directory}")
# st.write("Files in Directory:")
# st.write(files_in_directory)



# Function to load data from CSV or create new DataFrame
#Here , we check if the CSV files are there or not , if not there , we can creet new and save it locally
def load_data():
    if os.path.exists('main_table.csv') and os.path.exists('employee_list.csv') and os.path.exists('project_list.csv') and os.path.exists('project_resource_table.csv'):
        # Load data from existing CSV files
        main_table = pd.read_csv('main_table.csv')
        employee_list = pd.read_csv('employee_list.csv')
        project_list = pd.read_csv('project_list.csv')
        project_resource_table = pd.read_csv('project_resource_table.csv')
    else:
        # Initialize default DataFrames
        main_table = pd.DataFrame({
            'WeekEnd Date': ['2024-12-02', '2024-11-29', '2024-11-28', '2024-12-03', '2024-12-04'],
            'Employee Name': ['Ram', 'Laxman', 'Ram', 'Charan', 'Laxman'],
            'Project Name': ['Project A', 'Project B', 'Project C', 'Project D', 'Project E'],
            'Time(in hours)': [50, 60, 50, 80, 40]
        })

        employee_list = pd.DataFrame({
            'Employee Name': ['Ram', 'Laxman', 'Charan'],
            'Position': ['Analyst', 'Developer', 'Analyst'],
            'Skills': ['Python,Excel', 'Java, SQL', 'R, Analytics'],
            'CurrentStatus': ['Active', 'Active', 'Active']
        })

        project_list = pd.DataFrame({
            'Project Name': ['Project A', 'Project B', 'Project C', 'Project D', 'Project E'],
            'Description': ['Analysis', 'Development', 'Testing', 'Reporting', 'Design'],
            'Start Date': ['2024-12-02', '2024-11-29', '2024-11-28', '2024-12-03', '2024-12-04'],
            'Expected to Complete(Weeks)': [4, 6, 8, 3, 5],
            'Internal/External': ['Internal', 'External', 'Internal', 'External', 'Internal'],
            'Status': ['Active', 'Completed', 'On Hold', 'Active', 'Active']
        })

        # Initialize default DataFrame
        project_resource_table = pd.DataFrame({
            'Project': ['Project A', 'Project B', 'Project C', 'Project D', 'Project E'],
            'Resource': ['NAN', 'NAN', 'NAN', 'NAN', 'NAN'],
            'Role': ['Analyst', 'Developer', 'Tester', 'Developer', 'Analyst'],
            'Est_Time_Weeks': [4, 6, 8, 5, 3]
        })

        # Save the default DataFrames to CSV files
        #Here , it save locally , when we create it
        main_table.to_csv('main_table.csv', index=False)
        employee_list.to_csv('employee_list.csv', index=False)
        project_list.to_csv('project_list.csv', index=False)
        # Save the default DataFrame to a CSV file
        project_resource_table.to_csv('project_resource_table.csv', index=False)
        print("Default CSV files created and saved locally.")

    return main_table, employee_list, project_list,project_resource_table






# Function to save data to CSV
def save_data(main_table, employee_list, project_list,project_resource_table):
    main_table.to_csv('main_table.csv', index=False)
    employee_list.to_csv('employee_list.csv', index=False)
    project_list.to_csv('project_list.csv', index=False)
    project_resource_table.to_csv('project_resource_table.csv', index=False)

####################### Adding the infomation to the
# Helper functions to add data
def add_new_employee(Employee_Name, position, skills, current_status):
    new_employee = {'Employee Name':Employee_Name, 'Position': position, 'Skills': skills, 'CurrentStatus': current_status}
    employee_list.loc[len(employee_list)] = new_employee
    save_data(main_table, employee_list, project_list,project_resource_table) ##saving the Data

def add_new_project(project_name, description, start_date, expected_completion, internal_or_external, status):
    new_project = {
        'Project Name': project_name,
        'Description': description,
        'Start Date': start_date,
        'Expected to Complete(Weeks)': expected_completion,
        'Internal/External': internal_or_external,
        'Status': status
    }
    project_list.loc[len(project_list)] = new_project
    save_data(main_table, employee_list, project_list,project_resource_table) ##saving the Data

def add_employee_work_details(start_date, employee_name, project_name, time_in_hours):
    new_work = {
        'WeekEnd Date': start_date,
        'Employee Name': employee_name,
        'Project Name': project_name,
        'Time(in hours)': time_in_hours
    }
    main_table.loc[len(main_table)] = new_work
    save_data(main_table, employee_list, project_list,project_resource_table) ##saving the Data

def add_project_resource_table(project, resource, role, est_time_weeks):
    new_row = {
        'Project': project,
        'Resource': resource,
        'Role': role,
        'Est_Time_Weeks': est_time_weeks
    }
    project_resource_table.loc[len(project_resource_table)] = new_row
    save_data(main_table, employee_list, project_list,project_resource_table) ##saving the Data

# Function to process and clean the data from the main table
def main_table_data():
    main_table['WeekEnd Date'] = pd.to_datetime(main_table['WeekEnd Date'])
    # Extract year from 'WeekEnd Date'
    main_table['Year'] = main_table['WeekEnd Date'].dt.year
    # Convert year to string (if needed) and remove commas ,bcz of 2,024 to 2024
    main_table['Year'] = main_table['Year'].astype(str).str.replace(",", "")
    main_table['Week Number'] = main_table['WeekEnd Date'].dt.isocalendar().week
    main_table['WeekEnd Date'] = main_table['WeekEnd Date'].dt.date #to remove the time stamp 00:00:00
    return main_table

# Load data (from CSV or default values)
main_table, employee_list, project_list,project_resource_table = load_data()

# Streamlit app structure
st.sidebar.title("Choose your Task here")
option = st.sidebar.selectbox("Choose a section", 
    ["Dashboard", "Add New Employee", "Add New Project", "Employee Weekly Tracker","Add Project Resources", "Utilization Analysis"])

# Dashboard Section
if option == "Dashboard":
    st.title("Employee Tracker Dashboard")
    #Output the Employee List Table
    st.header("Employee List")
    st.dataframe(employee_list, use_container_width=True)
    #Output the Main Table
    st.header(" Main Table")
    main_table = main_table_data()
    st.dataframe(main_table, use_container_width=True)
    #Output the Project List
    st.header("Project List")
    st.dataframe(project_list, use_container_width=True)
    #Output the Resource Table
    st.header("Project Resource Table")
    st.dataframe(project_resource_table, use_container_width=True)

# Add New Employee Section
elif option == "Add New Employee":
    st.title("Add New Employee")
    with st.form(key='add_employee_form'):
        name = st.text_input("Name")
        position = st.text_input("Position")
        skills = st.text_input("Skills")
        current_status = st.selectbox("Current Status", ['Active', 'Inactive'])
        submit_employee = st.form_submit_button("Add Employee")
        if submit_employee:
            if name and position and skills and current_status:
                add_new_employee(name, position, skills, current_status)
                st.success("Employee added successfully!")
            else:
                st.error("Please fill all fields.")

# Add New Project Section
elif option == "Add New Project":
    st.title("Add New Project")
    with st.form(key='add_project_form'):
        project_name  = st.text_input("Project Name")
        description   = st.text_input("Description")
        start_date    = st.date_input("Start Date")
        expected_completion = st.number_input("Expected Completion (Weeks)", min_value=1)
        internal_or_external = st.selectbox("Internal or External", ['Internal', 'External'])
        status = st.selectbox("Status", ['Active', 'Completed', 'On Hold'])
        submit_project = st.form_submit_button("Add Project")
        if submit_project:
            if project_name and description and start_date and expected_completion and internal_or_external and status:
                add_new_project(project_name, description, start_date, expected_completion, internal_or_external, status)
                st.success("Project added successfully!")
            else:
                st.error("Please fill all fields.")

# Employee Weekly Tracker Section
elif option == "Employee Weekly Tracker":
    st.title("Employee Weekly Tracker")
    with st.form(key='add_work_form'):
        start_date      = st.date_input("Start Date")
        employee_name   = st.text_input("Employee Name")
        project_name    = st.text_input("Project Name")
        time_in_hours   = st.number_input("Time Spent (in hours)", min_value=1)
        submit_work     = st.form_submit_button("Add Work Details")
        if submit_work:
            if start_date and employee_name and project_name and time_in_hours:
                add_employee_work_details(start_date, employee_name, project_name, time_in_hours)
                st.success("Work details added successfully!")
            else:
                st.error("Please fill all fields.")

###ADd the project_resource_table
elif option == "Add Project Resources":
    st.title("Add Project Resources")
    with st.form(key='add_project_resources_form'):
        project_name = st.text_input("Enter  the Project Name")
        resource_name = st.text_input("Enter  the Resource Name")
        role_name = st.text_input("Enter  the Role")
        est_Time_in_Weeks = st.text_input(" Enter Estimated Time Weeks  ")
        submit_project_resources = st.form_submit_button("Add Project Resources")
        if submit_project_resources:
            if project_name and resource_name and  role_name and est_Time_in_Weeks:
                add_project_resource_table(project_name,resource_name,role_name,est_Time_in_Weeks)
                st.success("Added the Project Resources successfully!")
            else:
                st.error("Please fill all fields.")    

# Utilization Analysis Section
# Utilization Analysis Section 
elif option == "Utilization Analysis":
    st.title("Utilization Analysis")

    # Sidebar for options
    with st.sidebar:
        st.header("Select Option")

        # Main options select box
        main_option = st.selectbox("Choose an Option", ["Employee Work", "Filter Options","Actual Vs Estimated"])

    # Load main table data
    #From the main tbale we will do all the analysis , okay
    filtered_data = main_table_data()

    # Employee Work Analysis
    if main_option == "Employee Work":
        st.subheader("Employee Work Analysis")

        # Create pivot table
        pivot_table = filtered_data.pivot_table(
            index = 'Employee Name',
            columns = 'Project Name',
            values = 'Time(in hours)',
            aggfunc = 'sum'  # Sum of hours worked by each employee on each project
        ).fillna(0)

        # Display pivot table
        st.dataframe(pivot_table, use_container_width = True)

    # Filter Options
    elif main_option == "Filter Options":
        st.write("### Select Filtering Options")

        # Checkboxes for filter options
        filter_by_date = st.sidebar.checkbox("Filter by Date")
        filter_by_year = st.sidebar.checkbox("Filter by Year")
        filter_by_project = st.sidebar.checkbox("Filter by Project")
        filter_by_week_number = st.sidebar.checkbox("Filter by Week Number")
        filter_by_employee_name = st.sidebar.checkbox("Filter by Employee Name")

        # Apply Date filter
        if filter_by_date:
            date_filter = st.date_input("Select Date", value=datetime.datetime.today())
            filtered_data = filtered_data[filtered_data['WeekEnd Date'] == date_filter]

        # Apply Year filter
        # Apply Year filter
        if filter_by_year:
            years = filtered_data['Year'].unique()  # Get unique years from the data
            years = list(years)  # Convert to a list if needed
            years.sort()  # Sort the years for better usability
            year_filter = st.selectbox("Select Year", options = years)  # Provide list as options
            filtered_data = filtered_data[filtered_data['Year'] == year_filter]


        # Apply Project filter (only if selected)
        if filter_by_project:
            projects = filtered_data['Project Name'].unique()  # Get unique project names
            projects = list(projects)  # Convert to list to insert "All Projects"
            projects.insert(0, "All Projects")  # Insert "All Projects" at the start
            project_filter = st.selectbox("Select Project", projects)  # Select project or "All Projects"

            # If "All Projects" is selected, don't filter by project
            if project_filter != "All Projects":
                filtered_data = filtered_data[filtered_data['Project Name'] == project_filter]

        # Apply Week Number filter
        if filter_by_week_number:
            week_number_filter = st.number_input("Select Week Number", min_value=1, max_value=53)
            filtered_data = filtered_data[filtered_data['Week Number'] == week_number_filter]

        # Apply Employee Name filter (only if selected)
        if filter_by_employee_name:
            employee_names = filtered_data['Employee Name'].unique()  # Get unique employee names
            employee_names = list(employee_names)  # Convert to list to insert "All Employees"
            employee_names.insert(0, "All Employees")  # Insert "All Employees" at the start
            employee_name_filter = st.selectbox("Select Employee", employee_names)  # Select employee or "All Employees"

            # If "All Employees" is selected, don't filter by employee name
            if employee_name_filter != "All Employees": #This condition for other than ALL Employees
                filtered_data = filtered_data[filtered_data['Employee Name'] == employee_name_filter]

        # Display filtered data in a table
        st.dataframe(filtered_data, use_container_width=True)
    ###############
    elif main_option == "Actual Vs Estimated":
        #Check Box
        filter_by_Avg_Employee_work = st.sidebar.checkbox("Employee Avg Work Details")
        filter_by_project_resource = st.sidebar.checkbox("Project Resource Deatils")
        if filter_by_Avg_Employee_work :
            option_1 = st.selectbox("Choose an Option", ["Employee Avg Work Deatils", "Employeee Work Details"])
            if option_1 == "Employeee Work Details":
                st.subheader("Employee  Work Details")   
                #From the main tbale we will do all the analysis , okay
                filtered_data = main_table_data()
                temp_filter  = filtered_data[["Employee Name","Time(in hours)","WeekEnd Date"]]
                st.dataframe(temp_filter) 
            else:
                st.subheader("Employee Avg Work Details")    
                # Group by Employee Name and calculate the average work
                avg_work = filtered_data.groupby("Employee Name")["Time(in hours)"].mean()
                st.dataframe(avg_work)

        ##Print the Project Resource Table
        if filter_by_project_resource:
            st.subheader("Project Resource Table:")
            st.dataframe(project_resource_table)    




