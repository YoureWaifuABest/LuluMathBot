# LuluMathBot todo list
These are the general things I plan to add.

## High Priority
- [ ] General clean-up
- [ ] Rewrite arg system
- [x] Make arguments order-independent (in some cases)
- [x] Add stats at a certain level to !champ stats
- [ ] Add more Riot API Features
	- [x] Replace current ddragon input with static API
	- [p] Specific profile lookup other than just winrate
- [ ] Rewrite formatting.py
- [x] Improve !item search
	- [x] Improve parsing of colloq
	- [x] Return possible values with an incomplete string
		- [x] Ex: `!item hextech` returns the names: hextech gunblade, glp, protobelt, etc.
		- [x] If there is only one possible value, return that value.
- [ ] Use some sort of databse instead of just writing to files
  - [ ] Research into various DBs
	- [ ] Find Python bindings

## Mid Priority
- [ ] Add more features
	- [ ] Masteries
	- [ ] Runes
- [ ] Add spells to !champ
