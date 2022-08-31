import sqlite3, time, traceback, re

from  app.functions import *

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By

def get_data(links:list):
    X,Y = ScreenSize()
    driver =  webdriver.Firefox("") 
    driver.set_window_size(600, 600)
    driver.set_window_position(0,0)

    time.sleep(15)

    con = sqlite3.connect(SET.MAIN_DATABASE)
    cursor = con.cursor()

    cookie_have_to_close = True

    for url in links:
        print("***************************************** \n")
        url = "https://www.stepstone.de" + str(url[1])
        driver.get(url)
        time.sleep(2)


        

        while True:
            if driver.execute_script("return document.readyState") != "complete": 
                time.sleep(0.5) 
            else:              
                exec1 = driver.execute_script("return document.getElementsByClassName('sec-container').length")
                if exec1 == 1:
                    print("INFO: Onloading Page") 
                    time.sleep(10)
                    
                    exec2 = driver.execute_script("return document.getElementsByClassName('sec-container').length")
                    if exec2 == 1:
                        print("still onloading page..have to F5")
                        driver.refresh()
                        time.sleep(5)

                exec3 = driver.execute_script("return document.getElementsByClassName('sec-container').length")
                if exec3 == 0:
                    print("INFO: no loading")
                    break

        contine = True

        while True:
            try:     
                time.sleep(2)
                html_icerigi = driver.page_source
                soup = BeautifulSoup(html_icerigi, features='lxml')

                if cookie_have_to_close:
                    driver.find_element(by=By.XPATH, value= "//span[text()='Alles akzeptieren']").click()
                    print("INFO: coockies eaten")

                    cookie_have_to_close = False    
                    time.sleep(2)  
                
                top = list(soup.find("div",{"class":SET.getData_element_top}))
                

                firmenName = top[0].find('a').text          #Name der Firma
                articleName = top[1].find('h1').text        #Stellen Bezeichnung
                thirdTop = list(top[2].find('ul'))          #Eigenschaften der Stelle            
                
                if len(thirdTop) == 4:      #Wenn es nur 4 eigenschaften gibt
                    standort = thirdTop[0].text
                    stelle = thirdTop[1].text
                    vollzeit = thirdTop[2].text
                    publishedTime = thirdTop[3].text.split(":")[1].strip()

                    print(articleName)

                elif len(thirdTop) == 5:    #Wenn es nur 5 eigenschaften gibt
                    standort = thirdTop[1].text
                    stelle = thirdTop[2].text
                    vollzeit = thirdTop[3].text
                    publishedTime = thirdTop[4].text.split(":")[1].strip()

                    print(articleName)
                    print("publishedTime:",publishedTime)
                
                else:       #Wenn es eine Ausnahme ist wegen keine gute homoooo eigenschaften 
                    cursor.execute("INSERT INTO aussnahmen VALUES(?,?,?)",(articleName,firmenName,url))
                    con.commit()
                    break
                    
                descriptions = list(soup.find("div",{"class":SET.getData_element_description}))
                descriptionsLength = len(descriptions)

                if descriptionsLength == 5 :                  
                    field1 = descriptions[0].text
                    field2 = descriptions[1].text
                    field3 = descriptions[2].text
                    field4 = descriptions[3].text
                    field5 = descriptions[4].text #kontakt                 

                elif descriptionsLength == 4:
                    field1 = descriptions[0].text
                    field2 = descriptions[1].text
                    field3 = descriptions[2].text
                    field4 = " "
                    field5 = descriptions[3].text #kontakt                 
                    
                elif descriptionsLength == 3:
                    field1 = descriptions[0].text
                    field2 = descriptions[1].text
                    field3 = descriptions[2].text
                    field4 = " "
                    field5 = " "
                    
                    kontak_email = " "                

                else:
                    cursor.execute("INSERT INTO datenYok VALUES(?,?,?)",(articleName,firmenName,url))
                    con.commit()
                    break
                

                kontakt = field5
                if kontakt == " ": #wenn kontakte leer ist
                    query = (firmenName,articleName,standort,stelle,vollzeit,publishedTime,field1,field2,field3,field4,field5," "," "," ",url)
                else:
                    #---Findet die email---
                    match = re.search(r'[\w.+-]+@[\w-]+\.(com|de|net|org|COM|DE|NET|ORG)', kontakt)
                    if match:
                        kontak_email = match.group(0)
                    else:
                        kontak_email = ""

                    #---Findet die postleitszahl---        
                    alleNummern = [s for s in kontakt.split() if(len(s)==5 and s.isdigit())]
                    if len(alleNummern) == 0:
                        postLZahl = ""
                    else:
                        for zahl in alleNummern:
                            cursor.execute("SELECT * FROM postleitszahlen WHERE field2='{}'".format(zahl))
                            postLeitZahlDATA = cursor.fetchall()
                            
                            if (postLeitZahlDATA):
                                postLZahl = zahl

                                #postlz aus kontakte löschen und weiter mit der scheiße
                                kontakt = kontakt[0:kontakt.find(postLZahl)] + kontakt[kontakt.find(postLZahl)+5:]
                                break
                            else:
                                postLZahl = ""
                    

                    #---Findet die Telefon Nummer---                
                    matches = [match.span()[0] for match in re.compile(r"\d").finditer(kontakt)]
                    if not matches :
                        telefonNo = ""
                    else:
                        letzte_zahl = matches[0]
                        TelefonKoordinaten = []

                        for i in matches:
                            if (i - letzte_zahl)>4:
                                if len(TelefonKoordinaten)>=6: #Telefon muss mindestens 6 stellig sein
                                    break        
                                TelefonKoordinaten = []       
                            
                            TelefonKoordinaten.append(i)
                            letzte_zahl = i
                            
                        if len(TelefonKoordinaten) >= 6:
                            telefonNo = "".join([kontakt[i] for i in TelefonKoordinaten])
                        else:
                            telefonNo = ""

                    query = (firmenName,articleName,standort,stelle,vollzeit,publishedTime,field1,field2,field3,field4,field5,kontak_email,telefonNo,postLZahl,url) 

                cursor.execute("INSERT INTO datenTamam VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",query)
                con.commit()

                break

            except Exception:
                traceback.print_exc()
                if contine == False:
                    cursor.execute("INSERT INTO datenYok VALUES(?,?,?)",("None","None",url));con.commit()
                    contine = True
                    print("Kayıt  YOK")
                    break
                
                else:
                    contine = False
                    driver.refresh()  
                    print("REFRESHING");time.sleep(10) 
    
    driver.quit()
    TeleMessage("Daten Tamam")

        
            














