import sqlite3,time



class transport():
        
    def customQueryW(self,query):
        rows = self.cursor.execute(query)
        self.connection.commit()
        return rows
    
    def customQueryR(self,query):
        rows = self.cursor.execute(query).fetchall()
        return rows

    def download_file(self,fdate,tdate):
        query = f"""SELECT * from maindb WHERE times_now BETWEEN "{fdate}" and "{tdate}" """
        return self.customQueryR(query)

    def checkEntry(self,obj):
        query = """SELECT times_now,shift_now,serial,product,job,count(serial),clone from maindb WHERE serial='{}' and job='{}' and serial IS NOT NULL  GROUP BY serial """.format(obj.serial,obj.job)

        return self.customQueryR(query)

    def writeEntry(self,obj):
        query = """INSERT INTO maindb (times_now , shift_now , serial , product, job,tol,clone)
                   VALUES('{}','{}','{}','{}','{}',{},'False') """.format(obj.time_now,obj.shift,obj.serial,obj.product,obj.job,obj.tol)
        return self.customQueryW(query)
        

    def __init__(self):

        self.connection = sqlite3.connect("pms.records")
        self.cursor = self.connection.cursor()
        tables = self.cursor.execute("""SELECT name FROM sqlite_master  WHERE type ='table';""").fetchall()

        
        if not('maindb',) in tables:
            self.cursor.execute("""CREATE VIRTUAL TABLE maindb using fts5(times_now, shift_now , serial , product, job, tol, clone)""")
            self.connection.commit()
            

    def logwriter(self,time,shift,desc,line,info):
        self.cursor.execute(""" INSERT INTO systemfoots VALUES ('{}','{}','{}','{}','{}')""".format(time,shift,desc,line,info))

    def getqty(self,stime,etime):
        query =""" SELECT COUNT(*)from unitFootPrint WHERE times_now BETWEEN '{}' and '{}' """.format(stime,etime)
        return self.customQueryR(query)[0][0]

    def clr_clone(self,sno,value):
        query =""" UPDATE maindb SET clone="{}" WHERE serial="{}" """.format(str(value),sno)
        return self.customQueryW(query)
