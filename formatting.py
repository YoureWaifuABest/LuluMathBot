from itemdict import valuestoitems
import re

def statstrim(trim):
    armor    = str(trim[0]['armor'])
    armorLvl = str(trim[0]['armorperlevel'])
    mrBase   = str(trim[0]['spellblock'])
    mrPerLvl = str(trim[0]['spellblockperlevel'])
    health   = str(trim[0]['hp'])
    healthLv = str(trim[0]['hpperlevel'])
    hpregen  = str(trim[0]['hpregen'])
    hpregLvl = str(trim[0]['hpregenperlevel'])
    mana     = str(trim[0]['mp'])
    mpPerLvl = str(trim[0]['mpperlevel'])
    mpRegen  = str(trim[0]['mpregen'])
    mpRegLvl = str(trim[0]['mpregenperlevel'])
    moveSpd  = str(trim[0]['movespeed'])
    asOffset = str(trim[0]['attackspeedoffset'])
    asPerLvl = str(trim[0]['attackspeedperlevel'])
    atkRange = str(trim[0]['attackrange'])
    adBase   = str(trim[0]['attackdamage'])
    adPerLvl = str(trim[0]['attackdamageperlevel'])

    return 'Armor: ' + armor + ' Per Level: ' + armorLvl + '\n' + \
           'Magic Resist: ' + mrBase + ' Per Level: ' +mrPerLvl + '\n' + \
           'Health: ' + health + ' Per Level: ' + healthLv + '\n' + \
           'HP Regen: ' + hpregen + ' Per Level: ' +hpregLvl + '\n' + \
           'Mana: ' + mana + ' Per Level: ' + mpPerLvl + '\n' + \
           'MP Regen: ' + mpRegen + ' Per Level: ' + mpRegLvl + '\n' + \
           'Movement Speed: ' + moveSpd + '\n' + \
           'Attack Speed Offset: ' + asOffset + ' Per Level: ' + asPerLvl + \
           '\n' + \
           'Range: ' + atkRange + '\n' + \
           'Base AD: ' + adBase + ' Per level: ' + adPerLvl

def skinstrim(trim):
    skin = []
    i = 0
    while i < len(trim[0]):
        skin.append(str(trim[0][i]['name']))
        i += 1

    skinstr = str(skin).replace('[', '')
    skinstr = skinstr.replace(']', '')
    skinstr = skinstr.replace("'", '')
    skinstr = skinstr.replace("default", "Default")

    return skinstr

def itemstrim(trim):
    item = {}   
    item['cost'] = str(trim['gold']['total'])
    item['sell'] = str(trim['gold']['sell'])
    item['into'] = trim['into']
    item['name'] = str(trim['name'])
    item['desc'] = str(trim['description'])

    i = 0
    buildsinto = ''
    while i < len(item['into']):
        if i < len(item['into'])-1:
            buildsinto += str(valuestoitems[str(item['into'][i])]) + ',' + ' '
        else:
            buildsinto += str(valuestoitems[str(item['into'][i])])
        i += 1

    item['desc'] = item['desc'].replace('<br>', '\n')
    item['desc'] = re.sub("(<.*?>)", '', item['desc'])

    if buildsinto:
        itemstr = '**' + item['name'] + '**\n```' + \
                  'Costs: ' + item['cost'] + '\n\n' + \
                  'Sells for: ' + item['sell'] + '\n\n' + \
                  'Builds into: ' + buildsinto + '\n\n' + \
                  'Description:\n' + item['desc'] + '```'
    else:
        itemstr = '**' + item['name'] + '**\n```' + \
                  'Costs: ' + item['cost'] + '\n' + \
                  'Sells for: ' + item['sell'] + '\n' + \
                  'Description:\n' + item['desc'] + '```'

    return itemstr
