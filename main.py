import discord
import asyncio
from random import randint
from formatting import statstrim, skinstrim, itemstrim
from getargs   import getargs
from getdigits import getdigits
from findvalues import findchamp, finditem
from itemdict import itemstovalues, colloq

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))

    if message.content.startswith('!help'):
        await client.send_message(message.channel, '`Commands: !help, !reduction, !lethality, !damage, !champ, !item, !source, !license`\n' + 
                                                   'Add help as an argument to any command to get help with it.')
    if message.content.startswith('!clear'):
        if message.channel.permissions_for(message.author).manage_messages:
            await client.purge_from(message.channel, limit=500)
        else:
            await client.send_message(message.channel, 'You do not have permission to use this command!')

    if message.content.lower().startswith('that tasted'):
        await client.send_message(message.channel, 'purple!')

    if message.content.startswith('LULU'):
        if str(message.author) == 'sam sam#7213':
            await client.send_message(message.channel, 'sam pls')

    if message.content.lower().startswith('hello!!!'):
        await client.send_message(message.channel, 'Pleased to meet you!')

    if message.content.lower().startswith('!random'):
        argc, argv = getargs(message.content)

        try:
            float(argv[1])
        except:
            return -1

        try: 
            float(argv[2])
        except:
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

        if item == 'what is the best color?':
            await client.send_message(message.channel, 'Purple!')
            return -1

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

    if message.content.startswith('!source'):
        await client.send_message(message.channel, 'Github: https://github.com/YoureWaifuABest/LuluMathBot')

    if message.content.startswith('!license'):
        await client.send_message(message.channel, '{}'.format(open('LICENSE', 'r').read()))

    if message.content.startswith('!item'):
        argc, argv = getargs(message.content)

        try:
            argv[1]
        except:
            await client.send_message(message.channel, '**ERROR: No arguments present!**\n' +
                                                       '`See !item help`')
            return -1

        if argv[1].lower() == 'help':
            await client.send_message(message.channel, 'Prints information on a given item.\n' + 
                                                       'Usage: !item item')
            return 0
        
        i = 1
        item = ''
        while i < argc+1:
            if i == argc:
                item += argv[i].lower()
            else:
                item += argv[i].lower() + ' '
            i += 1

        try:
            value = itemstovalues[item]
        except KeyError:
            try:
                value = list(colloq.keys())[list(colloq.values()).index(';' + item)]
            except ValueError:
                await client.send_message(message.channel, '**ERROR: Item does not exist!**\n' +
                                                           'Please input the full name of the item, or an abbreviation (roa)\n' +
                                                           'If the abbreviation does not work, use the full name instead.')
                return -1

        output = finditem(value, '6.22.1')

        new_out = itemstrim(output)

        await client.send_message(message.channel, '{}'.format(new_out))

    if message.content.startswith('!champ'):
        argc, argv = getargs(message.content)

        i = 0
        while i != len(argv):
            argv[i] = argv[i].lower()
            i += 1

        try:
            argv[1]
        except:
            await client.send_message(message.channel, '**ERROR: No arguments present!**\n' +
                                                       '`Usage: !champ help`')
            return -1

        if argv[1] == 'help':
            await client.send_message(message.channel, 'Prints data on a certain champion.\n' +
                                                       '`Usage: !champ data champion options`\n' +
                                                       'Champion name needs to be capitalized, data needs to be lowercase, options need to be lowercase\n' +
                                                       'Options vary. `!champ data champion help` to list options.\n' +
                                                       '**Possible values for data:**\n' +
                                                       '`lore, blurb, stats, skins, tags`') #spells passive
            return 0
        
        output = findchamp(argv[2], argv[1], '6.22.1')

        if argv[1] == 'lore' or argv[1] == 'blurb':
            try:
                argv[3]
            except IndexError:
                new_out = output[0].replace('<br>', '\n')
                await client.send_message(message.channel, '**{}: **\n {}'.format(argv[1], new_out[:1000]))
                if argv[1] == 'lore':
                    await client.send_message(message.channel, '{}'.format(new_out[1000:]))
                return 0
            if argv[3] == 'help':
                await client.send_message(message.channel, 'No possible options!\n')
                return 0
            else:
                await client.send_message(message.channel, 'Too many arguments!')
                return -1
        elif argv[1] == 'stats':
            try:
                argv[3]
            except IndexError:
                argv.append('all')
            if argv[3] == 'all':
                new_out = statstrim(output)
            elif argv[3] == 'help':
                await client.send_message(message.channel, '`Usage: !champ stats champion options`\n' +
                                                           'Where options are: help (prints this help message), ' +
                                                           'all (prints keys + values), keys (prints just keys), or a certain key. Defaults to all.')
                return 0
            elif argv[3] == 'keys':
                new_out = output[0].keys()
            else:
                try:
                    new_out = output[0][argv[3]]
                except KeyError:
                    await client.send_message(message.channel, '**ERROR: Not an available key.**\n' +
                                                               'Please use `!champ stats champion keys` to list the keys')
                    return -1
            await client.send_message(message.channel, '**{}: **\n```{}```'.format(argv[1], new_out))
        elif argv[1] == 'spells':
            try:
                argv[3]
            except IndexError:
                argv.append('all')
            if argv[3] == 'all':
                a = 0
                for i in output[0]:
                    await client.send_message(message.channel, '{}'.format(output[0][a].items()))
                    a += 1
            elif argv[3] == 'help':
                await client.send_message(message.channel, '`Usage: !champ spells champion options`\n' +
                                                           'Where options are: help (prints this help message,) ' +
                                                           'all (prints info on all the spells), q,w,e,r (prints respective ability). Defaults to all.')
                return 0
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
            try:
                argv[3]
            except IndexError:
                new_out = skinstrim(output)
                await client.send_message(message.channel, '**Skins:**\n `{}`'.format(new_out))
                return 0
            if argv[3] == 'help':
                await client.send_message(message.channel, 'No possible options!\n')
                return 0
            else:
                await client.send_message(message.channel, 'Too many arguments!')
                return -1 
        elif argv[1] == 'tags':
            try:
                argv[3]
            except IndexError:
                new_out = '**Tags:**\n`'
                for i in output[0]:
                    new_out += i + ' '
                new_out += '`'
                await client.send_message(message.channel, '{}'.format(new_out))
            if argv[3] == 'help':
                await client.send_message(message.channel, 'No possible options!\n')
                return 0
            else:
                await client.send_message(message.channel, 'Too many arguments!')
                return -1 
        elif argv[1] == 'passive':
            await client.send_message(message.channel, '{}'.format(output[0]))

            #new_out = output
            #await client.send_message(message.channel, '**{}: **\n {}'.format(argv[2], new_out[0][1].items()))
    
    if message.content.startswith('!damage'):
        argc, argv = getargs(message.content)

        if argv[1] == 'help':
            await client.send_message(message.channel, 'Prints the damage dealt after reductions\n' +
                                                       'Usage: !damage base resist')
            return 0

        if argc < 2:
            await client.send_message(message.channel, '**ERROR: Too few arguments.**\n' +
                                                       'See !damage help')
            return -1
        
        if argc > 2:
            await client.send_message(message.channel, '**ERROR: Too many arguments.**\n' +
                                                       'See !damage help')
            return -1

        try:
            float(argv[1])
        except ValueError:
            await client.send_message(message.channel, '**ERROR: Entered value is not a number!**\n Syntax: !damage base resist')
            return -1

        try:
            float(argv[2])
        except ValueError:
            await client.send_message(message.channel, '**ERROR: Entered value is not a number!**\n Syntax: !damage base resist')
            return -1

        damage = float(argv[1]) * float(argv[2])
        await client.send_message(message.channel, 'Damage: __{}__'.format(damage))

    if message.content.startswith('!reduction'):
        # Remove command from processing of message (just get arguments)
        argc, argv = getargs(message.content)

        if argc < 1:
            await client.send_message(message.channel, '**ERROR: Too few arguments.**\n' +
                                                       'See !reduction help')
            return -1
        elif argc > 1:
            await client.send_message(message.channel, '**ERROR: Too many arguments.**\n' +
                                                       'See !reduction help')
            return -1

        # Print help message
        if argv[1] == 'help':
            await client.send_message(message.channel, 'Prints the value damage is multiplied by with a given amount of armor / mr\n' +
                                                       'Usage: !reduction number')
            return 0

        # Ensure value entered is at least a floating point number
        try: 
            float(argv[1])
        except ValueError:
            await client.send_message(message.channel, '**ERROR: Entered value is not a number!**\n Syntax: !reduction number')
            return -1

        if float(argv[1]) < 0:
            reduction = 2 - (100/(100-float(argv[1])))
        elif float(argv[1]) >= 0:
            reduction = 100/(100+float(argv[1]))

        await client.send_message(message.channel, 'Reduction Multiplier: __{}__'.format(reduction))

    if message.content.startswith('!lethality'):
        # Remove command from processing of message (just get arguments)
        # args = message.content[len('!lethality'):].strip()
        argc, argv = getargs(message.content)

        if argv[1] == "help":
            await client.send_message(message.channel, 'Calculates actual armor pen a target receives\n' +
                                                       '```syntax: !lethality number level\n' +
                                                       'or      !lethality table number```' +
                                                       'Adding table prints a table of values from level 1 to 18')
            return 0
        elif argv[1] == "table":
            # Ensure value entered is at least a floating point number
            if argc < 2:
                await client.send_message(message.channel, '**ERROR: Too few arguments!**\n Syntax: !lethality table number')
                return -1
            elif argc > 2:
                await client.send_message(message.channel, '**ERROR: Too many arguments!**\n' + 'Syntax: !lethality table number')
                return -1
            if argv[2] == "help":
                await client.send_message(message.channel, 'Prints a table of actual armor pen a target receives, from levels ' +
                                                           '1 to 18\n' +
                                                           'Usage: !lethality table number') 
                return 0
            try: 
                float(argv[2])
            except ValueError:
                await client.send_message(message.channel, '**ERROR: Entered value is not a number!**\n Syntax: !lethality table number')
                return -1
            
            stri  = '```\n'
            stri += 'Level  Actual Penetration\n'
            i = 1
            while i <= 18:
                lethality = 0.4 * float(argv[2]) + ((0.6 * float(argv[2]) * i)/18)
                blanks = 5 + 1/getdigits(i)
                stri += str(i)
                stri += ' ' * int(blanks)
                stri += str(lethality)
                stri += '\n'
                i += 1
            stri += '```'
            await client.send_message(message.channel, stri)

            return 0

        try:
            argv[2]
        except:
            await client.send_message(message.channel, '**ERROR: Too few arguments!**\n Syntax: !lethality number level')
            return -1 

        # Ensure value entered is at least a floating point number
        try: 
            float(argv[1])
        except ValueError:
            await client.send_message(message.channel, '**ERROR: Entered value is not a number!**\nSyntax: !lethality number level')
            return -1

        try: 
           float(argv[2])
        except ValueError:
            await client.send_message(message.channel, '**ERROR: Entered value is not a number!**\nSyntax: !lethality number level')
            return -1

        lethality = 0.4 * float(argv[1]) + ((0.6 * float(argv[1]) * float(argv[2]))/18)
        await client.send_message(message.channel, 'Effective Armor Pen: __{}__'.format(lethality))

from bottoken import token

client.run(token)
