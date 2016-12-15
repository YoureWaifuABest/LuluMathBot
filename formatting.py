import discord
import asyncio
from itemdict import valuestoitems
import re

def statstrim(trim, champ, level):
    armor    = trim[0]['armor']
    armorLvl = trim[0]['armorperlevel']
    mrBase   = trim[0]['spellblock']
    mrPerLvl = trim[0]['spellblockperlevel']
    health   = trim[0]['hp']
    healthLv = trim[0]['hpperlevel']
    hpregen  = trim[0]['hpregen']
    hpregLvl = trim[0]['hpregenperlevel']
    mana     = trim[0]['mp']
    mpPerLvl = trim[0]['mpperlevel']
    mpRegen  = trim[0]['mpregen']
    mpRegLvl = trim[0]['mpregenperlevel']
    moveSpd  = trim[0]['movespeed']
    asOffset = trim[0]['attackspeedoffset']
    asPerLvl = trim[0]['attackspeedperlevel']
    atkRange = trim[0]['attackrange']
    adBase   = trim[0]['attackdamage']
    adPerLvl = trim[0]['attackdamageperlevel']

    atspd = 0.625 / (1 + asOffset)

    embed = discord.Embed(color=0xCC00CC)
    if level == 'all':
        embed.add_field(name="Armor", value=armor, inline=True)
        embed.add_field(name="Armor Growth", value=armorLvl, inline=True)
        embed.add_field(name="Magic Resist", value=mrBase, inline=True)
        embed.add_field(name="Magic Resist Growth", value=mrPerLvl, inline=True)
        embed.add_field(name="Health", value=health, inline=True)
        embed.add_field(name="Health Growth", value=healthLv, inline=True)
        embed.add_field(name="Health Regen", value=hpregLvl, inline=True)
        embed.add_field(name="Health Regen Growth", value=hpregLvl, inline=True)
        embed.add_field(name="Mana", value=mana, inline=True)
        embed.add_field(name="Mana Growth", value=mpPerLvl, inline=True)
        embed.add_field(name="Mana Regen", value=mpRegen, inline=True)
        embed.add_field(name="Mana Regen Growth", value=mpRegLvl, inline=True)
        embed.add_field(name="Movement Speed", value=moveSpd, inline=True)
        embed.add_field(name="Attack Speed Offset", value=asOffset, inline=True)
        embed.add_field(name="Base Attack Speed", value=atspd, inline=True)
        embed.add_field(name="Attack Speed Per Level", value=asPerLvl, inline=True)
        embed.add_field(name="Attack Range", value=atkRange, inline=True)
        embed.add_field(name="Attack Damage", value=adBase, inline=True)
        embed.add_field(name="Attack Damage Growth", value=adPerLvl, inline=True)
    else:
        armor   = statlvl(armor,   armorLvl, int(level))
        mres    = statlvl(mrBase,  mrPerLvl, int(level))
        health  = statlvl(health,  healthLv, int(level)) 
        hpregen = statlvl(hpregen, hpregLvl, int(level))
        mana    = statlvl(mana,    mpPerLvl, int(level))
        mpRegen = statlvl(mpRegen, mpRegLvl, int(level))
        ad      = statlvl(adBase,  adPerLvl, int(level))
        atspdin = statlvl(0,       asPerLvl, int(level))

        embed.add_field(name="Armor", value=armor, inline=True)
        embed.add_field(name="Magic Resist", value=mres)
        embed.add_field(name="Health", value=health)
        embed.add_field(name="Health Regen", value=hpregen)
        embed.add_field(name="Mana", value=mana)
        embed.add_field(name="Mana Regen", value=mpRegen)
        embed.add_field(name="Attack Speed", value=str(atspd) + ' + ' + str(atspdin) + '%')
        embed.add_field(name="Attack Damage", value=ad)

    embed.set_author(name='Stats', icon_url="http://ddragon.leagueoflegends.com/cdn/6.23.1/img/champion/" + champ.capitalize() + ".png") 
    return embed

def statlvl(base, growth, level):
    return base + (growth * (level-1) * (.685+(.0175 * level)))


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
