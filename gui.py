from tkinter import *
import board as bd
import characters as char
import numpy as np

clickStart=3
clicks=clickStart
wildFireCharge=True
def buttonCommand(row,column):
	if bd.checkClick(row,column):
		bd.handleClick(row,column)
		updateBoard()
		updateManaLabels()
		global clicks
		clicks-=1
		generateClickLabel()
		if not checkTurnEnd():
			pass
		else:
			#turn over
			char.endRound()
			print ("\n")
			updatePlayerLabels()
			if char.enemyChars[0].isAlive() or char.enemyChars[1].isAlive() or char.enemyChars[2].isAlive() or char.enemyChars[3].isAlive():
				updateEnemyLabels()
			else:
				newLevel()
			if not char.gameOver():
				newTurn()
			else:
				print ("Game over...Thanks for playing!")
				exit()		
	else:
		popupmsg("You cannot click black or white blocks. Try using Wild Fire!")
		pass

def checkTurnEnd():
	if clicks>0:
		return False
	else:
		return True

def newLevel():
	global clicks
	global wildFireCharge
	wildFireCharge=True
	char.level+=1
	char.enemyChars=char.generateEnemies()
	updateEnemyLabels()
	updateLevelLabel()
	bd.board=bd.createBoard()
	updateBoard()
	clicks=clickStart
	updateClickLabel()

def newTurn():
	global clicks
	global wildFireCharge
	wildFireCharge=True
	clicks=clickStart
	updateClickLabel()
	bd.board=bd.createBoard()
	updateBoard()

def generateLevelLabel():
	global labelLeveltext
	labelLeveltext=StringVar()
	labelLeveltext.set("Level: "+str(char.level))
	#labelLevel=Label(root,height=1,width=15,text="Level: "+str(char.level))
	labelLevel=Label(root,height=1,width=15,textvariable=labelLeveltext)
	labelLevel.grid(row=0,column=0,columnspan=100)

def updateLevelLabel():
	labelLeveltext.set("Level: "+str(char.level))

def generateClickLabel():
	global labelClickstext
	labelClickstext=StringVar()
	labelClickstext.set("Clicks remaining: "+str(clicks))
	#labelClicks=Label(root,height=1,width=15,text="Clicks remaining: "+str(clicks))
	labelClicks=Label(root,height=1,width=15,textvariable=labelClickstext)
	labelClicks.grid(row=1,column=0,columnspan=100)

def updateClickLabel():
	labelClickstext.set("Clicks remaining: "+str(clicks))
	
def smashSkill():
	char.playerChars[0].useSkill()
	updateManaLabels()
	if char.enemyChars[0].isAlive() or char.enemyChars[1].isAlive() or char.enemyChars[2].isAlive() or char.enemyChars[3].isAlive():
		updateEnemyLabels()
	else:
		newLevel()

def backstabSkill():
	char.playerChars[1].useSkill()
	updateManaLabels()
	if char.enemyChars[0].isAlive() or char.enemyChars[1].isAlive() or char.enemyChars[2].isAlive() or char.enemyChars[3].isAlive():
		updateEnemyLabels()
	else:
		newLevel()

def wildfireSkill():
	global wildFireCharge
	if wildFireCharge:
		char.playerChars[2].useSkill()
		updateBoard()
		updateManaLabels()
		wildFireCharge=False
	else:
		print ("The wizard needs time to recover!")

def prayerSkill():
	char.playerChars[3].useSkill()
	updateManaLabels()
	updatePlayerLabels()

def generateBoard():
	global frame
	global buttonBoard
	global buttonBoardColors
	frame=Frame(root)
	frame.grid(row=5,column=5,rowspan=15,columnspan=15)
	buttonBoard=(np.full((15,15), None))
	buttonBoardColors=(np.full((15,15), None))
	for x in range(0,bd.boardRows):
		for y in range(0,bd.boardCols):
			buttonBoardColors[x][y]=StringVar()
			buttonBoardColors[x][y].set(colorCodes[bd.board[x][y]])
			buttonBoard[x][y]=Button(frame,height=3,width=3,bg=buttonBoardColors[x][y].get(),command=lambda row=x,column=y:buttonCommand(row,column),highlightthickness=0)
			buttonBoard[x][y].grid(row=bd.boardCols-y-1,column=x)

