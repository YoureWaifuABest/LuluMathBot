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
    champion = champion.capitalize()

    json_repr = open('ddragon/' + patch + '/data/en_US/champion/' + champion + '.json').read()

    f = find_values(find, json_repr)
    json_repr.close()

    return  f
           
def finditem(item, patch):
    json_repr = open('ddragon/' + patch +'/data/en_US/item.json').read()

    output = find_values('data', json_repr)
    json_repr.close()

    new = output[0][item]

    return new

def finditemval(item, patch):
    json_repr = open('ddragon/' + patch +'/data/en_US/item.json').read()

    output = find_values('data', json_repr)
    json_repr.close()

    keys = output[0]

    indexx = {}
    for i in keys:
        indexx[i] = output[0][i]['colloq']

    return indexx

def challenger():
    global param
    param['type'] = 'RANKED_SOLO_5x5'

    if not os.path.exists('currentchallenger'):
        r = requests.get('https://na.api.pvp.net/api/lol/na/v2.5/league/challenger', params=param)
        if r.status_code != 200:
            return -1
        f = open('currentchallenger', 'w') 
        f.write(r.text)
        f.close()
    elif time.time() - os.path.getmtime('currentchallenger') > 1800:
        r = requests.get('https://na.api.pvp.net/api/lol/na/v2.5/league/challenger', params=param)
        if r.status_code != 200:
            return -1
        f = open('currentchallenger', 'w')
        f.write(r.text)
        f.close()

    f = open('currentchallenger', 'r')

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
