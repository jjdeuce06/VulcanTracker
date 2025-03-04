#=============JOG-A-THON.PY=======================#
# RUN TRACKING APP
# JOHN GEREGA
#==================================================#

#=========LIBRARIES==================#
import tkinter as tk
from tkinter import *
from tkinter import messagebox, filedialog, scrolledtext
from tkinter import simpledialog
from tkcalendar import *
from Activity import Activity
import os

import mysql.connector

#==========END LIBRARIES=============#

class Jog:
        def __init__(self):
            self.login = tk.Tk()
            self.login.title("Vulcan Activity Tracker")
            self.login.geometry("925x500+300+200")
            self.login.configure(bg = "#fff")
            self.login.resizable(False, False)
            self.img = None

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

            # Load Image
            self.img = PhotoImage(file = 'imgs\cu.png')
            Label(self.login, image=self.img, bg='white').place(x=50, y=50)
            #Title label
            self.titlelabel = Label(self.login, text = 'Activity Tracker', fg = 'red', bg = 'white', font=('Microsoft YaHei UI Light', 23, 'bold'))
            self.titlelabel.place(x = 160, y = 400)

            #Sign Up Box
            self.login_frame = Frame(self.login, width = 350, height = 350, bg = "white")
            self.login_frame.place(x=480, y=70)

            # Heading
            self.heading = Label(self.login_frame, text='Sign In', fg='red', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
            self.heading.place(x=100, y=5)

            #User Data entry
            self.user = Entry(self.login_frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
            self.user.place(x=30, y=80)
            self.user.insert(0, 'Username')
            self.user.bind('<FocusIn>', self.on_enter_user)
            self.user.bind('<FocusOut>', self.on_leave_user)
            Frame(self.login_frame, width=295, height=2, bg='black').place(x=25, y=107)


            self.code = Entry(self.login_frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11), show="*")
            self.code.place(x=30, y=150)
            self.code.insert(0, 'Password')
            self.code.bind('<FocusIn>', self.on_enter_code)
            self.code.bind('<FocusOut>', self.on_leave_code)
            Frame(self.login_frame, width=295, height=2, bg='black').place(x=25, y=177)

            # Sign In Button
            Button(self.login_frame, width=39, pady=7, text='Sign In', bg='red', fg='white', border=0, command=self.signin).place(x=35, y=204)
            label = Label(self.login_frame, text="Don't have an account?", fg='black', bg='white', font=('Microsoft YaHei UI Light', 9))
            label.place(x=75, y=270)

            # Sign Up Button
            Button(self.login_frame, width=6, text='Sign Up', border=0, bg='red', cursor='hand2', fg='white', command=self.signup).place(x=215, y=270)

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
            self.menu_frame = tk.Frame(self.root, bg = 'white')
            #Home button and connect button indicator set up (still need to change names)
            self.connect_btn = tk.Button(self.menu_frame, text = 'Home', font = ('Bold', 12), fg = 'black', bd = 0,
                                        command=lambda: self.indicator(self.connect_marker, self.total_page))
            self.connect_btn.place(x = 12, y = 50)

            self.connect_marker = tk.Label(self.menu_frame, text = '', bg = 'white')
            self.connect_marker.place(x = 5, y = 50, width = 5, height = 30)

            #Add Data button and view button indicator set up
            self.view_btn = tk.Button(self.menu_frame, text = 'Add data', font = ('Bold', 12), fg = 'black', bd = 0,
                command=lambda: self.indicator(self.view_marker, self.addActivity_page))
            self.view_btn.place(x = 12, y = 150)

            self.view_marker = tk.Label(self.menu_frame, text='', bg = 'white')
            self.view_marker.place(x = 5, y = 150, width = 5, height = 30)

            #Specific activity button and receive button indicator set up
            self.rcv_btn = tk.Button(self.menu_frame, text = 'View Specific', font = ('Bold', 12), fg = 'black', bd = 0,
                                    command=lambda: self.indicator(self.rcv_marker, self.viewActivity_page))
            self.rcv_btn.place(x = 10, y = 100)

            self.rcv_marker = tk.Label(self.menu_frame, text='', bg = 'black')
            self.rcv_marker.place(x = 3, y = 100, width = 5, height = 30)

            #Sizing and packing the menu frame
            self.menu_frame.pack(side = tk.LEFT)
            self.menu_frame.propagate(False)
            self.menu_frame.configure(width = 100, height = 600)

            #Initialization, sizing, and packing of the interactive frame (where the user will enter information)
            self.interactive_frame = tk.Frame(self.root, highlightbackground='red', highlightthickness=3)
            self.interactive_frame.pack(side=tk.LEFT)
            self.interactive_frame.pack_propagate(False)
            self.interactive_frame.configure(height = 600, width = 900)

            #establish starting page
            self.indicator(self.connect_marker, self.total_page)

        #method for the connect page (page that shows up when connect button is clicked) and methods
        def total_page(self):
            total_frame = tk.Frame(self.interactive_frame)

            # Pack the new frame into the interactive_frame
            total_frame.pack(fill='both', expand=True)
            total_frame.config(bg = "white")

            # Total statistics Box - this where total stats for a user will be placed
            heading = Label(total_frame, text='Your Stats', fg='red', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
            heading.place(x = 300, y = 20)

            self.activity_header = Label(total_frame, text = "Total activities", fg='red', bg='white', font=('Microsoft YaHei UI Light', 12, 'bold'))
            self.activity_header.place(x=20, y=80)

            self.activites_disp = Label(total_frame, text = self.activites, fg = "red", bg='white', font=('Microsoft YaHei UI Light', 12, 'bold'))
            self.activites_disp.place(x = 60, y = 105)

            self.miles_ran_header = Label(total_frame, text = "Total miles", fg='red', bg='white', font=('Microsoft YaHei UI Light', 12, 'bold'))
            self.miles_ran_header.place(x=20, y=140)

            self.miles_ran = Label(total_frame, text = self.miles_ran_num, fg = "red", bg='white', font=('Microsoft YaHei UI Light', 12, 'bold'))
            self.miles_ran.place(x = 60, y = 165)

            self.calsburnedheader = Label(total_frame, text = "Total calories burned", fg='red', bg='white', font=('Microsoft YaHei UI Light', 12, 'bold'))
            self.calsburnedheader.place(x = 20, y = 210)

            self.totalcals = Label(total_frame, text = self.calsburned, fg = "red", bg='white', font=('Microsoft YaHei UI Light', 12, 'bold'))
            self.totalcals.place(x = 60, y = 235)

            self.elev_header = Label(total_frame, text = "Total elevation gained", fg='red', bg='white', font=('Microsoft YaHei UI Light', 12, 'bold'))
            self.elev_header.place(x=20, y = 280)
            
            self.total_elev = Label(total_frame, text = self.elev, fg = "red", bg='white', font=('Microsoft YaHei UI Light', 12, 'bold'))
            self.total_elev.place(x = 60, y = 305)

            self.updatetext()
            


        #Connection page/methods end
        
        #method for the receive file page (page that shows ep when receive file button is clicked)
        def viewActivity_page(self):
            viewActivity_frame = tk.Frame(self.interactive_frame)
            # Pack the new frame into the interactive_frame
            viewActivity_frame.pack(fill='both', expand=True)
            viewActivity_frame.config(bg = 'white')
            # Server Box
            heading = Label(viewActivity_frame, text='View Activity', fg='red', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
            heading.pack(pady = 10)

            #Enter file prompt
            send_prompt = Label(viewActivity_frame, text = "Please enter the name of the activity you want to view", font=('Microsoft YaHei UI Light', 18, 'bold'))
            send_prompt.pack(pady = 10)

            
            self.name_enter = Entry(viewActivity_frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
            self.name_enter.insert(0, "Activity Name")
            self.name_enter.bind('<FocusIn>', self.on_enter_name)
            self.name_enter.bind('<FocusOut>', self.on_leave_name)
            self.name_enter.pack(pady = 10)

            self.find_button = Button(viewActivity_frame, text='Find activity', bg='red', fg='white', border=0,
            command=self.getactivity)
            self.find_button.pack(pady = 10)

            self.specific_name_header = Label(viewActivity_frame, text = "Activity Name", font=('Microsoft YaHei UI Light', 12, 'bold'))
            self.specific_name_header.place(x = 10, y = 240)
            self.specific_name = Label(viewActivity_frame, text = "", font=('Microsoft YaHei UI Light', 12, 'bold'))
            self.specific_name.place(x = 20, y = 275)

            self.specific_cals_header = Label(viewActivity_frame, text = "Calories Burned", font=('Microsoft YaHei UI Light', 12, 'bold'))
            self.specific_cals_header.place(x = 10, y = 310)
            self.specific_cals = Label(viewActivity_frame, text = "", font=('Microsoft YaHei UI Light', 12, 'bold'))
            self.specific_cals.place(x = 20, y = 335)

            self.specific_elev_header = Label(viewActivity_frame, text = "Elevation", font=('Microsoft YaHei UI Light', 12, 'bold'))
            self.specific_elev_header.place(x = 10, y = 370)
            self.specific_elev = Label(viewActivity_frame, text = "", font=('Microsoft YaHei UI Light', 12, 'bold'))
            self.specific_elev.place(x = 20, y = 395)

            self.specific_zone_header = Label(viewActivity_frame, text = "Zone", font=('Microsoft YaHei UI Light', 12, 'bold'))
            self.specific_zone_header.place(x = 300, y = 240)
            self.specific_zone = Label(viewActivity_frame, text = "", font=('Microsoft YaHei UI Light', 12, 'bold'))
            self.specific_zone.place(x = 310, y = 275)

            self.specific_pace_header = Label(viewActivity_frame, text = "Pace", font=('Microsoft YaHei UI Light', 12, 'bold'))
            self.specific_pace_header.place(x = 300, y = 305)
            self.specific_pace = Label(viewActivity_frame, text = "", font=('Microsoft YaHei UI Light', 12, 'bold'))
            self.specific_pace.place(x = 310, y = 335)

            self.specific_hr_header = Label(viewActivity_frame, text = "Heart Rate", font=('Microsoft YaHei UI Light', 12, 'bold'))
            self.specific_hr_header.place(x = 300, y = 370)
            self.specific_hr = Label(viewActivity_frame, text = "", font=('Microsoft YaHei UI Light', 12, 'bold'))
            self.specific_hr.place(x = 310, y = 395)

            self.date_header = Label(viewActivity_frame,  text = "Date Completed", font=('Microsoft YaHei UI Light', 12, 'bold'))
            self.date_header.place(x = 390, y = 370)
            self.date_display = Label(viewActivity_frame, text = "", font=('Microsoft YaHei UI Light', 12, 'bold'))
            self.date_display.place(x = 390, y = 395)

            self.race_header = Label(viewActivity_frame, text = "", font=('Microsoft YaHei UI Light', 15, 'bold'))
            self.race_header.place(x = 350, y = 425)


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
            # Pack the new frame into the interactive_frame
            addActivity_frame.pack(fill='both', expand=True)
            addActivity_frame.config(bg = 'white')
            lb = tk.Label(addActivity_frame, text='Add Data', font=('Bold', 18))
            lb.pack()
            #Enter file prompt
            enc_prompt = Label(addActivity_frame, text = "Please enter your miles ran", font=('Microsoft YaHei UI Light', 12, 'bold'))
            enc_prompt.place(x=10, y =40)

            self.add_miles = Entry(addActivity_frame, width = 25, fg="black", border = 0, bg = "white", font=('Microsoft YaHei UI Light', 11))
            self.add_miles.place(x = 20, y = 80)
            self.add_miles.insert(0, 'Add data here')
            self.add_miles.bind('<FocusIn>', self.on_enter_miles)
            self.add_miles.bind('<FocusOut>', self.on_exit_miles)

            cal_prompt = Label(addActivity_frame, text = "Please enter your calories burned", font=('Microsoft YaHei UI Light', 12, 'bold'))
            cal_prompt.place(x = 10, y = 110)

            self.add_cals = Entry(addActivity_frame, width = 25, fg="black", border = 0, bg = "white", font=('Microsoft YaHei UI Light', 11))
            self.add_cals.place(x = 20, y = 140)
            self.add_cals.insert(0, 'Add cals here')
            self.add_cals.bind('<FocusIn>', self.on_enter_cals)
            self.add_cals.bind('<FocusOut>', self.on_exit_cals)

            elev_prompt = Label(addActivity_frame, text = "Please enter your elevation gained", font=('Microsoft YaHei UI Light', 12, 'bold'))
            elev_prompt.place(x =10, y = 170)

            self.elev_enter = Entry(addActivity_frame, width = 25, fg="black", border = 0, bg = "white", font=('Microsoft YaHei UI Light', 11))
            self.elev_enter.place(x=20, y=200)
            self.elev_enter.insert(0, 'Add elevation here')
            self.elev_enter.bind('<FocusIn>', self.on_enter_elev)
            self.elev_enter.bind('<FocusOut>', self.on_exit_elev)

            hr_prompt = Label(addActivity_frame, text = "Enter your average heart rate",  font=('Microsoft YaHei UI Light', 11, 'bold'))
            hr_prompt.place(x = 10, y = 230)

            self.hr_entry = Entry(addActivity_frame, width = 25, fg="black", border = 0, bg = "white", font=('Microsoft YaHei UI Light', 11))
            self.hr_entry.place(x = 20, y = 260)
            self.hr_entry.insert(0, 'Add Heart Rate here')
            self.hr_entry.bind('<FocusIn>', self.hr_on_entry)
            self.hr_entry.bind('<FocusOut>', self.hr_on_exit)

            pace_prompt = Label(addActivity_frame, text = "Please enter your average pace", font=('Microsoft YaHei UI Light', 12, 'bold'))
            pace_prompt.place(x = 20, y = 290)

            self.pace_entry = Entry(addActivity_frame, width = 25, fg="black", border = 0, bg = "white", font=('Microsoft YaHei UI Light', 11))
            self.pace_entry.place(x = 20, y = 320)
            self.pace_entry.insert(0, 'Add Average Mile Pace')
            self.pace_entry.bind('<FocusIn>', self.pace_enter)
            self.pace_entry.bind('<FocusOut>', self.pace_exit)

            name_prompt = Label(addActivity_frame, text = "Please enter activity name", font=('Microsoft YaHei UI Light', 12, 'bold'))
            name_prompt.place(x = 10, y = 340)

            self.name_entry = Entry(addActivity_frame, width = 25, fg="black", border = 0, bg = "white", font=('Microsoft YaHei UI Light', 11))
            self.name_entry.place(x = 20, y = 380)
            self.name_entry.insert(0, 'Enter activity name')
            self.name_entry.bind('<FocusIn>', self.name_enter)
            self.name_entry.bind('<FocusOut>', self.name_exit)

            self.activity_date = Calendar(addActivity_frame, selectmode = "day")
            self.activity_date.place(x = 420, y = 100)
            
            self.raceCheck = Checkbutton(addActivity_frame, text = "Race Day?", fg="black", border = 0, bg = "white", font=('Microsoft YaHei UI Light', 11))
            self.raceCheck.place(x = 420, y = 300)

            self.update_button = Button(addActivity_frame, text='Update', bg='red', fg='white', border=0,
            command=self.updatedata)
            self.update_button.place(x=330, y=400)
            


                    
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
        def hide_indicators(self):
            self.connect_marker.config(bg='grey')
            self.view_marker.config(bg='grey')
            self.rcv_marker.config(bg='grey')

        #method for deleting pages
        def delete_page(self):
            for frame in self.interactive_frame.winfo_children():
                frame.destroy()

        #method for switching pages (hides indicators, sets new indicator, deletes previous page, shows new page)
        def indicator(self, lb, page):
            self.hide_indicators()
            lb.config(bg='#42a1ff')
            self.delete_page()
            page()


        #---------USER-----------------#
        def on_enter_user(self, e):
            self.user.delete(0, 'end')

        def on_leave_user(self, e):
            name = self.user.get()
            if name == '':
                self.user.insert(0, 'Username')
        #---------END USER--------------#
        

    #-------------------------END CLIENT CLASS--------------------------------------------#


    #===========================MAIN======================================#
if __name__ == "__main__":
    jog = Jog()
    #=====================================================================#