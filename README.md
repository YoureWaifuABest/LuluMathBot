# LuluMathBot
Discord bot to do basic League of Legends related math and output League of Legends related stats. 

## No longer maintained; rewrote in Go and moved to https://github.com/kuwuda/Go-LuluMathBot

## Current features:
1. Lethality, armor, and magic resistance calculations
2. Basic damage calculator (damage * resist essentially)
3. Outputs Champion specific data (stats, lore, etc.)
4. Item information lookup
5. Print current challenger players
6. Can clear the channel
  + This requires appropriate permissions
  - Included because I've been too lazy to make a second bot
7. Will respond to certain phrases (for fun)
8. Some other fun phrases (8ball, rng)

## Dependencies
1. Python3.5+
2. discord.py
3. requests

## Installation
1. `git clone [this repo]`
2. Add your bot's token to bottoken.py
3. Add your Riot API token to apitoken.py
4. Launch it and it'll probably work.

### Disclaimer
LuluMathBot isn't endorsed by Riot Games and doesn't reflect the views or opinions of Riot Games
or anyone officially involved in producing or managing League of Legends.
League of Legends and Riot Games are trademarks or registered trademarks of Riot Games, Inc. League of Legends © Riot Games, Inc.
