# Telegram Bot
This simple Telegram-API (https://core.telegram.org/bots/api) based bot was developed as a part of my term project for "Programming basics for data science" course at HSE.
There are several telegram-API libraries already written for this purpose https://core.telegram.org/bots/samples. 
However, no such libraries were used in this projects, because of its educational purpose.
## What can this bot do?
After receiving a url, the bot sends a user statistics on the site text.
It includes word, sentences count, readability index and top-10 frequent words.
## How does it work?
The bot listens (long polling) to https://api.telegram.org/bot<token>/getUpdates. Users messages appear there as json-objects. After receiving an update the Bot handles it as an Upd-class object. From this object the Bot exctracts conversation address and message text (potentially containing the link, a user wants to explore). The Bot looks for a http(s)-link in the message. If there is no link, the Bot ignores such a message. If a link is found, it is redirected to the Scraper. The Scraper scrapes text from the website (currently from <p\>-tags only). If it fails to do so, the user receives a message with information about an occured error. If the text has been scrapped successfully, it's passed to the Analyzer. It counts words, sentences and characters and some other text stats.
  
All the received Updates are stored in the "contents" folder. All Bot-methods calls are logged in the log.log file by logger function.