def updateBoard():
	for x in range(0,bd.boardRows):
		for y in range(0,bd.boardCols):
			buttonBoardColors[x][y]=StringVar()
			buttonBoardColors[x][y].set(colorCodes[bd.board[x][y]])
			buttonBoard[x][y].config(bg=buttonBoardColors[x][y].get())

def generateSkillButtons():
	buttonBackstab=Button(root, height=4,width=9,bg="green4",text=char.playerChars[0].skillName,command=lambda:smashSkill())
	buttonBackstab.grid(row=100,column=5,columnspan=3)
	buttonWildFire=Button(root,height=4,width=9,bg="red2",text=char.playerChars[1].skillName,command=lambda:backstabSkill())
	buttonWildFire.grid(row=100,column=9,columnspan=3)
	buttonPrayer=Button(root,height=4,width=9,bg="yellow2",text=char.playerChars[2].skillName,command=lambda:wildfireSkill())
	buttonPrayer.grid(row=100,column=13,columnspan=3)
	buttonSmash=Button(root,height=4,width=9,bg="royalblue",text=char.playerChars[3].skillName,command=lambda:prayerSkill())
	buttonSmash.grid(row=100,column=17,columnspan=3)
	generateManaLabels()

def generateManaLabels():
	global labelBackstabText
	global labelWildFireText
	global labelPrayerText
	global labelSmashText
	labelBackstabText=StringVar()
	labelWildFireText=StringVar()
	labelPrayerText=StringVar()
	labelSmashText=StringVar()
	labelSmashText.set("Mana/Cost\n"+str(char.playerChars[0].mana)+"/"+str(char.playerChars[0].skillCost))
	labelBackstabText.set("Mana/Cost\n"+str(char.playerChars[1].mana)+"/"+str(char.playerChars[1].skillCost))
	labelWildFireText.set("Mana/Cost\n"+str(char.playerChars[2].mana)+"/"+str(char.playerChars[2].skillCost))
	labelPrayerText.set("Mana/Cost\n"+str(char.playerChars[3].mana)+"/"+str(char.playerChars[3].skillCost))
	labelSmash=Label(root,height=2,width=9,bg="green4",textvariable=labelSmashText)
	labelSmash.grid(row=101,column=5,columnspan=3)
	labelBackstab=Label(root,height=2,width=9,bg="red2",textvariable=labelBackstabText)
	labelBackstab.grid(row=101,column=9,columnspan=3)
	labelWildFire=Label(root,height=2,width=9,bg="yellow2",textvariable=labelWildFireText)
	labelWildFire.grid(row=101,column=13,columnspan=3)
	labelPrayer=Label(root,height=2,width=9,bg="royalblue",textvariable=labelPrayerText)
	labelPrayer.grid(row=101,column=17,columnspan=3)

def updateManaLabels():
	labelSmashText.set("Mana/Cost\n"+str(char.playerChars[0].mana)+"/"+str(char.playerChars[0].skillCost))
	labelBackstabText.set("Mana/Cost\n"+str(char.playerChars[1].mana)+"/"+str(char.playerChars[1].skillCost))
	labelWildFireText.set("Mana/Cost\n"+str(char.playerChars[2].mana)+"/"+str(char.playerChars[2].skillCost))
	labelPrayerText.set("Mana/Cost\n"+str(char.playerChars[3].mana)+"/"+str(char.playerChars[3].skillCost))

