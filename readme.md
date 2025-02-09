To use my Bot, you have to create a Telegram-Group and add you're own Telegram-Bot(telegram bot project available in repository). Now you can change in Setting.py the API_KEY and CHANNEL_ID of the Bot. 
If you don't want to use Telegram as Error or Status check, u can send your self e-mails by Gmail. Repalce TeleMessage() function with sendMail() in functions.py. Don't forget to change the Sender ID and the Passwort. 

First of all, u have to start with Console> python run.py
It will wait for an answer. U can run the process or test some features...


"email" or "telegram" will send a test message.

"sql" will create the needed database and tables.

"duplicated" will delete all duplicated links.(u must have runned before)

"unwanted" will delete all links of non desired companies.
