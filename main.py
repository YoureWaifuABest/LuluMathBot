import discord
import asyncio
import re
import datetime
import os
import time
from random import randint
from formatting import skinstrim, itemstrim, statstrim
from getargs   import getargs
from getdigits import getdigits
from findvalues import findchamp, finditem, challenger, findid, findwinrate
from itemdict import itemstovalues, valuestoitems, colloq

client = discord.Client()
patch = "6.23.1"
#store = ''

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    #### Fun Stuff ####
    if message.content.lower().startswith('that tasted'):
        await client.send_message(message.channel, 'purple!')

    if message.content.startswith('LULU'):
        if str(message.author) == 'sam sam#7213':
            await client.send_message(message.channel, 'sam pls')

    if message.content.lower().startswith('hello!!!'):
        await client.send_message(message.channel, 'Pleased to meet you!')

    if message.content.lower().startswith('!random'):
        argc, argv = getargs(message.content)

        if argv[1] == 'help':
            embed = discord.Embed(color=0xCC00CC, title="Help", description="Finds a random whole number between two values")
            embed.add_field(name="Usage", value="`!random number number`")
            await client.send_message(message.channel, embed=embed)
            return 0

        try:
            float(argv[1])
        except:
            embed = discord.Embed(color=0xFF0022, title="ERROR", description="Argument not a number!")
            embed.add_field(name="See", value="`!random help`")
            await client.send_message(message.channel, embed=embed)
            return -1

        try: 
            float(argv[2])
        except:
            embed = discord.Embed(color=0xFF0022, title="ERROR", description="Argument not a number!")
            embed.add_field(name="See", value="!random help")
            await client.send_message(message.channel, embed=embed)
            return -1

        rand = randint(int(argv[1]), int(argv[2]))
        rand = str(rand)

        await client.send_message(message.channel, '{}'.format(rand))

    if message.content.lower().startswith('!8ball'):
        argc, argv = getargs(message.content)
        
        i = 1
        item = ''
        while i < argc+1:
            if i == argc:
                item += argv[i].lower()
            else:
                item += argv[i].lower() + ' '
            i += 1

        rand = randint(1,5)
        if rand == 1:
            await client.send_message(message.channel, 'Answer is no.')
        elif rand == 2:
            await client.send_message(message.channel, 'Absolutely.')
        elif rand == 3:
            await client.send_message(message.channel, 'Answer is unclear')
        elif rand == 4:
            await client.send_message(message.channel, 'What?')
        elif rand == 5:
            await client.send_message(message.channel, 'Undoubtedly.')
        else:
            await client.send_message(message.channel, 'Definitely not.')

    #### Administrative Stuff ####
    if message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))

    if message.content.startswith('!help'):
        embed = discord.Embed(color=0xCC00CC)
        embed.add_field(name="Commands", value="!help, !reduction, !lethality, !damage, !champ, !item, !source, !license, !winrate, !challenger", inline=True)
        embed.set_footer(text="Add help as an argument to any command to get help with it.")
        await client.send_message(message.channel, embed=embed)

    if message.content.startswith('!source'):
        await client.send_message(message.channel, 'Github: https://github.com/YoureWaifuABest/LuluMathBot')

    if message.content.startswith('!license'):
        embed = discord.Embed(color=0xCC00CC, title="Unlicense", description=open('LICENSE', 'r').read())
        await client.send_message(message.channel, embed=embed)
        embed = discord.Embed(color=0xCC00CC, title="Attribution", description="LuluMathBot isn't endorsed by Riot Games and" +
                                                                               "doesn't reflect the views or opinions of Riot Games or anyone " +
                                                                               "officially involved in producing or managing League of Legends. " +
                                                                               "League of Legends and Riot Games are trademarks or registered " +
                                                                               "trademarks of Riot Games, Inc. League of Legends © Riot Games, " +
                                                                               "Inc.")
        await client.send_message(message.channel, embed=embed)

    if message.content.startswith('!clear'):
        if message.channel.permissions_for(message.author).manage_messages:
            await client.purge_from(message.channel, limit=500)
        else:
            await client.send_message(message.channel, 'You do not have permission to use this command!')

    #### Math ####
    if message.content.startswith('!damage'):
        argc, argv = getargs(message.content)

        try:
            argv[1]
        except:
            embed = discord.Embed(color=0xFF0022, title="ERROR", description="Too few arguments\nSee `!damage help`")
            await client.send_message(message.channel, embed=embed)
            return -1

        if argv[1] == 'help':
            embed = discord.Embed(color=0xCC00CC, title="Damage", description="Prints the damage dealt after reductions")
            embed.add_field(name="Usage", value="`!damage base resist`")
            await client.send_message(message.channel, embed=embed)
            return 0

        if argc < 2:
            embed = discord.Embed(color=0xFF0022, title="ERROR", description="Too few arguments\nSee `!damage help`")
            await client.send_message(message.channel, embed=embed)
            return -1
        
        if argc > 2:
            embed = discord.Embed(color=0xFF0022, title="ERROR", description="Too many arguments\nSee `!damage help`")
            await client.send_message(message.channel, embed=embed)
            return -1

        try:
            float(argv[1])
        except ValueError:
            embed = discord.Embed(color=0xFF0022, title="ERROR", description="Endered value is not a number")
            embed.add_field(name="Syntax", value="`!damage base resist`")
            await client.send_message(message.channel, embed=embed)
            return -1

        try:
            float(argv[2])
        except ValueError:
            embed = discord.Embed(color=0xFF0022, title="ERROR", description="Endered value is not a number")
            embed.add_field(name="Syntax", value="`!damage base resist`")
            await client.send_message(message.channel, embed=embed)
            return -1

        damage = float(argv[1]) * float(argv[2])
        embed = discord.Embed(title="Damage", color=0xCC00CC, description="__" + str(damage) + "__")
        await client.send_message(message.channel, embed=embed)

    if message.content.startswith('!reduction'):
        # Remove command from processing of message (just get arguments)
        argc, argv = getargs(message.content)

        if argc < 1:
            embed = discord.Embed(color=0xFF0022, title="ERROR", description="Too few arguments\nSee `!reduction help`")
            await client.send_message(message.channel, embed=embed)
            return -1
        elif argc > 1:
            embed = discord.Embed(color=0xFF0022, title="ERROR", description="Too many arguments\nSee `!reduction help`")
            await client.send_message(message.channel, embed=embed)
            return -1

        # Print help message
        if argv[1] == 'help':
            embed = discord.Embed(color=0xCC00CC, title="Help", description="Prints the value damage is multiplied by with a given amount of armor / mr")
            embed.add_field(name="Usage", value="`!reduction number`")
            await client.send_message(message.channel, embed=embed)
            return 0

        # Ensure value entered is at least a floating point number
        try: 
            float(argv[1])
        except ValueError:
            embed = discord.Embed(color=0xFF0022, title="ERROR", description="Entered value is not a number")
            embed.add_field(name="Syntax", value="`!reduction number`")
            await client.send_message(message.channel, embed=embed)
            return -1

        if float(argv[1]) < 0:
            reduction = 2 - (100/(100-float(argv[1])))
        elif float(argv[1]) >= 0:
            reduction = 100/(100+float(argv[1]))

        embed = discord.Embed(color=0xCC00CC)
        embed.add_field(name="Reduction Multiplier:", value="__" + str(reduction) + "__")
        await client.send_message(message.channel, embed=embed)

    if message.content.startswith('!lethality'):
        argc, argv = getargs(message.content)

        try:
            argv[1]
        except:
            embed = discord.Embed(color=0xFF0022, title="ERROR", description="Too few arguments")
            embed.add_field(name="See", value="`!lethality help`")
            await client.send_message(message.channel, embed=embed)
            return -1

        if argv[1] == "help":
            embed = discord.Embed(color=0xCC00CC, title="Help", description="Calculates actual armor pen a target receives")
            embed.add_field(name="Syntax", value="`!lethality number level`\n or `!lethality table number`")
            embed.set_footer(text="Adding table prints a table of values from level 1 to 18")
            await client.send_message(message.channel, embed=embed)
            return 0
        elif argv[1] == "table":
            # Ensure value entered is at least a floating point number
            if argc < 2:
                embed = discord.Embed(color=0xFF0022, title="ERROR", description="Too few arguments")
                embed.add_field(name="Syntax", value="`!lethality table number`")
                await client.send_message(message.channel, embed=embed)
                return -1
            elif argc > 2:
                embed = discord.Embed(color=0xFF0022, title="ERROR", description="Too many arguments")
                embed.add_field(name="Syntax", value="`!lethality table number`")
                await client.send_message(message.channel, embed=embed)
                return -1
            if argv[2] == "help":
                embed = discord.Embed(color=0xCC00CC, title="Help", description="Prints a table of actual armor pen a target receives, from levels 1 to 18")
                embed.add_field(name="Usage", value="`!lethality table number`")
                await client.send_message(message.channel, embed=embed)
                return 0
            try: 
                float(argv[2])
            except ValueError:
                embed = discord.Embed(color=0xFF0022, title="ERROR", description="Entered value is not a number")
                embed.add_field(name="Syntax", value="`!lethality table number`")
                await client.send_message(message.channel, embed=embed)
                return -1
            
            i = 1
            stri = ''
            strl = ''
            while i <= 18:
                lethality = 0.4 * float(argv[2]) + ((0.6 * float(argv[2]) * i)/18)
                stri += str(i) + '\n'
                strl += str(lethality) + '\n'
                i += 1
            embed = discord.Embed(color=0xCC00CC)
            embed.add_field(name="Level", value=stri, inline=True)
            embed.add_field(name="Actual Penetration", value=strl, inline=True)
            await client.send_message(message.channel, embed=embed)

            return 0

        try:
            argv[2]
        except:
            embed = discord.Embed(color=0xFF0022, title="ERROR", description="Too few arguments")
            embed.add_field(name="Syntax", value="`!lethality number level`")
            await client.send_message(message.channel, embed=embed)
            return -1 

        # Ensure value entered is at least a floating point number
        try: 
            float(argv[1])
        except ValueError:
            embed = discord.Embed(color=0xFF0022, title="ERROR", description="Entered value is not a number")
            embed.add_field(name="Syntax", value="`!lethality number level`")
            await client.send_message(message.channel, embed=embed)
            return -1

        try: 
           float(argv[2])
        except ValueError:
            embed = discord.Embed(color=0xFF0022, title="ERROR", description="Entered value is not a number")
            embed.add_field(name="Syntax", value="`!lethality number level`")
            await client.send_message(message.channel, embed=embed)
            return -1

        lethality = 0.4 * float(argv[1]) + ((0.6 * float(argv[1]) * float(argv[2]))/18)
        embed = discord.Embed(color=0xCC00CC)
        embed.add_field(name="Effective Armor Pen", value="__" + str(lethality) + "__")
        await client.send_message(message.channel, embed=embed)

    #### Data ####
    if message.content.startswith('!item'):
        argc, argv = getargs(message.content.lower())

        try:
            argv[1]
        except:
            embed = discord.Embed(color=0xFF0022, title="ERROR", description="No arguments present")
            embed.add_field(name="See", value="`!item help`")
            await client.send_message(message.channel, embed=embed)
            return -1

        if argv[1] == 'help':
            embed = discord.Embed(color=0xCC00CC, title="Help", description="Prints information on a given item")
            embed.add_field(name="Usage", value="`!item item`")
            await client.send_message(message.channel, embed=embed)
            return 0
        
        i = 1
        item = ''
        while i < argc+1:
            if i == argc:
                item += argv[i]
            else:
                item += argv[i] + ' '
            i += 1

        possible = [s for s in itemstovalues if re.search('{}'.format(item), s) is not None]
        inv_map  = {v: k for k, v in colloq.items()}
        c = 0
        colloqz  = [c for c in inv_map       if re.search('{}'.format(item), c) is not None]

        i = 0
        colloqval = []
        while i != len(colloqz):
            colloqval.append(inv_map[colloqz[i]])
            i += 1

        i = 0
        while i != len(colloqval):
            possible.append(valuestoitems[colloqval[i]])
            i += 1

        if len(possible) == 1:
            item = possible[0]
            value = itemstovalues[item]
            output = finditem(value, patch)
            new_out = itemstrim(output)
            await client.send_message(message.channel, embed=new_out)
        elif len(possible) == 0:
            embed = discord.Embed(color=0xFF0022, title="ERROR", description="Item not found!\nPlease input an actual item.")
            await client.send_message(message.channel, embed=embed)
        else:
            string = ''
            c = 0
            for i in possible:
                if c < (len(possible)-1):
                    string += i + ', '
                else:
                    string += i +'.'
                c += 1
            embed = discord.Embed(color=0xCC00CC, title="Value not found!")
            embed.add_field(name="Possible Values", value=string)
            await client.send_message(message.channel, embed=embed)

    if message.content.startswith('!champ'):
        argc, argv = getargs(message.content.lower())

        try:
            argv[1]
        except:
            embed = discord.Embed(color=0xFF0022, title="ERROR", description="No arguments present!")
            embed.add_field(name="Usage", value="`!champ help`")
            await client.send_message(message.channel, embed=embed)
            return -1

        if argv[1] == 'help':
            embed = discord.Embed(color=0xCC00CC, title="Help", description="Prints data on a certain champion")
            embed.add_field(name="Usage", value="`!champ data champion options`\n Options vary. `!champ data champion help` to list options.", inline=False)
            embed.add_field(name="Possible Values for Data", value="`lore, blurb, stats, skins, tags`") # spells passive
            await client.send_message(message.channel, embed=embed) 
            return 0
        
        if argv[2] != 'help':
            try:
                output = findchamp(argv[2], argv[1], patch)
            except FileNotFoundError:
                embed = discord.Embed(color=0xFF0022, title="ERROR", description="No such champion!")
                embed.add_field(name="Usage", value="`!champ help`")
                await client.send_message(message.channel, embed=embed)
                return -1

        if argv[1] == 'lore' or argv[1] == 'blurb':
            if argv[2] == 'help':
                await client.send_message(message.channel, 'No possible options!\n')
                return 0
            try:
                argv[3]
            except IndexError:
                new_out = output[0].replace('<br>', '\n')
                embed = discord.Embed(color=0xCC00CC, title="Lore", description=new_out[:1000])
                await client.send_message(message.channel, embed=embed)
                if argv[1] == 'lore':
                    embed = discord.Embed(color=0xCC00CC, description=new_out[1000:])
                    await client.send_message(message.channel, embed=embed)
                return 0
            if argv[3] == 'help':
                await client.send_message(message.channel, 'No possible options!\n')
                return 0
            else:
                embed = discord.Embed(color=0xFF0022, title="ERROR", description="Too many arguments!")
                embed.add_field(name="Usage", value="`!champ lore champ`")
                await client.send_message(message.channel, embed=embed)
                return -1
        elif argv[1] == 'stats':
            if argv[2] == 'help':
                embed = discord.Embed(color=0xCC00CC)
                embed.add_field(name="Usage", value="`!champ stats champion options`", inline=False)
                embed.add_field(name="Options", value="help (prints this help message), all (prints keys + values), keys (prints just keys), or a certain key." +
                                                      " Defaults to all.")
                await client.send_message(message.channel, embed=embed)
                return 0

            try:
                argv[3]
            except IndexError:
                argv.append('all')
            if argv[3] == 'help':
                embed = discord.Embed(color=0xCC00CC)
                embed.add_field(name="Usage", value="`!champ stats champion options`", inline=False)
                embed.add_field(name="Options", value="help (prints this help message), all (prints keys + values), keys (prints just keys), or a certain key." +
                                                      " Defaults to all.")
                await client.send_message(message.channel, embed=embed)
                return 0
            elif argv[3] == 'all':
                new_out = statstrim(output, argv[2])
            elif argv[3] == 'keys':
                # Format this later, since it's super ugly
                new_out = discord.Embed(color=0xCC00CC, title="Keys", description=str(output[0].keys()))
            else:
                try:
                    new_out = discord.Embed(color=0xCC00CC, title=argv[3].capitalize(), description=str(output[0][argv[3]]))
                except KeyError:
                    embed = discord.Embed(color=0xFF0022, title="ERROR", description="Not an available key")
                    embed.add_field(name="Please use", value="`!champ stats champion keys` to list possible keys")
                    await client.send_message(message.channel, embed=embed)
                    return -1
            await client.send_message(message.channel, embed=new_out)
        elif argv[1] == 'spells':
            if argv[2] == 'help':
                embed = discord.Embed(color=0xCC00CC)
                embed.add_field(name="Usage", value="`!champ spells champion options`", inline=False)
                embed.add_field(name="Options", value="`all (prints info on all spells), q,w,e,r.` Defaults to all")
                await client.send_message(message.channel, embed=embed)
                return 0
            try:
                argv[3]
            except IndexError:
                argv.append('all')
            if argv[3] == 'help':
                embed = discord.Embed(color=0xCC00CC)
                embed.add_field(name="Usage", value="`!champ spells champion options`", inline=False)
                embed.add_field(name="Options", value="`all (prints info on all spells), q,w,e,r.` Defaults to all")
                await client.send_message(message.channel, embed=embed)
                return 0
            if argv[3] == 'all':
                a = 0
                for i in output[0]:
                    await client.send_message(message.channel, '{}'.format(output[0][a].items()))
                    a += 1
            elif argv[3] == 'q':
                new_out = str(output[0][0].items())
                await client.send_message(message.channel, '{}'.format(new_out))
            elif argv[3] == 'w':
                await client.send_message(message.channel, '{}'.format(output[0][1].items()))
            elif argv[3] == 'e':
                await client.send_message(message.channel, '{}'.format(output[0][2].items()))
            elif argv[3] == 'r':
                await client.send_message(message.channel, '{}'.format(output[0][3].items()))
            else:
                await client.send_message(message.channel, '**ERROR: Invalid input!**\n' +
                                                           'See `!champ spells champion help` for help')
                return -1
        elif argv[1] == 'skins':
            if argv[2] == 'help':
                await client.send_message(message.channel, 'No possible options!\n')
                return 0
            try:
                argv[3]
            except IndexError:
                new_out = discord.Embed(color=0xCC00CC, title="Skins" , description=skinstrim(output))
                await client.send_message(message.channel, embed=new_out)
                return 0
            if argv[3] == 'help':
                await client.send_message(message.channel, 'No possible options!\n')
                return 0
            else:
                embed = discord.Embed(color=0xFF0022, title="ERROR", description="Too many arguments")
                embed.add_field(name="Usage", value="`!champ skins champion`")
                await client.send_message(message.channel, embed=embed)
                return -1 
        elif argv[1] == 'tags':
            if argv[2] == 'help':
                await client.send_message(message.channel, 'No possible options!\n')
                return 0
            try:
                argv[3]
            except IndexError:
                new_out = ''
                for i in output[0]:
                    new_out += i + ' '
                new_out += ''
                embed  = discord.Embed(title="Tags", color=0xCC00CC, description=new_out)
                await client.send_message(message.channel, embed=embed)
                return 0
            if argv[3] == 'help':
                await client.send_message(message.channel, 'No possible options!\n')
                return 0
            else:
                embed = discord.Embed(color=0xFF0022, title="ERROR", description="Too many arguments")
                embed.add_field(name="Usage", value="`!champ tags champion`")
                await client.send_message(message.channel, embed=embed)

    if message.content.lower().startswith('!challenger'):
        if 'help' in message.content.lower():
            embed = discord.Embed(color=0xCC00CC, title='Help', description='Prints the top 99 challenger players')
            embed.add_field(name="Usage", value="`!challenger`", inline=False)
            await client.send_message(message.channel, embed=embed)
            return 0

        members = challenger()

        w = 1
        position = ''
        name     = ''
        lp       = ''
        wl       = ''
        for i in members:
            if w < 100:
                position += str(w) + '.\n'
                name     += i['playerOrTeamName'] + '\n'
                lp       += str(i['leaguePoints']) + '\n'
            else:
                break
            w += 1

        embed = discord.Embed(color=0xDAA520, title="Top 99 Challenger")
        embed.add_field(name="Position", value=position)
        embed.add_field(name="Summoner", value=name)
        embed.add_field(name="LP",       value=lp)
        embed.set_footer(text="Data retreived on: " + time.strftime("%d-%m-%Y %H:%M:%S", time.localtime(os.path.getmtime('currentchallenger'))))

        await client.send_message(message.channel, embed=embed)

    if message.content.lower().startswith("!winrate"):
        argc, argv = getargs(message.content)

        try:
            argv[1]
        except IndexError:
            embed = discord.Embed(color=0xFF0022, title="ERROR", description="Too few arguments")
            embed.add_field(name="Usage", value="`!winrate player`")
            await client.send_message(message.channel, embed=embed)
            return -1

        # Not sure what to do if the player's name is help.
        if argv[1] == 'help':
            embed = discord.Embed(color=0xCC00CC, title='Help', description='Prints the winrate of a player')
            embed.add_field(name="Usage", value="`!winrate player`", inline=False)
            await client.send_message(message.channel, embed=embed)
            return 0

        if not re.match("^[0-9\\{a-zA-z} _\\.]+$", argv[1]):
            embed = discord.Embed(color=0xFF0022, title="ERROR", description="Character not allowed in League of Legends name.")
            embed.add_field(name="Possible Values", value="`Numbers 0-9, letters a-z (capitalized or uncapitalized), underscores, and periods.`")
            await client.send_message(message.channel, embed=embed)
            return -1

        playerid = findid(argv[1])
        if playerid == -1:
            embed = discord.Embed(color=0xFF0022, title="ERROR", description="Summoner does not exist!")
            await client.send_message(message.channel, embed=embed)
            return -1

        if findwinrate(playerid) == -1:
            embed = discord.Embed(color=0x1100CC, title="ERROR", description="User has no ranked games played!")
            await client.send_message(message.channel, embed=embed)
            return -1


        embed = discord.Embed(color=0xCC00CC, title="Winrate in Ranked", description=str(findwinrate(playerid)))
        embed.set_footer(text="Data retreived on: " + datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
        await client.send_message(message.channel, embed=embed)

from bottoken import token
client.run(token)
