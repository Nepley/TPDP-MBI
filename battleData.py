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
		with open("gamesNames.json", 'r', encoding = "utf_8") as f:
			gamesNames = json.load(f)

		loaded = False
		for game in gamesNames:
			if not loaded:
				try:
					self.pm = pymem.Pymem(game)

					self.playerPuppetId = self.pm.base_address+0x00C59F6D
					self.playerPuppetName = self.pm.base_address+0x00C59F71
					self.playerPuppetStyleId = self.pm.base_address+0x00C59F6F
					self.enemyTrainer = self.pm.base_address+0x00C5A104
					self.enemyPuppetId = self.pm.base_address+0x00C5A510
					self.enemyPuppetName = self.pm.base_address+0x00C5A514
					self.enemyPuppetStyleId = self.pm.base_address+0x00C5A512
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
