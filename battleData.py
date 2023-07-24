import pymem
import json

class BattleData:
	puppetData = []
	puppetList = []
	pm = None
	#
	playerPuppetId = None
	playerPuppetName = None
	playerPuppetStyleId = None
	enemyTrainer = None
	enemyPuppetId = None
	enemyPuppetName = None
	enemyPuppetStyleId = None


	def __init__(self):
		# Load Puppet Data
		with open("puppetData.json", 'r') as f:
			self.puppetData = json.load(f)

		with open("puppetList.json", 'r') as f:
			self.puppetList = json.load(f)

		# We load the possibles games executable
		with open("gamesAdresses.json", 'r', encoding = "utf_8") as f:
			gamesAdresses = json.load(f)

		loaded = False
		for game in gamesAdresses:
			if not loaded:
				# We try to load the game with the Extended Mod (English Ver.)
				try:
					self.pm = pymem.Pymem(game["PROCESS_NAME"])
					self.playerPuppetId = int(game["PLAYER_PUPPET_ID"], base=16)
					self.playerPuppetName = int(game["PLAYER_PUPPET_NAME"], base=16)
					self.playerPuppetStyleId = int(game["PLAYER_STYLE_ID"], base=16)
					self.enemyTrainer = int(game["ENEMY_TRAINER"], base=16)
					self.enemyPuppetId = int(game["ENEMY_PUPPET_ID"], base=16)
					self.enemyPuppetName = int(game["ENEMY_PUPPET_NAME"], base=16)
					self.enemyPuppetStyleId = int(game["ENEMY_STYLE_ID"], base=16)
					loaded = True
					break
				except:
					pass

		if not loaded:
			print("ERROR: Game not found.")
			exit(-1)

	def getEnemyPuppetId(self):
		id = self.pm.read_short(self.enemyPuppetId)
		return id
	
	def getEnemyPuppetSurname(self):
		return self.pm.read_string(self.enemyPuppetName, 9)
	
	def getEnemyPuppet(self):
		return self.puppetList[str(self.getEnemyPuppetId())]
	
	def getEnemyTrainer(self):
		return self.pm.read_string(self.enemyTrainer, 9)
	
	def getEnemyPuppetStyles(self):
		return self.puppetData[self.puppetList[str(self.getEnemyPuppetId())]]
	
	def getPlayerPuppetId(self):
		return self.pm.read_short(self.playerPuppetId)

	def getPlayerPuppetSurname(self):
		return self.pm.read_string(self.playerPuppetName, 9)
	
	def getPlayerStyleId(self):
		return int.from_bytes(self.pm.read_bytes(self.playerPuppetStyleId, 1), 'little')
	
	def getEnemyPuppetStyleId(self):
		return int.from_bytes(self.pm.read_bytes(self.enemyPuppetStyleId, 1), 'little')
	
	def getEnemyPuppetStyle(self):
		stylesList = list(self.getEnemyPuppetStyles().keys())
		return stylesList[self.getEnemyPuppetStyleId()]

	def getEnemyTableWeaknesses(self):
		stylesList = list(self.getEnemyPuppetStyles().values())
		return stylesList[self.getEnemyPuppetStyleId()]
