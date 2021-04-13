# to capture screenshots

import pyscreenshot 
import time 

minute=int(input("Minutes"))

def capture(minute):
    i=0
    # To capture the screen 
    image = pyscreenshot.grab() 
    image.show() 
    time.sleep(minute*60)
    image.save("image"+str(i)+".png") 
    i=i+1

capture(minute)

# to store running processes with timestamp into the database

from subprocess import PIPE, run
import mysql.connector

#change accordind to your mysql database, username and password

mydb = mysql.connector.connect(
  host="localhost",
  user="username",
  password="password",
  database="dbname"
)

mycursor = mydb.cursor()


def out(command):
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    return result.stdout
lis=[]
my_output = out("ps -eo cmd,lstart").strip()
my_output=my_output.split('\n')

for i in my_output:
    lis.append(i)

lis=lis[2::]
import re
p_name=[]
ts=[]

for i in range(len(lis)):
    m = re.findall(r'\[.*?\]', lis[i]) 
    n = lis[i].partition(']')[2] 
    n = n.lstrip()
    p_name.append(m)
    ts.append(n)
    


sql ='''CREATE TABLE Processes(process_name varchar(100), time_stamp varchar(100)) '''
mycursor.execute(sql)

for i in p_name:
    sql='INSERT INTO Processes (process_name) VALUES (%s)'
    val=[(i)]
    mycursor.execute(sql,val)

for i in ts:
    sql='INSERT INTO Processes (time_stamp) VALUES (%s)'
    val=[(i)]
    mycursor.execute(sql,val)

    
# to store tab_name with time stamp

sql ='''CREATE TABLE Tab(tab_name varchar(100), tab_time_stamp varchar(30)) '''
mycursor.execute(sql)

import gi
gi.require_version("Wnck", "3.0")
from gi.repository import Wnck

scr = Wnck.Screen.get_default()
scr.force_update()
tab_name=scr.get_active_window().get_name()
tab_name_list=[]
tab_name_list.append(tab_name)

t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)
tab_ts=[]
tab_ts.append(current_time)

for i in tab_name:
    sql='INSERT INTO Tab (tab_name) VALUES (%s)'
    val=[(i)]
    mycursor.execute(sql,val)
    
for i in tab_ts:
    sql='INSERT INTO Tab (tab_time_stamp) VALUES (%s)'
    val=[(i)]
    mycursor.execute(sql,val)
    
mydb.commit()
