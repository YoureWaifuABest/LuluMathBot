import json

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

    return find_values(find, json_repr)
           
def finditem(item, patch):
    json_repr = open('ddragon/' + patch +'/data/en_US/item.json').read()

    output = find_values('data', json_repr)

    new = output[0][item]

    return new

def finditemval(item, patch):
    json_repr = open('ddragon/' + patch +'/data/en_US/item.json').read()

    output = find_values('data', json_repr)

    keys = output[0]

    indexx = {}
    for i in keys:
        indexx[i] = output[0][i]['colloq']

    return indexx

#print (finditemval('whatever', '6.22.1'))

#print(skinstrim(findchamp('Lulu', 'skins', '6.22.1')))

#out = findchamp('Lulu', 'spells', '6.22.1')