def generatePlayerLabels():
	#add armor back in
	global labelRogueText
	global labelWizardText
	global labelPriestText
	global labelKnightText
	labelRogueText=StringVar()
	labelWizardText=StringVar()
	labelPriestText=StringVar()
	labelKnightText=StringVar()
	labelKnightText.set(str(char.playerChars[0].name)+"\nHealth: "+str(char.playerChars[0].lifePoints)+"\nArmor: "+str(char.playerChars[0].armor)+"\nAttack: "+str(char.playerChars[0].attackValue)+"\nArmor Pen: "+str(char.playerChars[0].armorPen))
	labelRogueText.set(str(char.playerChars[1].name)+"\nHealth: "+str(char.playerChars[1].lifePoints)+"\nArmor: "+str(char.playerChars[1].armor)+"\nAttack: "+str(char.playerChars[1].attackValue)+"\nArmor Pen: "+str(char.playerChars[1].armorPen))
	labelWizardText.set(str(char.playerChars[2].name)+"\nHealth: "+str(char.playerChars[2].lifePoints)+"\nArmor: "+str(char.playerChars[2].armor)+"\nAttack: "+str(char.playerChars[2].attackValue)+"\nArmor Pen: "+str(char.playerChars[2].armorPen))
	labelPriestText.set(str(char.playerChars[3].name)+"\nHealth: "+str(char.playerChars[3].lifePoints)+"\nArmor: "+str(char.playerChars[3].armor)+"\nAttack: "+str(char.playerChars[3].attackValue)+"\nArmor Pen: "+str(char.playerChars[3].armorPen))
	labelKnight=Label(root,height=5,width=15,bg="green4",textvariable=labelKnightText)
	labelKnight.grid(row=7,column=0,rowspan=2)
	labelRogue=Label(root,height=5,width=15,bg="red2",textvariable=labelRogueText)
	labelRogue.grid(row=10,column=0,rowspan=2)
	labelWizard=Label(root,height=5,width=15,bg="yellow2",textvariable=labelWizardText)
	labelWizard.grid(row=13,column=0,rowspan=2)
	labelPriest=Label(root,height=5,width=15,bg="royalblue",textvariable=labelPriestText)
	labelPriest.grid(row=16,column=0,rowspan=2)

def updatePlayerLabels():
	labelKnightText.set(str(char.playerChars[0].name)+"\nHealth: "+str(char.playerChars[0].lifePoints)+"\nArmor: "+str(char.playerChars[0].armor)+"\nAttack: "+str(char.playerChars[0].attackValue)+"\nArmor Pen: "+str(char.playerChars[0].armorPen))
	labelRogueText.set(str(char.playerChars[1].name)+"\nHealth: "+str(char.playerChars[1].lifePoints)+"\nArmor: "+str(char.playerChars[1].armor)+"\nAttack: "+str(char.playerChars[1].attackValue)+"\nArmor Pen: "+str(char.playerChars[1].armorPen))
	labelWizardText.set(str(char.playerChars[2].name)+"\nHealth: "+str(char.playerChars[2].lifePoints)+"\nArmor: "+str(char.playerChars[2].armor)+"\nAttack: "+str(char.playerChars[2].attackValue)+"\nArmor Pen: "+str(char.playerChars[2].armorPen))
	labelPriestText.set(str(char.playerChars[3].name)+"\nHealth: "+str(char.playerChars[3].lifePoints)+"\nArmor: "+str(char.playerChars[3].armor)+"\nAttack: "+str(char.playerChars[3].attackValue)+"\nArmor Pen: "+str(char.playerChars[3].armorPen))
	
