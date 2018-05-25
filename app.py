import paho.mqtt.publish as publish
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import paho.mqtt.client as mqtt
import re
import sendemailfull
import webbrowser
import threading
import dong
import sendemailkosub
import smtplib

name = ''
nhietdo = ''
doam = ''
meo = ''
j= 0
k = -1
dem = 0

publish.single("khoi/demo/app", "READY", hostname="192.168.43.54") 
class Application(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()
  
    def initUI(self):
        self.parent.title("Test")
        self.img1 = PhotoImage(file = 'D:\\Code\\Python\\HTN\\lamp.png').subsample(10,10)
        self.imgon = PhotoImage(file = 'D:\\Code\\Python\\HTN\\btnon.png').subsample(40,40)
        self.imgoff = PhotoImage(file = 'D:\\Code\\Python\\HTN\\btnoff.png').subsample(35,35)
        self.imgmail = PhotoImage(file = 'D:\\Code\\Python\\HTN\\email.png').subsample(35,35)
        self.imgweb = PhotoImage(file = 'D:\\Code\\Python\\HTN\\web.png').subsample(15,15)

        self.label1 = ttk.Label(self.parent, image = self.img1)
        self.label1.grid(row = 0, column = 0, padx = 2, pady =2 )

        ttk.Style().configure("BW.TButton", foreground='black', background='white')
        self.btn1 = ttk.Button(self.parent, text = "ON", width =0, command = self.on,image = self.imgon, compound = 'left', style = 'BW.TButton')
        self.btn2 = ttk.Button(self.parent, text = "OFF", width =0,command = self.off, image = self.imgoff, compound = 'left', style = 'BW.TButton')
        self.btn1.grid(row = 0, column = 1)
        self.btn2.grid(row = 0, column = 2)
        self.btn4 = ttk.Button(self.parent, text = "Setup", width = 5,compound = "center", command =self.sp)
        self.btn4.grid(row = 3, column =1, columnspan = 2)

        self.label6 = ttk.Label(self.parent, text = "Nhiệt độ", width = 8)
        self.label7 = ttk.Label(self.parent, text = "Độ ẩm", compound = "right")
        self.label6.grid(row = 5, column = 1)
        self.label7.grid(row = 5, column = 2)

        self.btn5 = ttk.Button(self.parent, text = "Gửi gmail", width = 0,image = self.imgmail, compound = 'left', command = self.gmail)
        self.btn5.grid(row = 6, column = 0, columnspan =2)

        self.btn6 = ttk.Button(self.parent, text = "Mở web", width = 0,image = self.imgweb, compound = 'left', command = self.web)
        self.btn6.grid(row = 6, column = 2)

    def on(self):
        self.lamp = "ON"

    def off(self): 
        self.lamp = "OFF"

    def sp(self): 
        if(self.lamp == 'ON'):
            publish.single("khoi/demo/app", "LAMPON", hostname="192.168.43.54") 
        elif(self.lamp == 'OFF'):
            publish.single("khoi/demo/app", "LAMPOFF", hostname="192.168.43.54") 
        messagebox.showinfo(title = 'Thông báo', message = "Đèn đang: " + self.lamp)

    def web(self):
        webbrowser.open("http://127.0.0.1:8050")

    def gmail(self):
        global name
        global meo
        self.second_win = Toplevel(self.parent)
        self.second_win.title("Gmail")
        self.second_win_lbl1 = ttk.Label(self.second_win, text = "Name:", width =7)
        self.second_win_lbl1.grid(row =0, column = 0,pady =5, padx =5)

        self.second_win_txt1 = Entry(self.second_win, width = 30)
        self.second_win_txt1.grid(row =0, column = 1)

        self.second_win_lbl2 = ttk.Label(self.second_win, text = "Email:", width =7)
        self.second_win_lbl2.grid(row =1, column = 0)

        self.second_win_txt2 = Entry(self.second_win, width = 30)
        self.second_win_txt2.grid(row =1, column = 1, pady =5,padx =5)

        self.second_win_btn1 = ttk.Button(self.second_win, text = "Quit", width = 10, command = self.second_win.quit)
        self.second_win_btn1.grid(row =2, column = 0, sticky = 'sw')

        self.second_win_btn2 = ttk.Button(self.second_win, text = "Send", width = 10, command = self.sendmeo)
        self.second_win_btn2.grid(row =2, column = 1)
        self.second_win.mainloop()

    def sendmeo(self):
        self.name = self.second_win_txt1.get()
        self.meo = self.second_win_txt2.get()
        self.obj = sendemailfull.MessageUser()
        self.obj.add_user(self.name,nhietdo,doam, email = self.meo)
        self.obj.get_details()
        self.obj.send_email()

def on_connect(mqttc, obj, flags, rc):
    pass

def on_message(mqttc, obj, msg):
    global nhietdo
    global doam
    global j
    global k
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    i = str(msg.payload)
    y = re.findall('[0-9]+',i)
    k = i.find('YES')
    print(k)
    nhietdo = y[0]
    doam = y[2]
    file = open("example.txt", "a")
    chuoi = str(j) + ',' + str(nhietdo) + ',' + str(doam)+'\n'
    file.write(chuoi)
    file.close()
    j += 1
    label4 = ttk.Label(root, text = nhietdo + " C")
    label5 = ttk.Label(root, text = doam + " %")
    label4.grid(row = 4, column = 1)
    label5.grid(row = 4, column = 2)

def on_publish(mqttc, obj, mid):
    print("mid: "+str(mid))
 
def on_subscribe(mqttc, obj, mid, granted_qos):
    pass

def on_log(mqttc, obj, level, string):
    pass

def bieudo():
    dong.app.run_server(debug=False)

def mail2():
    global dem
    while True:
        if (k != -1 and dem ==0):
            email_conn = smtplib.SMTP(sendemailkosub.host, sendemailkosub.port)
            email_conn.ehlo()
            email_conn.starttls()
            email_conn.login(sendemailkosub.username,sendemailkosub.password)
            email_conn.sendmail(sendemailkosub.from_email, sendemailkosub.to_list, "Co gi do khong dung")
            email_conn.quit()
            dem +=1

mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
mqttc.connect("192.168.43.54", 1883, 60) #dien IP cua Pi, vd: 192.168.1.77
mqttc.subscribe("khoi/demo/data", 0)    

root = Tk()
ex = Application(root)
if __name__ == '__main__':
    thread1 = threading.Thread(target=bieudo)
    thread1.start()
    thread2 = threading.Thread(target=mail2)
    thread2.start()
    mqttc.loop_start()
    root.mainloop()
