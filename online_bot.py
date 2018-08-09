import requests
import time
import json
import argparse

parser = argparse.ArgumentParser(description='Trigger when someone from list became online')
parser.add_argument('ids', 
            metavar='ids_list',
            nargs='+',
            type=int,
            help='vk ids for trigger')
parser.add_argument('--access_token',
            action='store',
            dest='access_token',
            help='Access token to use vkApi')
args = parser.parse_args()

SLEEP_TIME = 5
api = 'https://api.vk.com/method/'
method = 'users.get'
fields = '?lang=ru' + '&v=5.8' + '&fields=online'
if not args.access_token:
    raise Exception('Need access_token (use --access_token=*your token*)')
access_token = '&access_token=' + args.access_token
ids = args.ids
online_ids = set()
fields += '&user_ids='
for q in ids:
    fields += str(q) + ','
fields = fields[:-1]
url = api + method + fields + access_token
r = requests.get(url)
humans = {}
for human in r.json()['response']:
    humans[human['id']] = human['first_name'] + ' ' + human['last_name']
    if human['online']:
        online_ids.add(human['id'])
print('looking for:', humans)
print('now online:', [humans[id_] for id_ in online_ids])
while 1:
    r = requests.get(url)
    new_online_ids = set()
    for human in r.json()['response']:
        if human['online']:
            new_online_ids.add(human['id'])
    new_ids = new_online_ids.difference(online_ids)
    if new_ids:
        print('\a', time.ctime(), 'new online:', [humans[online_id] for online_id in new_ids])
    online_ids = new_online_ids.copy()
    # print(time.ctime(), 'online:', online_ids)
    time.sleep(SLEEP_TIME)