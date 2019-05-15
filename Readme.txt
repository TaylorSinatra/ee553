How to run:
	To run the game run gui.py via python3. The game is a combination of graphical interface and terminal output. The terminal output is additional information and is not required to play.
How to play:
		Player Characters:
			The player has four characters, a knight, rogue, wizard, and priest. Each has their own unique stats, color, and a special skill. The knight is the main tank and can smash all enemies for double his attack power. The rogue can backstab all enemies for significant damage and ignore armor. The wizard can destroy 5 columns from the play board at random once per turn. The priest can heal all living allies for 50 health. Each skill has a mana requirement to use it. The player gains mana by destroying the appropriate colored block in the play area.

		Enemy Characters:
			Four enemies are randomly generated and persist until they are killed or the game ends. As the player kills enemies they will become stronger and stronger.

		Play Board:
			The play board consists of 6 color blocks. White blocks have already been destroyed and are "empty". Black blocks cannot be clicked and can only be destroyed by the wizard's wild fire skill. When a player clicks a colored block, it and all blocks connected that are the same color will be destroyed and the player will receive mana for that color character's skill.

		Turns:
			The game is turn based. The player will have 3 clicks to interact with the play board. Clicks are not consumed when using a skill. After the player uses their clicks, the player characters will attack the first living enemy (top down). If any enemies survive, they will attack the players in the same fashion. When all enemies are defeated, a new board and new enemies will be generated. When all player characters are defeated, the game ends.