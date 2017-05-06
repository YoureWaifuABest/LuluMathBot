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


def findchampid(champ):
    global param
    champ = champ.capitalize()

    if not os.path.exists('data/championID'):
        r = requests.get('https://na1.api.riotgames.com/lol/static-data/v3/champions', params=param)
        if r.status_code != 200:
            return -1
        f = open('data/championID', 'w')
        f.write(r.text)
        f.close()
    elif time.time() - os.path.getmtime('data/championID') > 3600:
        r = requests.get('https://na1.api.riotgames.com/lol/static-data/v3/champions', params=param)
        if r.status_code != 200:
            return -1
        f = open('data/championID', 'w')
        f.write(r.text)
        f.close()

    f = open('data/championID', 'r')

    out = find_values(champ.capitalize(), f.read())
    f.close()

    return out[0]['id']

def findchamp(champ, cid, find):
    global param
    champ = champ.capitalize()
    param['champData'] = find

    if not os.path.exists('data/' + champ + find):
        r = requests.get('https://na1.api.riotgames.com/lol/static-data/v3/champions/' + cid, params=param)
        if r.status_code != 200:
            return -1
        f = open('data/' + champ + find, 'w')
        f.write(r.text)
        f.close()
    elif time.time() - os.path.getmtime('data/' + champ + find) > 7200:
        r = requests.get('https://na1.api.riotgames.com/lol/static-data/v3/champions/' + cid, params=param)
        if r.status_code != 200:
            return -1
        f = open('data/' + champ + find, 'w')
        f.write(r.text)
        f.close()

    f = open('data/' + champ + find, 'r')
    text = find_values(find, f.read())
    f.close()

    return text
           
def finditem(item):
    global param
    
    param['itemData'] = 'all'
    if not os.path.exists('data/' + str(item)):
        r = requests.get('https://na1.api.riotgames.com/lol/static-data/v3/items/' + str(item), params=param)
        if r.status_code != 200:
            return -1
        f = open('data/' + str(item), 'w')
        f.write(r.text)
        f.close()
    elif time.time() - os.path.getmtime('data/' + str(item)) > 7200:
        r = requests.get('https://na1.api.riotgames.com/lol/static-data/v3/items/' + str(item), params=param)
        if r.status_code != 200:
            return -1
        f = open('data/' + str(item), 'w')
        f.write(r.text)
        f.close()

    f = open('data/' + str(item), 'r')

    new = json.loads(f.read())
    f.close()

    return new

def finditemval(item):
    global param

    if not os.path.exists('data/items'):
        r = requests.get('https://na1.api.riotgames.com/lol/static-data/v3/items/', params=param)
        if r.status_code != 200:
            return -1
        f = open('data/items', 'w')
        f.write(r.text)
        f.close()
    elif time.time() - os.path.getmtime('data/' + str(item)) > 115200:
        r = requests.get('https://na1.api.riotgames.com/lol/static-data/v3/items/', params=param)
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

    if not os.path.exists('data/currentchallenger'):
        r = requests.get('https://na1.api.riotgames.com/lol/league/v3/challengerleagues/by-queue/RANKED_SOLO_5x5', params=param)
        if r.status_code != 200:
            return -1
        f = open('data/currentchallenger', 'w') 
        f.write(r.text)
        f.close()
    elif time.time() - os.path.getmtime('data/currentchallenger') > 1800:
        r = requests.get('https://na1.api.riotgames.com/lol/league/v3/challengerleagues/by-queue/RANKED_SOLO_5x5', params=param)
        if r.status_code != 200:
            return -1
        f = open('data/currentchallenger', 'w')
        f.write(r.text)
        f.close()

    f = open('data/currentchallenger', 'r')

    text = find_values('entries', f.read())
    f.close()

    output = sorted(text[0], key=lambda lp: lp['leaguePoints'], reverse=True)

    return output

def findid(player):
    global param

    r = requests.get('https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/' + player, params=param)

    if r.status_code != 200:
        return -1

    text = find_values(player.lower(), r.text)

    return text[0]['id']

def findwinrate(playerid):
    global param
    param['season'] = "SEASON2017"

    r = requests.get('https://na.api.pvp.net/api/lol/na/v1.3/stats/by-summoner/' + str(playerid) + '/summary', params=param)

    text = find_values("playerStatSummaries", r.text)

    for i in text[0]:
        if i['playerStatSummaryType'] == 'RankedSolo5x5':
            break

    if not i['wins'] and not i['losses']:
        return -1

    winrate = i['wins'] / (i['wins'] + i['losses'])

    return winrate

def findrank(playerid):
    global param

    r = requests.get('https://na.api.pvp.net/api/lol/na/v2.5/league/by-summoner/' + str(playerid) + '/entry', params=param)

    out = find_values(str(playerid), r.text)

    try:
        out[0][0]
    except IndexError:
        return -1

    return out[0][0]

def findchampstats(cid, playerid):
    global param

    param['season'] = "SEASON2017"

    r = requests.get('https://na.api.pvp.net/api/lol/na/v1.3/stats/by-summoner/' + str(playerid) + '/ranked', params=param)

    out = find_values("champions", r.text)

    for i in out[0]:
        if i['id'] == cid:
            out = i

    return out
