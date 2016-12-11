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
    item['name'] = str(trim['name'])
    item['desc'] = str(trim['description'])

    item['desc'] = item['desc'].replace('<br>', '\n')
    item['desc'] = re.sub("(<.*?>)", '', item['desc']) 
    embed = discord.Embed(color=0xCC00CC, title=item['name']) 
    try:
        item['into'] = trim['into']
    except KeyError: 
        embed.add_field(name="Costs", value=item['cost'])
        embed.add_field(name="Sells for", value=item['sell'])
        embed.add_field(name="Description", value=item['desc'], inline=False)
        return embed

    i = 0
    buildsinto = ''
    while i < len(item['into']):
        if i < len(item['into'])-1:
            buildsinto += str(valuestoitems[str(item['into'][i])]) + ',' + ' '
        else:
            buildsinto += str(valuestoitems[str(item['into'][i])])
        i += 1

    if buildsinto:
        embed.add_field(name="Costs", value=item['cost'])
        embed.add_field(name="Sells for", value=item['sell'])
        embed.add_field(name="Builds into", value=buildsinto, inline=False)
        embed.add_field(name="Description", value=item['desc'], inline=False)

    return embed

def rankedtrim(trim):
    if trim == -1:
        embed = discord.Embed(color=0x1100CC, title="ERROR", description="Summoner has no ranked games played!")
    else: 
        embed = discord.Embed(color=0xCC00CC, title=trim['entries'][0]['playerOrTeamName'], description=trim['name'])
        embed.add_field(name="Rank", value=trim['tier'] + ' ' + trim['entries'][0]['division'])
        embed.add_field(name="LP", value=trim['entries'][0]['leaguePoints'])
        embed.add_field(name="Win/Loss", value=str(trim['entries'][0]['wins']) + '/' + str(trim['entries'][0]['losses']))

        try:
            trim['entries'][0]['miniSeries']
            mseries = True
        except KeyError:
            mseries = False
        
        if mseries:
            embed.add_field(name="Series", value="Wins needed: " + str(trim['entries'][0]['miniSeries']['target']) + '\n' + \
                                                 "Current Win / Loss: " + str(trim['entries'][0]['miniSeries']['wins']) + '/' + \
                                                 str(trim['entries'][0]['miniSeries']['losses']), inline=False)

        string = ''
        if trim['entries'][0]['isVeteran'] == True:
            string += "Veteran | "
        if trim['entries'][0]['isFreshBlood'] == True:
            string += "Fresh Blood | "
        if trim['entries'][0]['isHotStreak'] == True:
            string += "Hot Streak "

        # shouldn't need to make this check. clean up
        if trim['entries'][0]['isVeteran'] == True or trim['entries'][0]['isFreshBlood'] == True or trim['entries'][0]['isHotStreak'] == True:
            embed.add_field(name="Emblems:", value=string)

    return embed
