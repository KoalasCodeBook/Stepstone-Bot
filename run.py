from app import *

while True:
    myChoose = UserInput()

    if myChoose == "quit" :
        break
    if myChoose == "start":
        setup_SQLTable() #setup sql tables
        setup_postleitszahl() #setup postleitzahlen

        searchLinks = targetSearchLinks() #read search-links
        TeleMessage("***********\n\n\nErst ziehe ich die Links")
        for link,number in searchLinks:
            try:
                get_link(link)
            except ValueError as E:
                TeleMessage("Done with Link-{}\n{}".format(number,E))
            except Exception as E:
                TeleMessage("Failed to get Link-{}\n{}".format(number,E))
                SET.FAILEDLINKS.append(link) #not finished


        TeleMessage("Bin fertig mit den links. Das sind alle Links die es nicht zu ende geschaft haben:")
        if SET.FAILEDLINKS:
            for link in SET.FAILEDLINKS:
                TeleMessage(str(link))
                time.sleep(1)
        else:
            TeleMessage("Keine Links. Hmmm.. keine Fehler passiert. Da stimmt etwas nicht")
        

        newLength,oldLength = duplicated_bombok() 
        unWantedCompany = unWantedBitches()
        TeleMessage("Filtere alle doppelten raus\nAlte Laenge: {}\nNeue Laenge: {}\n\nNich erwünschte Firmen-Artikel:{}".format(oldLength,newLength,unWantedCompany))

        cursor = sqlite3.connect(SET.MAIN_DATABASE).cursor()
        links = [x for x in cursor.execute("SELECT * FROM links").fetchall()]

        splited = splitList(links,SET.SplitTHREAD)
        
        l1 = list(splited["thread-1"])
        l2 = list(splited["thread-2"])
        l3 = list(splited["thread-3"])
         
        thread1 = Thread(target=get_data, args=(l1,))
        thread2 = Thread(target=get_data, args=(l2,))
        thread3 = Thread(target=get_data, args=(l3,))

        TeleMessage("Jetzt starte ich mit get_data")

        thread1.start()
        thread2.start()
        thread3.start()

        thread1.join()
        thread2.join()
        thread3.join()

        TeleMessage("Ich bin mit den Daten fertig...\n") 

    elif myChoose == "start link":
        setup_SQLTable() #setup sql tables
        setup_postleitszahl() #setup postleitzahlen

        searchLinks = targetSearchLinks() #read search-links
        TeleMessage("***********\n\n\nErst ziehe ich die Links")
        for link,number in searchLinks:
            try:
                get_link(link)
            except ValueError as E:
                TeleMessage("Done with Link-{}\n{}".format(number,E))
            except Exception as E:
                TeleMessage("Failed to get Link-{}\n{}".format(number,E))
                SET.FAILEDLINKS.append(link) #not finished


        TeleMessage("Bin fertig mit den links. Das sind alle Links die es nicht zu ende geschaft haben:")
        if SET.FAILEDLINKS:
            for link in SET.FAILEDLINKS:
                TeleMessage(str(link))
                time.sleep(1)
        else:
            TeleMessage("Keine Links. Hmmm.. keine Fehler passiert. Da stimmt etwas nicht")
        

        newLength,oldLength = duplicated_bombok() 
        unWantedCompany = unWantedBitches()
        TeleMessage("Filtere alle doppelten raus\nAlte Laenge: {}\nNeue Laenge: {}\n\nNich erwünschte Firmen-Artikel:{}".format(oldLength,newLength,unWantedCompany))


        break
    elif myChoose == "start data":
        cursor = sqlite3.connect(SET.MAIN_DATABASE).cursor()
        links = [x for x in cursor.execute("SELECT * FROM links").fetchall()]

        splited = splitList(links,SET.SplitTHREAD)
        
        l1 = list(splited["thread-1"])
        l2 = list(splited["thread-2"])
        l3 = list(splited["thread-3"])
         
        thread1 = Thread(target=get_data, args=(l1,))
        thread2 = Thread(target=get_data, args=(l2,))
        thread3 = Thread(target=get_data, args=(l3,))

        thread1.start()
        thread2.start()
        thread3.start()

        thread1.join()
        thread2.join()
        thread3.join()

        TeleMessage("Ich bin mit den Daten fertig...\n") 
        



 

    elif myChoose == "email":
        sendMail("why are u gay?")
    elif myChoose == "telegram":
        start = time.time()
        teleTHREAD = Thread(target=TeleMessage,args=["Fehler  muss sein"])
        teleTHREAD.start()   
    elif myChoose == "sql":
        setup_postleitszahl()
        setup_SQLTable()
    elif myChoose == "duplicated":
        print(duplicated_bombok())
    elif myChoose == "unwanted":
        print("unwanted company counter: {} ".format(unWantedBitches())) 
    elif myChoose == "just print":
        print(targetSearchLinks())
        


"""

teile die liste in THREAD (3)...
speicher die links in THREAD (3) verschiede .files/temp/ortner/datein

starte auf einmal THEAD(3) verschiedene Opera Tabs wo links durch gehen
alle gezogenen datein im jeweiligen ortner abspeichern

wenn im (thread) process ein fehler entstehnt geht email an Timo...

wenn einer dieser processe fertig wird erstelle csv aus der sql datei


"""
