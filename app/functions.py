import app.settings as SET

import sqlite3
import csv
import smtplib
import ssl
import pyautogui
import telebot
import pandas as pd
from email.message import EmailMessage



def ScreenSize():
    SCREENwidth, SCREENheight= pyautogui.size()
    return SCREENwidth,SCREENheight

##--- MAIN FUNCTIONS ---##
def UserInput():
    myChoose = input("""
        Welcome Bylad..
            quit
            email
            telegram
            start
            start link
            start data
            sql
            duplicated
            unwanted
            just print
        Choose one to run
    """)
    

    return myChoose

def splitList(myList,threads:int): 
    result = {}
    number = 1

    while myList:  
        if number>threads:
            number = 1 

        target = "thread-" + str(number)

        if not target in result.keys():
            result[target] = []
        else:
            temp = result[target]
            temp.append(myList.pop(0))
            result[target] = temp
                
        number += 1

    return result


##--- FILTER FUNCTIONS ---##
def duplicated_bombok():
    con = sqlite3.connect(SET.MAIN_DATABASE)
    cursor = con.cursor()

    cursor.execute("SELECT * FROM links")
    links = cursor.fetchall()
    data = {}

    for i in links:
        data[i[1]] = i

    newLength = str(len(data))
    oldLength = str(len(links))    
    cursor.execute("DROP TABLE links")
    cursor.execute("CREATE TABLE IF NOT EXISTS links(url1 TEXT,url2 TEXT,url3,companyName TEXT)")   
  
    for i in data:
        i = data[i]
        cursor.execute("INSERT INTO links VALUES(?,?,?,?)",(i[0],i[1],i[2],i[3].lower()))
        
    con.commit() 
    return (newLength,oldLength)   

def unWantedBitches():    
    unwanted_company =  [x[0].lower() for x in pd.read_excel(SET.UNWANTED_COMPANIES).values]
    counter = 0

    con = sqlite3.connect(SET.MAIN_DATABASE)
    cursor = con.cursor()

    cursor.execute("SELECT * FROM links")
    data = cursor.fetchall()

    cursor.execute("DROP TABLE links")
    cursor.execute("CREATE TABLE IF NOT EXISTS links(url1 TEXT,url2 TEXT,url3,companyName TEXT)")   
  
    for job in data:
        if job[3] in unwanted_company:
            counter += 1 
        else:
            cursor.execute("INSERT INTO links VALUES(?,?,?,?)",(job[0],job[1],job[2],job[3]))
    
    con.commit() 
    return (str(counter))  
        
##--- SETUP SQL ---##
def setup_postleitszahl():
    con = sqlite3.connect(SET.MAIN_DATABASE)
    cursor = con.cursor()

    result = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='postleitszahlen'").fetchone()
    
    if result != None:
        cursor.execute("DROP TABLE postleitszahlen")
        con.commit()
    
    with open(SET.POSTLEITSZAHLEN,'r') as file:        
        reader = csv.reader(file,delimiter=";")
        
        to_db = []
        for i in reader:
            if len(i[1]) != 5:
                i[1] = "0" + i[1]
            to_db.append((i[0], i[1], i[2], i[3]))
    
    cursor.execute('CREATE TABLE IF NOT EXISTS "postleitszahlen" ( "field1" TEXT, "field2" TEXT, "field3" TEXT, "field4" TEXT)')
    cursor.executemany("INSERT INTO postleitszahlen VALUES (?,?,?,?)", to_db)
    con.commit();con.close()
  
def setup_SQLTable():
    con = sqlite3.connect(SET.MAIN_DATABASE)
    cursor = con.cursor()

    #Table for Daten ziehen
    cursor.execute("""CREATE TABLE IF NOT EXISTS datenTamam(firmenName TEXT,articleName TEXT,standort TEXT,stelle TEXT,vollzeit TEXT,published TEXT,field1 TEXT,field2 TEXT,field3 TEXT,field4 TEXT,field5 TEXT,email TEXT,telefon TEXT,postLZ TEXT,url TEXT)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS datenYok(  firmenName TEXT, articleName TEXT, url TEXT)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS aussnahmen( firmenName TEXT, articleName TEXT, url TEXT)""")

    #Table for Links ziehen
    cursor.execute("CREATE TABLE IF NOT EXISTS links(url1 TEXT,url2 TEXT,url3,companyName TEXT)")   
    cursor.execute("CREATE TABLE IF NOT EXISTS failedLinks(url TEXT,empty TEXT)") 
    
    con.commit();con.close()
 
def targetSearchLinks():
    data = pd.read_excel(SET.TARGET_SEARCH_LINKS).values
    return [[x,y] for x,y in data]

def sendMail(content):
    email_sender = SET.EMAIL_SENDER
    email_password = SET.EMAIL_PASSWORD
    email_receiver = 'target_bumbumbuuum@outlook.com'        
    subject = 'Boooot'     

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(content)

    context = ssl.create_default_context()
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
 
def TeleMessage(TELEGRAM_MESSAGE):  
    bot = telebot.TeleBot(SET.API_KEY)
    bot.send_message(SET.CHANNEL_ID,TELEGRAM_MESSAGE)
    bot.stop_bot()