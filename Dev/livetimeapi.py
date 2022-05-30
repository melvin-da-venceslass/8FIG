import datetime,time,json



class main():
    def form_unix(self,value):
        day   = str(value).split("-")
        dtime = datetime.date(int(day[0]), int(day[1]), int(day[2]))
        dtime = int(time.mktime(dtime.timetuple()))
        return dtime

    def cdatetime(self,unix):
        ctime = time.strftime(f"{self.settings_['date_form']} :: {self.settings_['hour_form']}",time.localtime(int(unix)))
        return ctime

    def cdate(self,unix):
        ctime = time.strftime(f"{self.settings_['date_form']}",time.localtime(int(unix)))
        return ctime
    
    def ctime(self,unix):
        ctime = time.strftime(f"{self.settings_['hour_form']}",time.localtime(int(unix)))
        return ctime


    def stime(self):
        ctime = time.strftime(f"{self.settings_['time_form']}",time.localtime(time.time()))
        return ctime
    
    def sdate(self):
        cdate = time.strftime(f"{self.settings_['date_form']}",time.localtime(time.time()))
        return cdate
    
    def shour(self):
        chour = time.strftime("%H",time.localtime(time.time()))
        return chour

    def sshift(self):
        now = self.shour()
        if now in self.shift_A:
            cshift = "A"
            return cshift
        elif now in self.shift_B:
            cshift = "B"
            return cshift
        elif now in self.shift_C:
            cshift = "C"
            return cshift
        
    def timeframe(self,unixtimes,out):
        ctime = datetime.datetime.fromtimestamp(int(round(unixtimes)))
        stime = ctime.replace(minute=0, second=0).timestamp()
        etime = stime + 3600
        ptime = stime - 3600

        if out =='s':
            return stime
        elif out == 'e':
            return etime
        
    def cTimeFrame(self):
        unixtimes = time.time()
        ctime = datetime.datetime.fromtimestamp(int(round(unixtimes)))
        stime = ctime.replace(minute=0, second=0).timestamp()
        etime = stime + 3600
        ptime = stime - 3600
        return [round(stime),round(etime),round(ctime.timestamp())]

        
    def unixnow(self):
        unix = round(time.time())
        return unix      
       
    
    def __init__(self,settings_):
        self.settings_ = settings_
        self.shift_C = settings_["shift_hours"]["shift_C"]
        self.shift_A = settings_["shift_hours"]["shift_A"]
        self.shift_B = settings_["shift_hours"]["shift_B"]


