import scraper, bot, analyzer
import re


def main():

    # extract token
    with open('../token.token', 'r') as f:
        token = f.read().strip('\n')

    # initialize Bot with token
    home_bot = bot.Bot(token)

    offset = None

    # loop for continuous functioning
    while True:
        try:
            last_upd = home_bot.get_last_update(offset)
            if last_upd:
                offset = last_upd.get_offset() + 1
                msg_text = last_upd.get_text()
                links = re.findall('http[s]?://\S*', msg_text)
                site_text = scraper.Scraper(links[0]).scrape()
                # scraper.Scraper(links[0]).scrape() returns str if an error occurs
                if type(site_text) == list:
                    text_stats = analyzer.Analyzer(site_text).get_stats()
                    # analyzer.Analyzer(site_text).get_stats() returns str if an error occurs
                    if type(text_stats) == dict:
                        response = ''
                        for key, value in text_stats.items():
                            response += (key+': '+str(value)+'\n')
                        home_bot.send_text(chat_id=last_upd.get_chat_id(), text=response)
                    else:
                        home_bot.send_text(chat_id=last_upd.get_chat_id(), text=text_stats)
                else:
                    home_bot.send_text(chat_id=last_upd.get_chat_id(), text=site_text)
        except IndexError:
            pass
        except KeyboardInterrupt:
            exit()


# run only from console
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
