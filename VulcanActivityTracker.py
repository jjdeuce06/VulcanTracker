#=============VULCANACTIVITYTRACKE.PY=======================#
# RUN TRACKING APP
# JOHN GEREGA
#==================================================#

#=========LIBRARIES==================#
import tkinter as tk
from tkinter import *
from tkinter import messagebox, filedialog, scrolledtext
from tkinter import simpledialog
from tkcalendar import Calendar, DateEntry
from Activity import Activity
import os

import mysql.connector

#==========END LIBRARIES=============#

class Jog:
        def __init__(self):
            self.login = tk.Tk()
            self.login.title("Vulcan Activity Tracker")
            self.login.geometry("1000x600+200+100")
            self.login.configure(bg='#f0f2f5')
            self.login.resizable(False, False)
            self.img = None

            # Define modern colors
            self.PRIMARY_COLOR = '#2c3e50'
            self.SECONDARY_COLOR = '#3498db'
            self.ACCENT_COLOR = '#e74c3c'
            self.BG_COLOR = '#f0f2f5'
            self.TEXT_COLOR = '#2c3e50'

            self.miles_ran_num = 0
            self.activites = 0
            self.avghr = 0
            self.calsburned = 0
            self.elev = 0
            self.zone = 0
            self.pace = 0
            self.act_date = None
            self.user_data = []
            self.current_username = None
            
            self.conn = mysql.connector.connect(
                host = "",  #Enter your own data
                user = "",
                password = "",
                database = "vulcanTracker"
            )
            self.cursor = self.conn.cursor()

            # Create main container
            self.main_container = Frame(self.login, bg=self.BG_COLOR)
            self.main_container.pack(fill='both', expand=True, padx=20, pady=20)

            # Left side image container
            self.image_container = Frame(self.main_container, bg=self.BG_COLOR)
            self.image_container.pack(side='left', fill='both', expand=True, padx=(0, 20))

            # Load Image with better styling
            self.img = PhotoImage(file='imgs/cu.png')
            Label(self.image_container, image=self.img, bg=self.BG_COLOR).pack(pady=50)
            
            # Title with better styling
            self.titlelabel = Label(self.image_container, text='Activity Tracker', 
                                  fg=self.PRIMARY_COLOR, bg=self.BG_COLOR,
                                  font=('Helvetica', 28, 'bold'))
            self.titlelabel.pack(pady=(0, 20))

            # Right side login container
            self.login_frame = Frame(self.main_container, bg='white', 
                                   highlightbackground=self.PRIMARY_COLOR,
                                   highlightthickness=2)
            self.login_frame.pack(side='right', fill='both', expand=True, padx=(0, 0))
            self.login_frame.pack_propagate(False)

            # Heading with better styling
            self.heading = Label(self.login_frame, text='Sign In', 
                               fg=self.PRIMARY_COLOR, bg='white',
                               font=('Helvetica', 24, 'bold'))
            self.heading.pack(pady=(40, 30))

            # Username input with better styling
            self.user = Entry(self.login_frame, width=25, fg=self.TEXT_COLOR, 
                            border=0, bg='white',
                            font=('Helvetica', 12))
            self.user.pack(pady=(0, 10))
            self.user.insert(0, 'Username')
            self.user.bind('<FocusIn>', self.on_enter_user)
            self.user.bind('<FocusOut>', self.on_leave_user)
            Frame(self.login_frame, width=300, height=2, bg=self.PRIMARY_COLOR).pack(pady=(0, 20))

            # Password input with better styling
            self.code = Entry(self.login_frame, width=25, fg=self.TEXT_COLOR, 
                            border=0, bg='white',
                            font=('Helvetica', 12), show="*")
            self.code.pack(pady=(0, 10))
            self.code.insert(0, 'Password')
            self.code.bind('<FocusIn>', self.on_enter_code)
            self.code.bind('<FocusOut>', self.on_leave_code)
            Frame(self.login_frame, width=300, height=2, bg=self.PRIMARY_COLOR).pack(pady=(0, 20))

            # Sign In Button with better styling
            Button(self.login_frame, width=20, pady=8, text='Sign In', 
                  bg=self.SECONDARY_COLOR, fg='white', border=0,
                  font=('Helvetica', 11, 'bold'),
                  command=self.signin).pack(pady=(20, 30))

            # Sign Up section with better styling
            signup_frame = Frame(self.login_frame, bg='white')
            signup_frame.pack()
            
            Label(signup_frame, text="Don't have an account?", 
                 fg=self.TEXT_COLOR, bg='white',
                 font=('Helvetica', 10)).pack(side='left', padx=(0, 10))

            Button(signup_frame, text='Sign Up', 
                  bg=self.ACCENT_COLOR, fg='white',
                  border=0, font=('Helvetica', 10, 'bold'),
                  command=self.signup).pack(side='right')

            # Start the main event loop
            self.login.mainloop()  # This keeps the window open and responsive
        #Sign in method to ensure username and password matches

        def signin(self):
            username = self.user.get()
            password = self.code.get()

            if username == 'user' and password == '1234':
                self.open_userportal()
            #elif username != 'user' and password != '1234':
                #messagebox.showerror("Invalid", "invalid username and password")
            #elif password != '1234':
                #messagebox.showerror("Invalid", "invalid password")
            #elif username != 'user':
                #messagebox.showerror("Invalid", "invalid username")
            else:
                user = False
                passw = False
                #database = Database()
                #datbase.connect_database()
                select_query = "SELECT * FROM userProfile"
                self.cursor.execute(select_query)
                results = self.cursor.fetchall()
                #print("User profile:")
                for row in results:
                    #print(row)
                    if (username == row[0]):
                        user = True
                    if (password == row[1]):
                        passw = True
                
                if (user == True and passw == True):
                    self.current_username = username       #assign the username to the global variable for data tracking
                    self.open_userportal()

        
        def signup(self):
            self.signup_window = Toplevel(self.login)
            self.signup_window.title("Create new account")
            self.signup_window.geometry("600x400")
            self.signup_window.configure(bg="#fff")
            self.signup_window.resizable(False, False)
            self.menu_frame = tk.Frame(self.signup_window, bg = 'white')

            #Heading
            Label(self.signup_window, text = "Create new account", fg="red", bg="white", font=('Microsoft YaHei UI Light', 23, 'bold')).place(x=180, y=20)

            Label(self.signup_window, text = "First name", fg="black", bg="white", font=('Microsoft YaHei UI Light', 11)).place(x=50, y=110)
            self.fname_entry = Entry(self.signup_window, width=15, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
            self.fname_entry.place(x=50, y=140)
            Frame(self.signup_window, width=150, height=2, bg='black').place(x=50, y=160)

            self.lname = Label(self.signup_window, text = "Last name", fg="black", bg="white", font=('Microsoft YaHei UI Light', 11)).place(x=50, y=170)
            self.lname_entry = Entry(self.signup_window, width=15, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
            self.lname_entry.place(x=50, y=200)
            Frame(self.signup_window, width=150, height=2, bg='black').place(x=50, y=220)

            # Age Entry
            Label(self.signup_window, text="Age", fg="black", bg="white", font=('Microsoft YaHei UI Light', 11)).place(x=50, y=230)
            self.age_entry = Entry(self.signup_window, width=15, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
            self.age_entry.place(x=50, y=270)
            Frame(self.signup_window, width=150, height=2, bg='black').place(x=50, y=290)

            # Username Entry
            Label(self.signup_window, text="Username", fg="black", bg="white", border = 2, font=('Microsoft YaHei UI Light', 11)).place(x=250, y=110)
            self.signup_username_entry = Entry(self.signup_window, width=15, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
            self.signup_username_entry.place(x=250, y=140)
            Frame(self.signup_window, width=150, height=2, bg='black').place(x=250, y=160)

            # Password Entry
            Label(self.signup_window, text="Password", fg="black", bg="white", font=('Microsoft YaHei UI Light', 11)).place(x=250, y=170)
            self.signup_password_entry = Entry(self.signup_window, width=15, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11), show="*")
            self.signup_password_entry.place(x=250, y=200)
            Frame(self.signup_window, width=150, height=2, bg='black').place(x=250, y=220)

            # Confirm Button
            Button(self.signup_window, width=20, pady=7, text='Confirm', bg='red', fg='white', border=0, command=self.create_account).place(x=200, y=350)

        def create_account(self):
            fname = self.fname_entry.get()
            lname = self.lname_entry.get()
            new_age = self.age_entry.get()
            new_user = self.signup_username_entry.get()
            new_password = self.signup_password_entry.get()

            try:
                fname = str(fname)
                lname = str(lname)
                new_age = int(new_age)
                new_user = str(new_user)
                new_password = str(new_password)
                insert_query = "INSERT INTO signup (fname, lname, username, password, age) VALUES (%s, %s, %s, %s, %s)"
                values = (fname, lname, new_user, new_password, new_age)
                self.cursor.execute(insert_query, values)
                self.conn.commit()
                print("Data inserted successfully!")
                self.open_userportal()
            except ValueError:
                messagebox.showerror("Invalid", "invalid entries")

            
            
        #---------USER-----------------#
        def on_enter_user(self, e):
            self.user.delete(0, 'end')

        def on_leave_user(self, e):
            name = self.user.get()
            if name == '':
                self.user.insert(0, 'Username')
        #---------END USER--------------#

        #---------PASSWORD---------------------#
        def on_enter_code(self, e):
            self.code.delete(0, 'end')

        def on_leave_code(self, e):
            name = self.code.get()
            if name == '':
                self.code.insert(0, 'Password')
        #---------END PASSWORD-------------------#


        #method to open the main window
        def open_userportal(self):
            #Setting up the initial window
            self.root = Toplevel(self.login)
            self.root.geometry("925x500+300+200")
            self.root.title("Vulcan Activity Tracker")
            self.root.resizable(False, False)
            self.root.configure(bg=self.BG_COLOR)
            
            # Menu frame with modern styling
            self.menu_frame = tk.Frame(self.root, bg=self.PRIMARY_COLOR)
            
            # Modern styled menu buttons
            button_style = {'font': ('Helvetica', 12, 'bold'), 
                          'fg': 'white', 
                          'bg': self.PRIMARY_COLOR, 
                          'bd': 0,
                          'padx': 20,
                          'pady': 10,
                          'activebackground': self.SECONDARY_COLOR,
                          'activeforeground': 'white'}
            
            #Home button with modern styling
            self.connect_btn = tk.Button(self.menu_frame, 
                                      text='Home',
                                      **button_style,
                                      command=lambda: self.indicator(self.connect_marker, self.total_page))
            self.connect_btn.place(x=0, y=50)

            self.connect_marker = tk.Label(self.menu_frame, bg=self.SECONDARY_COLOR)
            self.connect_marker.place(x=0, y=50, width=4, height=40)

            #View Specific button with modern styling
            self.rcv_btn = tk.Button(self.menu_frame, 
                                  text='View Specific',
                                  **button_style,
                                  command=lambda: self.indicator(self.rcv_marker, self.viewActivity_page))
            self.rcv_btn.place(x=0, y=100)

            self.rcv_marker = tk.Label(self.menu_frame, bg=self.SECONDARY_COLOR)
            self.rcv_marker.place(x=0, y=100, width=4, height=40)

            #Add Data button with modern styling
            self.view_btn = tk.Button(self.menu_frame, 
                                   text='Add Data',
                                   **button_style,
                                   command=lambda: self.indicator(self.view_marker, self.addActivity_page))
            self.view_btn.place(x=0, y=150)

            self.view_marker = tk.Label(self.menu_frame, bg=self.SECONDARY_COLOR)
            self.view_marker.place(x=0, y=150, width=4, height=40)

            #Sizing and packing the menu frame
            self.menu_frame.pack(side=tk.LEFT, fill='y')
            self.menu_frame.pack_propagate(False)
            self.menu_frame.configure(width=150, height=600)

            #Modern styled main content frame
            self.interactive_frame = tk.Frame(self.root, 
                                           bg=self.BG_COLOR,
                                           highlightbackground=self.PRIMARY_COLOR,
                                           highlightthickness=2)
            self.interactive_frame.pack(side=tk.LEFT, fill='both', expand=True)
            self.interactive_frame.pack_propagate(False)
            self.interactive_frame.configure(height=600, width=900)

            #establish starting page
            self.indicator(self.connect_marker, self.total_page)

        def total_page(self):
            total_frame = tk.Frame(self.interactive_frame)
            total_frame.pack(fill='both', expand=True)
            total_frame.config(bg=self.BG_COLOR)

            # Main heading with modern styling
            heading = Label(total_frame, 
                          text='Your Stats',
                          fg=self.PRIMARY_COLOR,
                          bg=self.BG_COLOR,
                          font=('Helvetica', 28, 'bold'))
            heading.place(x=300, y=20)

            # Stats container frame
            stats_frame = Frame(total_frame, 
                              bg='white',
                              highlightbackground=self.PRIMARY_COLOR,
                              highlightthickness=1)
            stats_frame.place(x=20, y=80, width=800, height=350)

            # Modern styled stat labels
            stat_style = {'fg': self.PRIMARY_COLOR,
                        'bg': 'white',
                        'font': ('Helvetica', 12, 'bold')}
            
            value_style = {'fg': self.SECONDARY_COLOR,
                         'bg': 'white',
                         'font': ('Helvetica', 14, 'bold')}

            # Activities
            self.activity_header = Label(stats_frame, text="Total Activities", **stat_style)
            self.activity_header.place(x=30, y=20)
            self.activites_disp = Label(stats_frame, text=self.activites, **value_style)
            self.activites_disp.place(x=30, y=50)

            # Miles
            self.miles_ran_header = Label(stats_frame, text="Total Miles", **stat_style)
            self.miles_ran_header.place(x=30, y=100)
            self.miles_ran = Label(stats_frame, text=self.miles_ran_num, **value_style)
            self.miles_ran.place(x=30, y=130)

            # Calories
            self.calsburnedheader = Label(stats_frame, text="Total Calories Burned", **stat_style)
            self.calsburnedheader.place(x=30, y=180)
            self.totalcals = Label(stats_frame, text=self.calsburned, **value_style)
            self.totalcals.place(x=30, y=210)

            # Elevation
            self.elev_header = Label(stats_frame, text="Total Elevation Gained", **stat_style)
            self.elev_header.place(x=30, y=260)
            self.total_elev = Label(stats_frame, text=self.elev, **value_style)
            self.total_elev.place(x=30, y=290)

            self.updatetext()

        def hide_indicators(self):
            self.connect_marker.config(bg=self.BG_COLOR)
            self.view_marker.config(bg=self.BG_COLOR)
            self.rcv_marker.config(bg=self.BG_COLOR)

        def indicator(self, lb, page):
            self.hide_indicators()
            lb.config(bg=self.SECONDARY_COLOR)
            self.delete_page()
            page()

        #method for the receive file page (page that shows ep when receive file button is clicked)
        def viewActivity_page(self):
            viewActivity_frame = tk.Frame(self.interactive_frame)
            viewActivity_frame.pack(fill='both', expand=True)
            viewActivity_frame.config(bg=self.BG_COLOR)

            # Modern heading
            heading = Label(viewActivity_frame, 
                          text='View Activity',
                          fg=self.PRIMARY_COLOR,
                          bg=self.BG_COLOR,
                          font=('Helvetica', 28, 'bold'))
            heading.pack(pady=20)

            # Search container
            search_frame = Frame(viewActivity_frame,
                               bg='white',
                               highlightbackground=self.PRIMARY_COLOR,
                               highlightthickness=1)
            search_frame.pack(padx=20, pady=10, fill='x')

            # Search prompt
            send_prompt = Label(search_frame,
                              text="Enter activity name to view details",
                              fg=self.PRIMARY_COLOR,
                              bg='white',
                              font=('Helvetica', 12))
            send_prompt.pack(pady=10)

            # Modern search entry
            self.name_enter = Entry(search_frame,
                                  width=30,
                                  fg=self.TEXT_COLOR,
                                  bg='white',
                                  font=('Helvetica', 12),
                                  bd=2,
                                  relief='solid')
            self.name_enter.insert(0, "Activity Name")
            self.name_enter.bind('<FocusIn>', self.on_enter_name)
            self.name_enter.bind('<FocusOut>', self.on_leave_name)
            self.name_enter.pack(pady=10)

            # Modern find button
            self.find_button = Button(search_frame,
                                    text='Find Activity',
                                    bg=self.SECONDARY_COLOR,
                                    fg='white',
                                    font=('Helvetica', 11, 'bold'),
                                    bd=0,
                                    padx=20,
                                    pady=8,
                                    command=self.getactivity)
            self.find_button.pack(pady=15)

            # Results container
            results_frame = Frame(viewActivity_frame,
                                bg='white',
                                highlightbackground=self.PRIMARY_COLOR,
                                highlightthickness=1)
            results_frame.pack(padx=20, pady=20, fill='both', expand=True)

            # Modern label styles
            header_style = {'fg': self.PRIMARY_COLOR,
                          'bg': 'white',
                          'font': ('Helvetica', 12, 'bold')}
            
            value_style = {'fg': self.SECONDARY_COLOR,
                         'bg': 'white',
                         'font': ('Helvetica', 14)}

            # Left column
            left_frame = Frame(results_frame, bg='white')
            left_frame.pack(side='left', padx=30, pady=20, fill='both', expand=True)

            self.specific_name_header = Label(left_frame, text="Activity Name", **header_style)
            self.specific_name_header.pack(anchor='w', pady=(0, 5))
            self.specific_name = Label(left_frame, text="", **value_style)
            self.specific_name.pack(anchor='w', pady=(0, 20))

            self.specific_cals_header = Label(left_frame, text="Calories Burned", **header_style)
            self.specific_cals_header.pack(anchor='w', pady=(0, 5))
            self.specific_cals = Label(left_frame, text="", **value_style)
            self.specific_cals.pack(anchor='w', pady=(0, 20))

            self.specific_elev_header = Label(left_frame, text="Elevation", **header_style)
            self.specific_elev_header.pack(anchor='w', pady=(0, 5))
            self.specific_elev = Label(left_frame, text="", **value_style)
            self.specific_elev.pack(anchor='w')

            # Right column
            right_frame = Frame(results_frame, bg='white')
            right_frame.pack(side='left', padx=30, pady=20, fill='both', expand=True)

            self.specific_zone_header = Label(right_frame, text="Zone", **header_style)
            self.specific_zone_header.pack(anchor='w', pady=(0, 5))
            self.specific_zone = Label(right_frame, text="", **value_style)
            self.specific_zone.pack(anchor='w', pady=(0, 20))

            self.specific_pace_header = Label(right_frame, text="Pace", **header_style)
            self.specific_pace_header.pack(anchor='w', pady=(0, 5))
            self.specific_pace = Label(right_frame, text="", **value_style)
            self.specific_pace.pack(anchor='w', pady=(0, 20))

            self.specific_hr_header = Label(right_frame, text="Heart Rate", **header_style)
            self.specific_hr_header.pack(anchor='w', pady=(0, 5))
            self.specific_hr = Label(right_frame, text="", **value_style)
            self.specific_hr.pack(anchor='w')

            # Date at the bottom
            date_frame = Frame(results_frame, bg='white')
            date_frame.pack(side='bottom', fill='x', padx=30, pady=20)

            self.date_header = Label(date_frame, text="Date Completed", **header_style)
            self.date_header.pack(side='left', padx=(0, 10))
            self.date_display = Label(date_frame, text="", **value_style)
            self.date_display.pack(side='left')

        def on_enter_name(self, e):
            self.name_enter.delete(0, 'end')
        def on_leave_name(self, e):
                if self.name_enter.get() == "":
                    self.name_enter.delete(0, 'end')  # Clear the entry field
                    self.name_enter.insert(0, 'Add data here')
        def getactivity(self):
                self.activity_name = self.name_enter.get()
                for i in range(0, len(self.user_data), 1):
                    if self.user_data[i].get_name() == self.activity_name:
                        self.specific_name.config(text = str(self.user_data[i].get_name()))
                        self.specific_cals.config(text = str(self.user_data[i].get_cals()))
                        self.specific_elev.config(text = str(self.user_data[i].get_elevation()))
                        self.specific_zone.config(text = str(self.user_data[i].get_zone()))
                        self.specific_pace.config(text = str(self.user_data[i].get_pace()))
                        self.specific_hr.config(text = str(self.user_data[i].get_hr()))
                        self.date_display.config(text = str(self.user_data[i].get_date()))
                        if (self.user_data[i].get_race() == True):
                            self.race_header.config(text = "RACE DAY!")
                        break
                    else:
                        print("no value found for this specific i value")

        #method for view file page (page that shows up when view button is clicked)
        def addActivity_page(self):
            addActivity_frame = tk.Frame(self.interactive_frame)
            addActivity_frame.pack(fill='both', expand=True)
            addActivity_frame.config(bg=self.BG_COLOR)

            # Modern heading
            heading = Label(addActivity_frame,
                          text='Add Activity',
                          fg=self.PRIMARY_COLOR,
                          bg=self.BG_COLOR,
                          font=('Helvetica', 28, 'bold'))
            heading.pack(pady=20)

            # Main container with two columns
            main_container = Frame(addActivity_frame, bg=self.BG_COLOR)
            main_container.pack(fill='both', expand=True, padx=20, pady=10)

            # Left side for inputs
            input_frame = Frame(main_container,
                              bg='white',
                              highlightbackground=self.PRIMARY_COLOR,
                              highlightthickness=1)
            input_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))

            # Right side for calendar
            calendar_frame = Frame(main_container,
                                 bg='white',
                                 highlightbackground=self.PRIMARY_COLOR,
                                 highlightthickness=1)
            calendar_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))

            # Calendar widget for activity date
            Label(calendar_frame, text="Select Date", fg=self.PRIMARY_COLOR, bg='white', font=('Helvetica', 12, 'bold')).pack(pady=(20, 5))
            self.activity_date = Calendar(calendar_frame, selectmode="day", date_pattern='yyyy-mm-dd')
            self.activity_date.pack(pady=10)

            # Modern input styles
            entry_style = {'width': 25,
                         'fg': self.TEXT_COLOR,
                         'bg': 'white',
                         'font': ('Helvetica', 12),
                         'bd': 2,
                         'relief': 'solid'}

            label_style = {'fg': self.PRIMARY_COLOR,
                         'bg': 'white',
                         'font': ('Helvetica', 12, 'bold')}

            # Input fields container
            fields_container = Frame(input_frame, bg='white')
            fields_container.pack(padx=30, pady=20, fill='both', expand=True)

            # Miles input
            Label(fields_container, text="Miles Ran", **label_style).pack(anchor='w', pady=(0, 5))
            self.add_miles = Entry(fields_container, **entry_style)
            self.add_miles.insert(0, 'Enter miles')
            self.add_miles.bind('<FocusIn>', self.on_enter_miles)
            self.add_miles.bind('<FocusOut>', self.on_exit_miles)
            self.add_miles.pack(anchor='w', pady=(0, 15))

            # Calories input
            Label(fields_container, text="Calories Burned", **label_style).pack(anchor='w', pady=(0, 5))
            self.add_cals = Entry(fields_container, **entry_style)
            self.add_cals.insert(0, 'Enter calories')
            self.add_cals.bind('<FocusIn>', self.on_enter_cals)
            self.add_cals.bind('<FocusOut>', self.on_exit_cals)
            self.add_cals.pack(anchor='w', pady=(0, 15))

            # Elevation input
            Label(fields_container, text="Elevation Gained", **label_style).pack(anchor='w', pady=(0, 5))
            self.elev_enter = Entry(fields_container, **entry_style)
            self.elev_enter.insert(0, 'Enter elevation')
            self.elev_enter.bind('<FocusIn>', self.on_enter_elev)
            self.elev_enter.bind('<FocusOut>', self.on_exit_elev)
            self.elev_enter.pack(anchor='w', pady=(0, 15))

            # Heart Rate input
            Label(fields_container, text="Average Heart Rate", **label_style).pack(anchor='w', pady=(0, 5))
            self.hr_entry = Entry(fields_container, **entry_style)
            self.hr_entry.insert(0, 'Enter heart rate')
            self.hr_entry.bind('<FocusIn>', self.hr_on_entry)
            self.hr_entry.bind('<FocusOut>', self.hr_on_exit)
            self.hr_entry.pack(anchor='w', pady=(0, 15))

            # Pace input
            Label(fields_container, text="Average Pace", **label_style).pack(anchor='w', pady=(0, 5))
            self.pace_entry = Entry(fields_container, **entry_style)
            self.pace_entry.insert(0, 'Enter pace')
            self.pace_entry.bind('<FocusIn>', self.pace_enter)
            self.pace_entry.bind('<FocusOut>', self.pace_exit)
            self.pace_entry.pack(anchor='w', pady=(0, 15))

            # Activity Name input
            Label(fields_container, text="Activity Name", **label_style).pack(anchor='w', pady=(0, 5))
            self.name_entry = Entry(fields_container, **entry_style)
            self.name_entry.insert(0, 'Enter activity name')
            self.name_entry.bind('<FocusIn>', self.name_enter)
            self.name_entry.bind('<FocusOut>', self.name_exit)
            self.name_entry.pack(anchor='w', pady=(0, 15))

            # Race checkbox
            self.raceCheck = Checkbutton(fields_container,
                                    text="Race Day",
                                    fg=self.PRIMARY_COLOR,
                                    bg='white',
                                    font=('Helvetica', 12))
            self.raceCheck.pack(anchor='w', pady=15)

            # Submit button
            self.update_button = Button(calendar_frame,
                text='Submit',
                bg=self.SECONDARY_COLOR,
                fg='white',
                border=0,
                font=('Helvetica', 12, 'bold'),
                command=self.updatedata)
            self.update_button.place(x=100, y=350, width=150, height=40)

            # Add hover effect
            self.update_button.bind('<Enter>', lambda e: self.update_button.config(bg=self.ACCENT_COLOR))
            self.update_button.bind('<Leave>', lambda e: self.update_button.config(bg=self.SECONDARY_COLOR))

        def on_enter_miles(self, e):
            self.add_miles.delete(0, 'end')
        def on_exit_miles(self, e):
                if self.add_miles.get() == "":
                    self.add_miles.delete(0, 'end')  # Clear the entry field
                    self.add_miles.insert(0, 'Add miles here')
        def on_enter_cals(self, e):
                self.add_cals.delete(0, 'end')
        def on_exit_cals(self, e):
            if self.add_cals.get() == "":
                    self.add_cals.delete(0, 'end')  # Clear the entry field
                    self.add_cals.insert(0, 'Add calories here')
        def on_enter_elev(self, e):
                self.elev_enter.delete(0, 'end')
        def on_exit_elev(self, e):
                if self.elev_enter.get() == "":
                    self.elev_enter.delete(0, 'end')
                    self.add_miles.insert(0, 'Add elevation here')
        def hr_on_entry(self, e):
            self.hr_entry.delete(0, 'end')
        def hr_on_exit(self, e):
            if self.hr_entry.get() == "":
                self.hr_entry.delete(0, 'end')
                self.hr_entry.insert(0, "Add heart rate here")
        def pace_enter(self, e):
            self.pace_entry.delete(0, 'end')
        def pace_exit(self, e):
            if self.pace_entry.get() == "":
                self.pace_entry.delete(0, 'end')
                self.pace_entry.insert(0, 'Add mile pace')
        def name_enter(self, e):
            self.name_entry.delete(0, 'end')
        def name_exit(self, e):
            if self.name_entry.get() == "":
                self.name_entry.delete(0, 'end')
                self.name_entry.insert(0, 'Add activity name')
        def updatedata(self):
            self.newmiles = self.add_miles.get()
            self.newcals = self.add_cals.get()
            self.new_elev = self.elev_enter.get()
            self.activites = int(self.activites) + 1
            self.new_name = self.name_entry.get()
            self.new_pace = self.pace_entry.get()
            self.new_hr = self.hr_entry.get()
            self.new_date = self.activity_date.get_date()
            #self.check_race = self.raceCheck.getboolean()

            #Add activity to the array
            data_added = False
            while(data_added == False):
                workout = Activity()
                workout.set_pace(int(self.new_pace))
                workout.set_miles(float(self.newmiles))
                workout.set_elevation(int(self.new_elev))
                workout.set_hr(int(self.new_hr))
                workout.set_zone(20)
                workout.set_cals(int(self.newcals))
                workout.set_name(self.new_name)
                workout.set_date(self.new_date)
                #workout.set_race(self.check_race)
                if len(self.user_data) == 0:
                    self.user_data.insert(0, workout)
                    data_added = True
                else:
                    self.user_data.append(workout)
                    data_added = True
            
            self.new_name = ""
            #add to total values
            select_query = "SELECT miles, activites FROM userProfile WHERE username = %s"
            self.cursor.execute(select_query, (self.current_username,))
            result = self.cursor.fetchone()  # Fetch one row (tuple)

            current_miles = float(result[0])
            current_activities = int(result[1])
            try:
                # Convert user input to integer and add to miles_ran_num
                    if self.newmiles != "":
                        miles_to_add = float(self.newmiles)  # Convert to float
                        self.miles_ran_num += miles_to_add  # Update the total miles
                        current_miles += miles_to_add
                    if self.newcals != "":
                        cals_to_add = int(self.newcals)
                        self.calsburned += cals_to_add
                    if self.new_elev != "":
                        elev_to_add = int(self.new_elev)
                        self.elev += elev_to_add
                    current_activities += 1
                    # Update the database with new values
                    update_query = "UPDATE userProfile SET miles = %s, activites = %s WHERE username = %s"
                    self.cursor.execute(update_query, (current_miles, current_activities, self.current_username))
                    self.conn.commit()
                    print("database updated")
            except ValueError:
                # If conversion to int fails, handle it here
                messagebox.showerror("Invalid Input", "Please enter a valid number for miles.")
        def updatetext(self):
                select_query = "SELECT * FROM userProfile"
                self.cursor.execute(select_query)
                results = self.cursor.fetchall()
                for row in results:
                    print("Database user: ", row[0])
                    print("User logged in: ", self.current_username)
                    if str(row[0]) == self.current_username:
                        self.activites_disp.config(text = str(row[4]))
                        self.miles_ran.config(text = str(row[3]))
                self.totalcals.config(text = str(self.calsburned))
                self.total_elev.config(text = str(self.elev))
        def delete_page(self):
            for frame in self.interactive_frame.winfo_children():
                frame.destroy()


    #-------------------------END CLIENT CLASS--------------------------------------------#


    #===========================MAIN======================================#
if __name__ == "__main__":
    jog = Jog()
    #=====================================================================#