import discord
import asyncio
from itemdict import valuestoitems
import re

def statstrim(trim, champ):
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

    embed = discord.Embed(color=0xCC00CC)
    embed.add_field(name="Armor", value=armor, inline=True)
    embed.add_field(name="Armor Per Level", value=armorLvl, inline=True)
    embed.add_field(name="Magic Resist", value=mrBase, inline=True)
    embed.add_field(name="Magic Resist Per Level", value=mrPerLvl, inline=True)
    embed.add_field(name="Health", value=health, inline=True)
    embed.add_field(name="Health Per Level", value=healthLv, inline=True)
    embed.add_field(name="Health Regen", value=hpregLvl, inline=True)
    embed.add_field(name="Health Regen Per Level", value=hpregLvl, inline=True)
    embed.add_field(name="Mana", value=mana, inline=True)
    embed.add_field(name="Mana Per Level", value=mpPerLvl, inline=True)
    embed.add_field(name="Mana Regen", value=mpRegen, inline=True)
    embed.add_field(name="Mana Regen Per Level", value=mpRegLvl, inline=True)
    embed.add_field(name="Movement Speed", value=moveSpd, inline=True)
    embed.add_field(name="Attack Speed Offset", value=asOffset, inline=True)
    embed.add_field(name="Attack Range", value=atkRange, inline=True)
    embed.add_field(name="Attack Damage", value=adBase, inline=True)
    embed.add_field(name="Attack Damage Per Level", value=adPerLvl, inline=True)
    embed.set_author(name='Stats', icon_url="http://ddragon.leagueoflegends.com/cdn/6.23.1/img/champion/" + champ.capitalize() + ".png")

    return embed

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

    embed = discord.Embed(color=0xCC00CC, title=item['name']) 
    if buildsinto:
        embed.add_field(name="Costs", value=item['cost'])
        embed.add_field(name="Sells for", value=item['sell'])
        embed.add_field(name="Builds into", value=buildsinto)
        embed.add_field(name="Description", value=item['desc'])
    else:
        embed.add_field(name="Costs", value=item['cost'])
        embed.add_field(name="Sells for", value=item['sell'])
        embed.add_field(name="Description", value=item['desc'])

    return embed
