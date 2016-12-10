import json
import os
import time
import requests
from apikey import api_key

param = {'api_key': api_key}

def find_values(id, json_repr):
    results = []

    def _decode_dict(a_dict):
        try: results.append(a_dict[id])
        except KeyError: pass
        return a_dict

    json.loads(json_repr, object_hook=_decode_dict)
    return results

def findchamp(champion, find, patch):
    global param
    champion = champion.capitalize()

    if not os.path.exists('data/championID'):
        r = requests.get('https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion', params=param)
        if r.status_code != 200:
            return -1
        f = open('data/championID', 'w')
        f.write(r.text)
        f.close()
    elif time.time() - os.path.getmtime('championID') > 7200:
        r = requests.get('https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion', params=param)
        if r.status_code != 200:
            return -1
        f = open('data/championID', 'w')
        f.write(r.text)
        f.close()

    f = open('data/championID', 'r')
    text = find_values('data', f.read())
    cid  = str(text[0][champion]['id'])
    f.close()

    if not os.path.exists('data/' + champion + find):
        param['champData'] = find
        r = requests.get('https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion/' + cid, params=param)
        if r.status_code != 200:
            return -1
        f = open('data/' + champion + find, 'w')
        f.write(r.text)
        f.close()
    elif time.time() - os.path.getmtime('data/' + champion + find) > 7200:
        param['champData'] = find
        r = requests.get('https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion/' + cid, params=param)
        if r.status_code != 200:
            return -1
        f = open('data' + champion + find, 'w')
        f.write(r.text)
        f.close()

    f = open('data/' + champion + find, 'r')
    text = find_values(find, f.read())
    f.close()

    return text
           
def finditem(item, patch):
    global param
    
    param['itemData'] = 'all'
    if not os.path.exists('data/' + str(item)):
        r = requests.get('https://global.api.pvp.net/api/lol/static-data/na/v1.2/item/' + str(item), params=param)
        if r.status_code != 200:
            return -1
        f = open('data/' + str(item), 'w')
        f.write(r.text)
        f.close()
    elif time.time() - os.path.getmtime('data/' + str(item)) > 7200:
        r = requests.get('https://global.api.pvp.net/api/lol/static-data/na/v1.2/item/' + str(item), params=param)
        if r.status_code != 200:
            return -1
        f = open('data/' + str(item), 'w')
        f.write(r.text)
        f.close()

    f = open('data/' + str(item), 'r')

    new = json.loads(f.read())
    f.close()

    return new

def finditemval(item, patch):
    global param

    if not os.path.exists('data/items'):
        r = requests.get('https://global.api.pvp.net/api/lol/static-data/na/v1.2/item', params=param)
        if r.status_code != 200:
            return -1
        f = open('data/items', 'w')
        f.write(r.text)
        f.close()
    elif time.time() - os.path.getmtime('data/' + str(item)) > 115200:
        r = requests.get('https://global.api.pvp.net/api/lol/static-data/na/v1.2/item', params=param)
        if r.status_code != 200:
            return -1
        f = open('data/items', 'w')
        f.write(r.text)
        f.close()

    f = open('data/items', 'r')

    output = find_values('data', f.read())
    keys = output[0]

    indexx = {}
    for i in keys:
        indexx[i] = output[0][i]['colloq']

    return indexx

def challenger():
    global param
    param['type'] = 'RANKED_SOLO_5x5'

    if not os.path.exists('data/currentchallenger'):
        r = requests.get('https://na.api.pvp.net/api/lol/na/v2.5/league/challenger', params=param)
        if r.status_code != 200:
            return -1
        f = open('data/currentchallenger', 'w') 
        f.write(r.text)
        f.close()
    elif time.time() - os.path.getmtime('data/currentchallenger') > 1800:
        r = requests.get('https://na.api.pvp.net/api/lol/na/v2.5/league/challenger', params=param)
        if r.status_code != 200:
            return -1
        f = open('currentchallenger', 'w')
        f.write(r.text)
        f.close()

    f = open('data/currentchallenger', 'r')

    text = find_values('entries', f.read())
    f.close()

    output = sorted(text[0], key=lambda lp: lp['leaguePoints'], reverse=True)

    return output

def findid(player):
    global param

    r = requests.get('https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/' + player, params=param)

    if r.status_code != 200:
        return -1

    text = find_values(player.lower(), r.text)

    return text[0]['id']

def findwinrate(playerid):
    global param
    param['season'] = "SEASON2016"

    r = requests.get('https://na.api.pvp.net/api/lol/na/v1.3/stats/by-summoner/' + str(playerid) + '/summary', params=param)

    text = find_values("playerStatSummaries", r.text)

    for i in text[0]:
        if i['playerStatSummaryType'] == 'RankedSolo5x5':
            break

    if not i['wins'] and not i['losses']:
        return -1

    winrate = i['wins'] / (i['wins'] + i['losses'])

    return winrate
