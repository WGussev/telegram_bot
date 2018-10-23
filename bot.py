import requests as rq
import functools
import datetime
import json
import re
from Scraper import Scraper
from Analyzer import Analyzer


def logger(func):
    
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        with open('log.log', 'a') as f:
            f.write(str(datetime.datetime.now()) +
                    ' entering: ' +
                    str(func.__name__) +
                    ' from ' + str(func.__module__) + '\n')
            # how can I extract classname for a method?
            try:
                print('!  ', func.__name__)
                result = func(*args, **kwargs)
            except Exception as exp:
                f.write('! an EXCEPTION occurred: ' + str(exp) + '\n')
                result=None
            f.write('exiting: ' + str(func.__name__)+'\n')
        return result

    return wrapped


class Upd:

    def __init__(self, content):
        self.content = content['result'][0]
        with open('./contents/' + str(self.content['update_id']) + '.json', 'w') as f:
            json.dump(self.content, f)

    def get_offset(self):
        return self.content['update_id']

    def get_chat_id(self):
        return self.content['message']['chat']['id']

    def get_file_id(self):
        if self.content['message']['document']['file_id']:
            return self.content['message']['document']['file_id']
        else:
            return False

    def get_text(self):
        return self.content['message']['text']


class Bot:

    base_url = 'https://api.telegram.org/bot'

    def __init__(self, token):
        self.token = token
        try:
            with open('log.log', 'x') as f:
                pass
        except FileExistsError:
            pass

    @logger
    def assemble_url(self, method_name):
        """assembles target url according to a method used"""
        return self.base_url + f'{self.token}/{method_name}'

    @logger
    def get_last_update(self, offset, limit=1, timeout=300):
        """receives updates one-by-one"""
        method_name = 'getUpdates'
        params = {'limit': limit,
                  'timeout': timeout}
        if offset:
            params['offset'] = offset
        upd = Upd(rq.get(self.assemble_url(method_name), params).json())
        print(upd)
        return upd

    @logger
    def send_text(self, chat_id, text):
        """sends text messages"""
        method_name = 'sendMessage'
        params = {'chat_id': chat_id,
                  'text': text}
        msg = rq.post(self.assemble_url(method_name), params)
        return msg

    @logger
    def get_file(self, file_id):
        method_name = 'getFile'
        params = {'file_id': file_id}
        file = rq.get(self.assemble_url(method_name), params)



def main():
    token = #add token here
    home_bot = Bot(token)
    offset = None

    while True:
        try:
            last_upd = home_bot.get_last_update(offset)
            if last_upd:
                offset = last_upd.get_offset() + 1
                msg_text = last_upd.get_text()

                links = re.findall('http[s]?://\S*', msg_text)
                print(links)
                site_text = Scraper(links[0]).scrape()
                print(site_text)
                text_stats = Analyzer(site_text).get_stats()
                print(text_stats)
                response = ''
                for key, value in text_stats.items():
                    response += (key+': '+str(value)+'\n')

                home_bot.send_text(chat_id=last_upd.get_chat_id(), text=response)

                #if last_upd.get_file_id():
                #    home_bot.get_file(last_upd.get_file_id())
        except IndexError:
            pass
        except KeyboardInterrupt:
            exit()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
