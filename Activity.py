class Activity:

    def __init__(self):
        self.miles = 0
        self.elevation = 0
        self.calories = 0
        self.heartrate = 0
        self.zone = 0
        self.pace = 0
        self.wname = ""
        self.act_date = None
        self.race_day = False

    #setters
    def set_name(self, workname):
        self.wname = workname
    def set_pace(self, userpace):
        self.pace = int(userpace)
    def set_miles(self, usermiles):
        self.miles = int(usermiles)
    def set_elevation(self, userelev):
        self.elevation = int(userelev)
    def set_zone(self, userage):
        maxhr = 220 - userage
        hr = self.get_hr()
        hr = float(hr)
        if hr == 0:
            print("Unable to calculate without a heart rate")
        else:
            if hr >= maxhr * 0.50 and hr <= maxhr * 0.60:
                self.zone = 1
            elif hr >= maxhr*0.60 and hr <= maxhr * 0.70:
                self.zone = 2
            elif hr >= maxhr * 0.70 and hr <= maxhr * 0.80:
                self.zone = 3
            elif hr >= maxhr * 0.80 and hr <= maxhr * 0.90:
                self.zone = 4
            else:
                self.zone = 5
    def set_cals(self, usercals):
        self.cals = usercals
    def set_hr(self, userhr):
        self.heartrate = userhr
    def set_date(self, userdate):
        self.act_date = userdate
    def set_race(self, userrace):
        self.race_day = userrace
        


    #getters
    def get_pace(self):
        return self.pace
    def get_miles(self):
        return self.miles
    def get_elevation(self):
        return self.elevation
    def get_hr(self):
        return self.heartrate
    def get_cals(self):
        return self.calories
    def get_zone(self):
        return self.zone
    def get_name(self):
        return self.wname
    def get_date(self):
        return self.act_date
    def get_race(self):
        return self.race_day
    