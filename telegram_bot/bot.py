import requests as rq
import functools
import datetime
import json
import os

def logger(func):
    """
        opens/creates log.log file to store function log:
        enter/exit time, exceptions, if any occured
    """
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        with open('../log.log', 'a') as f:
            # enter-log
            f.write(str(datetime.datetime.now()) +
                    ' entering: ' +
                    str(func.__name__) +
                    ' from ' + str(func.__module__) + '\n')
            try:
                result = func(*args, **kwargs)
            # exception-log
            except Exception as exp:
                f.write('! an EXCEPTION occurred: ' + str(exp) + '\n')
                result = None
            # exit-log
            f.write('exiting: ' + str(func.__name__)+'\n')
        return result

    return wrapped


class Upd:

    """ a container class for server response json-objects
        with methods for information extraction"""

    def __init__(self, content):
        self.content = content['result'][0]
        if not os.path.exists('../contents'):
            os.makedirs('../contents')
        with open('../contents/' + str(self.content['update_id']) + '.json', 'w') as f:
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

    """ allows interaction between functional modules and user, server"""

    base_url = 'https://api.telegram.org/bot'

    @logger
    def __init__(self, token):
        """ API-authorisation with a token"""
        self.token = token
        try:
            with open('../log.log', 'x') as f:
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
            print(params)
        upd = Upd(rq.get(self.assemble_url(method_name), params).json())
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
