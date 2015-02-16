# -*- coding: utf-8 -*-

# Copyright (c) 2015 Alexander Teves <alexander.teves@gmail.com>
# Released under the terms of the MIT license

from __future__ import print_function
from httplib2 import Http

import base64
import json
import argparse
import sys


class BasecampApi(object):
    def __init__(self, accountId, username, password):
        self.accountId = accountId
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'BasecampApi ({})'.format(username),
            'Authorization': 'Basic %s' % base64.encodestring('%s:%s' % (username, password))
        }

    def getSubscribers(self, projectId):
        url = 'https://basecamp.com/{}/api/v1/projects/{}/accesses.json'.format(self.accountId, projectId)
        response, content = Http().request(url, 'GET', headers=self.headers)
        if(response['status'] == '200'):
            subscribers = []
            jsonContent = json.loads(content)
            for element in jsonContent:
                subscribers.append(element['id'])
            return subscribers
        else:
            raise Exception('API responded with %s' % response['status'])

    def postMessage(self, projectId, subject, content, subscribers=[]):
        message = json.dumps({'subject': subject, 'content': content, 'subscribers': subscribers})
        url = 'https://basecamp.com/{}/api/v1/projects/{}/messages.json'.format(self.accountId, projectId)
        response, content = Http().request(url, 'POST', body=message, headers=self.headers)
        if(response['status'] == '201'):
            return True
        else:
            raise Exception('API responded with %s' % response['status'])

    def postTodo(self, projectId, todolistId, content):
        todo = json.dumps({'content': content})
        url = 'https://basecamp.com/{}/api/v1/projects/{}/todolists/{}/todos.json'.format(self.accountId, projectId, todolistId)
        response, content = Http().request(url, 'POST', body=todo, headers=self.headers)
        if(response['status'] == '201'):
            return True
        else:
            raise Exception('API responded with %s' % response['status'])


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(
            description='POST to Basecamp\n\n'
            'POST either a message to a project or a todo to a todolist.\n'
            'To POST a todo, simply use the optional argument -t (--todolistid).')
        parser.add_argument('-a', '--accountid', help='ID of the Basecamp account', required=True)
        parser.add_argument('-u', '--username', help='Username (will be an email address)', required=True)
        parser.add_argument('-p', '--password', help='Password for the user', required=True)
        parser.add_argument('-i', '--projectid', help='ID of the project to post to', required=True)
        parser.add_argument('-t', '--todolistid', help='ID of the todolist to post to', required=False)
        parser.add_argument('-s', '--subject', help='Message subject', required=True)
        parser.add_argument('-n', '--notify', help='0: nobody, 1: all subscribers (defaults to 0)', default=0, type=int)
        args = parser.parse_args()
        api = BasecampApi(args.accountid, args.username, args.password)
        print('Enter the message content, end EOT (^D or CTRL + D)')
        content = sys.stdin.read()
        if(args.todolistid):
            api.postTodo(args.projectid, args.todolistid, content)
        else:
            if(args.notify == 0):
                api.postMessage(args.projectid, args.subject, content)
            elif(args.notify == 1):
                subscribers = api.getSubscribers(args.projectid)
                api.postMessage(args.projectid, args.subject, content, subscribers=subscribers)
            else:
                print('Invalid value \'{}\' for subscriber notification parameter'.format(str(args.notify)), file=sys.stderr)
                sys.exit(1)
        sys.exit(0)
    except Exception, e:
        print(e.message, file=sys.stderr)
        sys.exit(1)