def generateEnemyLabels():
	#add armor back in
	global labelEnemy1Text
	global labelEnemy2Text
	global labelEnemy3Text
	global labelEnemy4Text
	labelEnemy1Text=StringVar()
	labelEnemy2Text=StringVar()
	labelEnemy3Text=StringVar()
	labelEnemy4Text=StringVar()
	labelEnemy1Text.set(str(char.enemyChars[0].name)+"\nHealth: "+str(char.enemyChars[0].lifePoints)+"\nArmor: "+str(char.enemyChars[0].armor)+"\nAttack: "+str(char.enemyChars[0].attackValue)+"\nArmor Pen: "+str(char.enemyChars[0].armorPen))
	labelEnemy2Text.set(str(char.enemyChars[1].name)+"\nHealth: "+str(char.enemyChars[1].lifePoints)+"\nArmor: "+str(char.enemyChars[1].armor)+"\nAttack: "+str(char.enemyChars[1].attackValue)+"\nArmor Pen: "+str(char.enemyChars[1].armorPen))
	labelEnemy3Text.set(str(char.enemyChars[2].name)+"\nHealth: "+str(char.enemyChars[2].lifePoints)+"\nArmor: "+str(char.enemyChars[2].armor)+"\nAttack: "+str(char.enemyChars[2].attackValue)+"\nArmor Pen: "+str(char.enemyChars[2].armorPen))
	labelEnemy4Text.set(str(char.enemyChars[3].name)+"\nHealth: "+str(char.enemyChars[3].lifePoints)+"\nArmor: "+str(char.enemyChars[3].armor)+"\nAttack: "+str(char.enemyChars[3].attackValue)+"\nArmor Pen: "+str(char.enemyChars[3].armorPen))
	labelEnemy1=Label(root,height=5,width=15,bg="DarkOrchid1",textvariable=labelEnemy1Text)
	labelEnemy1.grid(row=7,column=20,rowspan=2)
	labelEnemy2=Label(root,height=5,width=15,bg="DarkOrchid1",textvariable=labelEnemy2Text)
	labelEnemy2.grid(row=10,column=20,rowspan=2)
	labelEnemy3=Label(root,height=5,width=15,bg="DarkOrchid1",textvariable=labelEnemy3Text)
	labelEnemy3.grid(row=13,column=20,rowspan=2)
	labelEnemy4=Label(root,height=5,width=15,bg="DarkOrchid1",textvariable=labelEnemy4Text)
	labelEnemy4.grid(row=16,column=20,rowspan=2)

def updateEnemyLabels():
	labelEnemy1Text.set(str(char.enemyChars[0].name)+"\nHealth: "+str(char.enemyChars[0].lifePoints)+"\nArmor: "+str(char.enemyChars[0].armor)+"\nAttack: "+str(char.enemyChars[0].attackValue)+"\nArmor Pen: "+str(char.enemyChars[0].armorPen))
	labelEnemy2Text.set(str(char.enemyChars[1].name)+"\nHealth: "+str(char.enemyChars[1].lifePoints)+"\nArmor: "+str(char.enemyChars[1].armor)+"\nAttack: "+str(char.enemyChars[1].attackValue)+"\nArmor Pen: "+str(char.enemyChars[1].armorPen))
	labelEnemy3Text.set(str(char.enemyChars[2].name)+"\nHealth: "+str(char.enemyChars[2].lifePoints)+"\nArmor: "+str(char.enemyChars[2].armor)+"\nAttack: "+str(char.enemyChars[2].attackValue)+"\nArmor Pen: "+str(char.enemyChars[2].armorPen))
	labelEnemy4Text.set(str(char.enemyChars[3].name)+"\nHealth: "+str(char.enemyChars[3].lifePoints)+"\nArmor: "+str(char.enemyChars[3].armor)+"\nAttack: "+str(char.enemyChars[3].attackValue)+"\nArmor Pen: "+str(char.enemyChars[3].armorPen))
	
def popupmsg(msg):
	popup=Tk()
	popup.wm_title("!")
	label=Label(popup, text=msg)
	label.pack(side="top", fill="x", pady=10)
	B1=Button(popup, text="Okay", command = popup.destroy)
	B1.pack()
	popup.mainloop()

colorCodes=["white","black","green4","red2","yellow2","royalblue"]
#buttonBackstab=None
root = Tk()
frame=Frame(root)
generatePlayerLabels()
generateBoard()
generateSkillButtons()
generateEnemyLabels()
generateLevelLabel()
generateClickLabel()
root.mainloop()
