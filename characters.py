import numpy as np
import board as bd


class PlayerCharacter():
	def __init__(self,lifePoints,attackValue,color,armor,armorPen,name):
		self.lifePoints=lifePoints
		self.armorPen=armorPen
		self.attackValue=attackValue
		#["white","black","green","red","yellow","blue"]
		self.color=color
		self.armor=armor
		self.name=name
		self.mana=100
		if color==2:
			self.skill=self.backstab
			self.skillName="Backstab"
			self.skillCost=25
			self.skillDesc="Backstab all for double damage and ignoring armor"
		elif color==3:
			self.skill=self.wildfire
			self.skillName="Wild Fire"
			self.skillCost=20
			self.skillDesc="Destroy 5 columns at random"
		elif color==4:
			self.skill=self.prayer
			self.skillName="Prayer"
			self.skillCost=35
			self.skillDesc="Increase all living allies health"
		elif color==5:
			self.skill=self.smash
			self.skillName="Smash"
			self.skillCost=7
			self.skillDesc="Attack each enemy"

	def isAlive(self):
		if self.lifePoints>0:
			return True
		else:
			return False

	def takeHit(self,hitPower,armorPen):
		appliedArmor=self.armor-armorPen
		if appliedArmor<0:
			appliedArmor=0
		dmg=hitPower-appliedArmor
		if dmg<0:
			dmg=0
		self.lifePoints-=dmg
		print (self.name+" takes "+str(dmg)+" damage!")
		if self.lifePoints<=0:
			print (self.name+" has died!!!")
			self.lifePoints=0

	def attack(self,target):
		target.takeHit(self.attackValue,self.armorPen)
	
	def heal(self,amount):
		if self.isAlive():
			self.lifePoints+=amount
	
	def manaGain(self,amount):
		self.mana+=amount

	def useSkill(self):
		if self.isAlive():
			if self.mana>=self.skillCost:
				print ("using skill: "+self.skillName)
				self.skill()
				self.mana-=self.skillCost
			else:
				print ("not enough mana")
		else:
			print (self.name+" is dead...")
	
	def backstab(self):
		damage=(self.attackValue*2+self.armorPen*2)*2
		for enemy in enemyChars:
			if enemy.isAlive():
				enemy.takeHit(damage,10000)
	
	def prayer(self):
		val=50
		for ally in playerChars:
			ally.heal(val)
	
	def smash(self):
		damage=self.attackValue*2
		for enemy in enemyChars:
			if enemy.isAlive():
				enemy.takeHit(damage,self.armorPen)
	
	def wildfire(self):
		manaCounts=bd.wildfire()
		for char in range(0,len(playerChars)):
			if playerChars[char].isAlive():
				playerChars[char].manaGain(manaCounts[char+2])

class EnemyCharacter():
	def __init__(self,level):
		self.level=int(level/5)
		self.lifePoints=np.random.randint(1*self.level+20,100*self.level+100)
		self.armorPen=0
		self.attackValue=np.random.randint(8,self.level+12)*(self.level+1)
		self.armorPen=np.random.randint(0,3*self.level+20)
		#["white","black","green","red","yellow","blue"]
		self.armor=np.random.randint(0*self.level,8*self.level+8)
		if self.level>2:
			prefixes=["Mighty","Fearless","Great","Strong","Major","Hardened","Epic","Giant"]
		elif self.level==1 or self.level==2:
			prefixes=["Mighty","Scrawny","Weak","Lesser","Major","Minor","Epic","Giant"]
		else:
			prefixes=["Puny","Scrawny","Weak","Lesser","Sickly","Minor","Pathetic","Injured"]
		names=["Wolf","Imp","Titan","Goblin","Demon","Treant"]
		self.name=prefixes[np.random.randint(0,8)]+" "+names[np.random.randint(0,6)]
	
	def __del__(self):
		#print (self.name,"Destroyed")
		pass
	
	def isAlive(self):
		if self.lifePoints>0:
			return True
		else:
			return False
	
	def takeHit(self,hitPower,armorPen):
		appliedArmor=self.armor-armorPen
		if appliedArmor<0:
			appliedArmor=0
		dmg=hitPower-appliedArmor
		if dmg<0:
			dmg=0
		self.lifePoints-=dmg
		print (self.name+" takes "+str(dmg)+" damage!")
		if self.lifePoints<=0:
			print (self.name+" has died!!!")
			self.lifePoints=0
	
	def attack(self,target):
		target.takeHit(self.attackValue,self.armorPen)

def endRound():
	#players attack
	for character in playerChars:
		if character.isAlive():
			for enemy in enemyChars:
				if enemy.isAlive():
					print (character.name+" is attacking "+enemy.name)
					character.attack(enemy)
					break
				else:
					pass
	#enemies attack
	for enemy in enemyChars:
		if enemy.isAlive():
			for character in playerChars:
				if character.isAlive():
					print (enemy.name+" is attacking "+character.name)
					enemy.attack(character)
					break
				else:
					pass

def gameOver():
	if playerChars[0].isAlive() or playerChars[1].isAlive() or playerChars[2].isAlive() or playerChars[3].isAlive():
		return False
	else:
		return True
def generateEnemies():
	enemyChars=[]
	for n in range(0,4):
		enemyChars.append(EnemyCharacter(level))
	return enemyChars

level=1
#create player characters [green,red,yellow,blue]
playerChars=[]
playerChars=[PlayerCharacter(150,10,5,15,2,"Knight"),PlayerCharacter(100,20,2,5,8,"Rouge"),PlayerCharacter(75,15,3,3,15,"Wizard"),PlayerCharacter(125,5,4,10,1,"Priest")]

#generate enemies
enemyChars=generateEnemies()
