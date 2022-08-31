import app.settings as SET
from  app.functions import *

from selenium import webdriver
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup

import sqlite3,time

def get_link(getLink_link:str):
    getLink_Jobs_ClassName = SET.getLink_Jobs_ClassName
    getLink_Jobs_CompanyName = SET.getLink_Jobs_CompanyName
    getLink_xpath_nextPage_href = SET.getLink_xpath_nextPage_href
                    
    con = sqlite3.connect(SET.MAIN_DATABASE)
    cursor = con.cursor()
    
    X,Y = ScreenSize()

    driver = webdriver.Firefox("") 
    driver.set_window_position(0, 0)
    driver.set_window_size(int(X*0.33), int(Y*0.66))

    driver.get(getLink_link)

    time.sleep(10)
    driver.refresh()
    time.sleep(5)

    #cockies to eat ...Es muss 'Alles akzeptieren' heißen.      
    driver.find_element(by=By.XPATH, value= "//span[text()='Alles akzeptieren']").click()

    while True:    
        html_icerigi = driver.page_source
        soup = BeautifulSoup(html_icerigi, 'lxml')

        JobsList = soup.find_all('div',{"class":getLink_Jobs_ClassName} )
        
        if len(JobsList) == 0:
            FatherDIV = [i for i in soup.find_all('div') if len(i) == 25]

            if FatherDIV:     
                for TargetDIV in FatherDIV[0]:
                    getLink_Jobs_ClassName = " ".join([c for c in TargetDIV.get("class")])
                    break 
                
            else:
                getLink_Jobs_ClassName = ""
                driver.quit()
                raise TypeError("Error: Keine 25 Jobs gefunden. Ich versuche es mit dem naechsten link.")
                            
            JobsList = soup.find_all('div',{"class":getLink_Jobs_ClassName} ) 




        #Looping alle links in der offenen Seite
        for Job in JobsList:
            JobArticle = Job.find("div").find('article')
            elementsA = JobArticle.find_all('a')

            companyName = Job.find("div",{"class":getLink_Jobs_CompanyName})
            
            if companyName:
                companyName = companyName.text
            else:
                companyName = ""

            if len(elementsA) == 3:
                href1= elementsA[0]['href'] #Andere Jobs von der selben Firma
                href2= elementsA[1]['href'] #link der Stelle
                href3= elementsA[2]['href'] #link der Stelle
            else:                
                href1 = "\n".join([link['href'] for link in elementsA])
                cursor.execute("INSERT INTO failedLinks VALUES(?,?)",(href1,""));con.commit()    #Speichert die nicht passenden links
                continue

            cursor.execute("INSERT INTO links VALUES(?,?,?,?)",(href1,href2,href3,companyName));con.commit()    #Speichert das link wenns passt
 
        href = ""
        xpath = getLink_xpath_nextPage_href
        element1 = driver.find_element(by=By.XPATH, value=xpath)
        if element1:
            href = element1.get_attribute("href")
            if href == None:
                driver.quit()
                raise ValueError("Es geht nicht mehr weiter. Ich fange mit dem naechsten link an..")
        else:
            driver.quit()
            raise TypeError("Ich kann wegen einem Fehler nicht auf die naechste seite")

        driver.get(href)   
        




      
    