from PyQt5 import QtCore, QtGui, QtWidgets,uic
from PyQt5.QtGui import *
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
                         QFontDatabase, QIcon, QLinearGradient, QPalette,
                         QPainter, QPixmap,QRadialGradient, QMovie, QTextCursor)
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog

from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import sys,livetimeapi,datetime,dbapi,os,json,resources,time,machine_interface,base64
from os.path import exists

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('mainui.ui', self)

class Dlg(QtWidgets.QMainWindow):
    def __init__(self):
        super(Dlg, self).__init__()
        uic.loadUi('dialaog.ui', self)

class Unit_x1:
    def __init__(self):
        self.serial:str=""
        self.product:str=""
        self.job:str=""
        self.time_now:int=0
        self.shift:str=""
        self.tol:str=""

class Unit_x2:
    def __init__(self):
        self.serial:str=""
        self.product:str=""
        self.job:str=""
        self.time_now:int=0
        self.shift:str=""
        self.tol:str=""


class app:
    def app_health_ng(self,value,console):
        self.reeset()
        self.health = value
        self.appdow.console_.setText(console)
        self.appdow.scan_input.setEnabled(value)
        self.appdow.scan_input.clear()
        if value == False:
            self.appdow.console_.setStyleSheet("color: rgb(255, 0, 0);")
            self.appdow.online_.setPixmap(QPixmap(u":/newPrefix/red.png"))
        else:
            self.appdow.console_.setStyleSheet("color: rgb(0, 145, 0);")
            self.appdow.online_.setPixmap(QPixmap(u":/newPrefix/online.png"))
            self.appdow.scan_input.setFocus(True)


    def app_clock(self):
        try:

            self.appdow.datetime_.setText("{} | {} | {}".format(str(self.timeapi.sdate()),
                                                               str(self.timeapi.stime()),
                                                               str(self.timeapi.sshift())))


           
        except Exception as e:
           self.exception_mgr(e)

    def app_beat(self):
        try:
            
            self.mac_interface.write_regs(self.mac_interface.ping,0,0)

            ping = self.mac_interface.read_regs(self.mac_interface.ackw,1)[0]
            if ping == 1:
                if self.health == False:
                    self.app_health_ng(True,"Ready!")
                    self.appdow.scan_input.setFocus(True)
               
            else:
                self.app_health_ng(False,"Machine Busy...")
            self.mac_interface.write_regs(self.mac_interface.ping,1,1)
        except Exception as e:
            self.app_health_ng(False,str(e))            
            self.exception_mgr(e)


    def app_life(self):
        try:
            self.looptimer = QtCore.QTimer()
            self.looptimer.timeout.connect(self.app_clock)
            self.looptimer.start(1000)

            self.appbeat = QtCore.QTimer()
            self.appbeat.timeout.connect(self.app_beat)
            self.appbeat.start(self.mac_interface.p_int)

        except Exception as e:
            self.exception_mgr(e)




    def eval_input(self):
        try:
            scan_data = self.appdow.scan_input.text()
            self.appdow.scan_input.clear()
            

            if self.health:

                if self.appdow.radBut_o.isChecked() or self.appdow.radBut_t.isChecked():
                    
                    if scan_data[0:2]=="71" and scan_data[0:2]!="19":
                        self.unit.serial = scan_data.upper()
                        self.appdow.label_serial_.setText(self.unit.serial)
                        self.appdow.cb_serial.setPixmap(QPixmap(u":/newPrefix/check.png"))
                        self.appdow.console_.setText("Serial# Scan Success!")
                        self.appdow.console_.setStyleSheet("color: rgb(0,145, 0);")

                    elif "-" in scan_data and scan_data[0:2]!="19":
                        self.unit.product = scan_data.upper()
                        data = eval(open("varient.file","r+").read())
                        self.unit.tol = data[str(int(self.unit.product.split("-")[1][0:-1]))]
                        self.appdow.label_product_.setText(self.unit.product)
                        self.appdow.cb_product.setPixmap(QPixmap(u":/newPrefix/check.png"))
                        self.appdow.console_.setText("Product# Scan Success!")
                        self.appdow.console_.setStyleSheet("color: rgb(0,145, 0);")


                    elif scan_data[0:2]=="00" and scan_data[0:2]!="19" and scan_data[0:1]!="7":
                        self.unit.job = scan_data.upper()
                        self.appdow.label_job_.setText(self.unit.job)
                        self.appdow.cb_job.setPixmap(QPixmap(u":/newPrefix/check.png"))
                        self.appdow.console_.setText("Serial# Scan Success!")
                        self.appdow.console_.setStyleSheet("color: rgb(0,145 ,0);")

                    else:
                        
                        self.appdow.console_.setText("Invalid Entry")
                        self.appdow.console_.setStyleSheet("color: rgb(255, 0, 0);")

                    if self.unit.serial!="" and self.unit.job!="" and self.unit.product!="":
                        
                        self.appdow.console_.setText("Processing...")
                        self.unit.time_now=self.timeapi.unixnow()
                        self.unit.shift=self.timeapi.sshift()
                        entryCheck =  self.dbms.checkEntry(self.unit)
                        listof_clone = []

                        if entryCheck==[]:
                            process_check=True

                        else:
                            for row in entryCheck:
                                if row[6]=="True":
                                    listof_clone.append(True)
                                elif row[6]=="False":
                                    listof_clone.append(False)

                        if True in listof_clone:
                            process_check=True
                            self.dbms.clr_clone(self.unit.serial,False)
                        elif listof_clone ==[]:
                            process_check=True
                        else:
                            process_check=False

                        if process_check:
                            if self.coils ==1:
                                self.mac_interface.write_regs(self.mac_interface.data,int(self.unit.product.split("-")[1][0:-1]),4)
                                self.mac_interface.write_regs(self.mac_interface.data_mm,int(self.unit.tol),4)
                                self.dbms.writeEntry(self.unit)
                                self.reeset()
                                self.appdow.console_.setStyleSheet("color: rgb(0, 145, 0);")
                                
                                self.appdow.console_.setText("Scan Complete - Start the Machine...")
                            elif self.coils ==2 and self.roll_1 == None:
                                self.roll_1 = self.unit
                                self.unit = Unit_x1()
                                self.appdow.console_.setStyleSheet("color: rgb(0, 145, 0);")
                                self.appdow.console_.setText("Coil_1 Record Success!,Scan Coil 2#")
                                self.clear_fields()
                            
                            elif self.coils ==2 and self.roll_1 != None:
                                if self.roll_1.product == self.unit.product:
                                    if self.roll_1.serial != self.unit.serial:
                                        self.mac_interface.write_regs(self.mac_interface.data,int(self.unit.product.split("-")[1][0:-1]),4)
                                        self.dbms.writeEntry(self.unit)
                                        self.dbms.writeEntry(self.roll_1)
                                        self.roll_1 = None
                                        self.appdow.console_.setStyleSheet("color: rgb(0, 145, 0);")
                                        self.appdow.console_.setText("Scan Complete - Start the Machine...")
                                        self.reeset()
                                    else:
                                        self.appdow.console_.setStyleSheet("color: rgb(255, 0, 0);")
                                        self.appdow.console_.setText("Same Label Detected! Resetting...")
                                        self.roll_1 = None
                                        self.reeset()

                                else:
                                    self.appdow.console_.setStyleSheet("color: rgb(255, 0, 0);")
                                    self.appdow.console_.setText("Product# mistmatch - Resetting...")
                                    self.roll_1 = None
                                    self.reeset()
                            
                        else:
                            print(entryCheck)
                            print(entryCheck[len(entryCheck)-1],len(entryCheck)-1)
                            print(entryCheck[len(entryCheck)-1][0])
                            dateTime_ = str(self.timeapi.cdatetime(entryCheck[len(entryCheck)-1][0]))
                            self.windlg.title_.setText("Duplicate entry!")
                            self.windlg.serial_.setText(str(entryCheck[0][2]))
                            self.windlg.product_.setText(str(entryCheck[0][3]))
                            self.windlg.job_.setText(str(entryCheck[0][4]))
                            self.windlg.datetime_.setText( dateTime_ + " | " + str(entryCheck[0][1]))
                            self.windlg.show()
                            self.windlg.warn_ok.setFocus(True)
                            self.appdow.console_.setStyleSheet("color: rgb(255, 0, 0);")
                            self.appdow.console_.setText("Duplicate entry!")
                else:
                    self.appdow.console_.setStyleSheet("color: rgb(255, 0, 0);")
                    self.appdow.console_.setText("Select Mode of operations.")
                                                                                                          
            else:
                self.appdow.console_.setStyleSheet("color: rgb(255, 0, 0);")
                self.appdow.console_.setText("System failure, Please refresh...")

        except Exception as e:
            self.exception_mgr(e)


    def clear_fields(self):
        self.appdow.label_serial_.clear()
        self.appdow.label_product_.clear()
        self.appdow.label_job_.clear()
        self.appdow.cb_serial.setPixmap(QPixmap(u":/newPrefix/setp.png"))
        self.appdow.cb_product.setPixmap(QPixmap(u":/newPrefix/setp.png"))
        self.appdow.cb_job.setPixmap(QPixmap(u":/newPrefix/setp.png"))

    def reeset(self):
        try:
            self.appdow.configuration_frame.setEnabled(False)
            self.appdow.flow_control_frame.setEnabled(False)
            if self.health:
                self.coils=0
                self.radioToogle()
                self.appdow.scan_input.setEnabled(True)
                self.appdow.scan_input.setFocus(True)

                self.appdow.cb_serial.setPixmap(QPixmap(u":/newPrefix/setp.png"))
                self.appdow.cb_product.setPixmap(QPixmap(u":/newPrefix/setp.png"))
                self.appdow.cb_job.setPixmap(QPixmap(u":/newPrefix/setp.png"))
                self.clear_fields()
                self.unit = Unit_x1()
                # self.appdow.console_.setStyleSheet("color: rgb(0, 145, 0);")            
                # self.appdow.console_.setText("Initializing... ")
                self.windlg.hide()

            else:
                self.appdow.console_.setStyleSheet("color: rgb(255, 0, 0);")
                self.appdow.console_.setText("System failure, Please refresh...")

        except Exception as e:
            self.exception_mgr(e)

    def logout_eng(self,iv=True):
        try:
            self.appdow.configuration_frame.setEnabled(False)
            self.appdow.flow_control_frame.setEnabled(False)
            self.appdow.varient_search.clear()
            self.appdow.setTol.clear()
            self.appdow.varient_name.clear()
            self.appdow.tol_value.clear()
            self.appdow.redo_sn.clear()
            self.appdow.username_.clear()
            self.appdow.password_.clear()
            if iv:
                self.appdow.Sts_msg_loin.setText("Logout Success!")

        except Exception as e:
            self.exception_mgr(e)
    def login_eng(self):
        try:
            username_ = self.appdow.username_.text()
            password_ = self.appdow.password_.text()
            self.appdow.username_.clear()
            self.appdow.password_.clear()
            if base64.b64decode(self.settings_["engineer"]).decode('utf-8') == username_+":"+password_:
                self.appdow.configuration_frame.setEnabled(True)
                self.appdow.flow_control_frame.setEnabled(True)
                self.appdow.Sts_msg_loin.setText("Login Success!")
                
            else:
                self.appdow.Sts_msg_loin.setText("Invalid Credentials!")
                self.logout_eng(iv=False)
                
        except Exception as e:
            self.logout_eng(iv=False)
            self.exception_mgr(e)
       

    def file_save(self,data,filename):
        try:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            dlg,_= QFileDialog.getSaveFileName(self.appdow,"Save records",filename,"CSV Files (*.csv)", options=options)
            file = open(dlg,"w")
            file.write(data)
            file.close()
        except Exception as e:
            self.exception_mgr(e)


    def download(self):
        try:
            fdate = self.appdow.fdate_.date().toPyDate()
            tdate = self.appdow.tdate_.date().toPyDate()
            fdate = self.timeapi.form_unix(fdate)
            tdate = self.timeapi.form_unix(tdate)
            tdate = 86400 + tdate
            rows = self.dbms.download_file(fdate,tdate)
            table = "Date,time,Shift,Serial#,Product#,Job#,Tol#\n"
            for row in rows:
                for idx,col in enumerate(row):
                    if idx==0:
                        table += str(self.timeapi.cdate(int(col))) +"," +str(self.timeapi.ctime(int(col))) +","
                    else:
                        table += str(col)+","
                table +="\n"
            fName = str(self.timeapi.unixnow())
            self.file_save(table,fName+".csv")
           
          
            self.appdow.console_.setText("Downloading records...")
        except Exception as e:
 
            self.exception_mgr(e)

    def radioToogle(self):
        
        self.appdow.scan_input.setFocus(True)
        self.unit = Unit_x1()
        self.roll_1 = None
        self.clear_fields()
        if self.appdow.radBut_o.isChecked():
            self.coils = 1
            
            

        elif self.appdow.radBut_t.isChecked():
            self.coils = 2

        else:
            self.appdow.console_.setStyleSheet("color: rgb(0, 0, 255);")
            self.appdow.console_.setText("Select the Mode of Operation")


    def find_the_varient(self):
        try:
            self.appdow.Sts_msg_save.clear()
            file_exists = exists("varient.file")
            
            if not file_exists:
                d = {}
                for each in range(1000):
                    d[str(each)]= str(0)
                open("varient.file","w+").write(str(d))

            data = eval(open("varient.file","r+").read())
            key = self.appdow.varient_search.text()
            if not key == "":
                self.appdow.varient_name.setText(key)
                if data[key]:
                    self.appdow.tol_value.setText(data[key])
                else:
                    self.appdow.varient_name.clear()
            else:
                self.appdow.Sts_msg_save.setText("Field cannot be empty")
        except Exception as e:
            self.exception_mgr(e)

    def clear_all_fields(self):
        self.appdow.varient_search.clear()
        self.appdow.setTol.clear()
        self.appdow.varient_name.clear()
        self.appdow.tol_value.clear()

    def save_the_varient(self):
        try:
            data = eval(open("varient.file","r+").read())
            key = self.appdow.varient_search.text()
            val = self.appdow.setTol.text()
            if not key =="" and not val=="": 
                data[str(key)]=str(val)
                open("varient.file","w+").write(str(data))
                self.appdow.Sts_msg_save.setText("Save Success")
                self.clear_all_fields()
            else:
                self.appdow.Sts_msg_save.setText("Field cannot be empty")


        except Exception as e:
            self.appdow.Sts_msg_save.text("Save Failed!")
            self.exception_mgr(e)




    def saveRedo(self):
        try:
            serial = (self.appdow.redo_sn.text()).upper()
            if not serial == "":
                self.appdow.redo_sn.clear()
                self.dbms.clr_clone(serial,True)
                self.appdow.flow_info.setText(serial +" Duplication Authorised!")
            else:
                self.appdow.flow_info.setText("Field cannot be empty")
        except Exception as e:
            self.appdow.flow_info.setText(serial +" Duplication Authorisation Failed!")
            self.exception_mgr(e)

    def remove_redo(self):
        try:
            serial = (self.appdow.redo_sn.text()).upper()
            if not serial == "":
                self.appdow.redo_sn.clear()
                self.dbms.clr_clone(serial,False)
                self.appdow.flow_info.setText(serial +" Duplication Removed!")
            else:
                self.appdow.flow_info.setText("Field cannot be empty")

        except Exception as e:
            self.appdow.flow_info.setText(serial +" Duplication Authorisation Failed!")
            self.exception_mgr(e)

    def connetion_mafia(self):
        try:
            today = datetime.datetime.now()
            self.appdow.scan_input.returnPressed.connect(self.eval_input)
            self.appdow.reset_.clicked.connect(self.reeset)
            self.appdow.varient_find.clicked.connect(self.find_the_varient)
            self.appdow.remove_redo.clicked.connect(self.remove_redo)
            self.appdow.download_.clicked.connect(self.download)
            self.appdow.login_but.clicked.connect(self.login_eng)
            self.appdow.logot_but.clicked.connect(lambda:self.logout_eng(iv=True))
            self.appdow.save_tol.clicked.connect(self.save_the_varient)
            self.windlg.warn_ok.clicked.connect(self.reeset)
            self.appdow.refresh_.clicked.connect(self.refresh_settings)
            self.appdow.radBut_o.toggled.connect(self.radioToogle)
            self.appdow.radBut_t.toggled.connect(self.radioToogle)
            self.appdow.save_redo.clicked.connect(self.saveRedo)
            d = QDateTime(today.year, today.month, today.day, today.hour, today.minute)

            self.appdow.fdate_.setMaximumDateTime(d)
            self.appdow.tdate_.setMaximumDateTime(d)

            self.appdow.fdate_.setDateTime(d)
            self.appdow.tdate_.setDateTime(d)

        except Exception as e:
            self.exception_mgr(e)

    def msgbtn(self,i):
        print ("Button pressed is:",i.text())
    
    def showDialog(self,msg,type_):
        
        msgBox = QMessageBox()
        if type_ == "Err":
            msgBox.setIcon(QMessageBox.Warning)
        else:
            msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(str(msg))
        msgBox.setWindowTitle("Alert!")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.buttonClicked.connect(self.msgbtn)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            print('OK clicked')            
            

    def exception_mgr(self,value):
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        open("error.log","a+").write(f"{exc_type}:{fname} : {exc_tb.tb_lineno}")
        self.appdow.console_.setText(str(value))
        self.appdow.console_.setStyleSheet("color: rgb(255, 0, 0);")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        #self.showDialog(f"{exc_type}:{fname} : {exc_tb.tb_lineno}","Err")


    def get_settings(self):
        try:
            settings_file = open("settings.conf")
            settings_ = json.load(settings_file)
            self.settings_ = settings_
        except Exception as e:
            self.showDialog(f"Settings File missing","Err")
            self.exception_mgr("Settings File missing")
    
    def refresh_settings(self):
        try:
            self.get_settings()
            self.timeapi = livetimeapi.main(self.settings_)
            self.mac_interface = machine_interface.connect_machine(self.settings_)
            self.reeset()

        except Exception as e:
            self.exception_mgr(str(e))



    def __init__(self):
        try:
            self.coils=0
            self.health = False
            self.app = QtWidgets.QApplication(sys.argv)
            self.get_settings()
            self.splash = QtWidgets.QSplashScreen(QPixmap(u':/newPrefix/banner.png'))
            self.splash.show()

            self.appdow = Ui()
            self.windlg = Dlg()

        
            self.windlg.warn.setPixmap(QPixmap(u":/newPrefix/warnning.png"))
            self.appdow.bgms.setPixmap(QPixmap(u":/newPrefix/label.jpg"))

            self.appdow.setWindowIcon(QtGui.QIcon(u":/newPrefix/FAVICON.png"))
            self.windlg.setWindowIcon(QtGui.QIcon(u":/newPrefix/FAVICON.png"))

            self.appdow.scan_input.setFocus(True)

            self.radioToogle()
            
            self.dbms = dbapi.transport()
            self.refresh_settings()
            self.app_life()
            self.connetion_mafia()
            self.appdow.show()
            self.splash.hide()
            
            sys.exit(self.app.exec_())
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(fname,exc_tb.tb_lineno)
            self.showDialog(f"Application Boot error!","Err")
            sys.exit()




if __name__ == "__main__":
   
   appObj = app()
   
