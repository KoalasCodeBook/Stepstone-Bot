To use my Bot, you have to create a Telegram-Group and add you're own Telegram-Bot(use my other project from repository). Now you can change in Setting.py the API_KEY and CHANNEL_ID of the Bot. 
If you don't want to use Telegram, u can send your self e-mails by Gmail. Repalce TeleMessage() function with sendMail() in functions.py. Don't forget to change the Sender ID and the Passwort. 

First of all, u have to start run.py
It will wait for an answer. U can run the process or test some features...


"email" or "telegram" will send a try message.

"sql" will create the needed database and tables.

"duplicated" will delete all duplicated links.(u must have started before)

"unwanted" will delete all links of non desired companies.
