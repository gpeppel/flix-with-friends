import random


class Room:
	def __init__(self, roomId=None):
		self.id = roomId
		if self.id is None:
			self.id = self.generateRoomId(12)

		self.users = {}
		self.creator = None


	def addUser(self, user):
		self.users[user.id] = user

		if self.creator is None:
			self.creator = user


	def removeUser(self, user):
		if user.id not in self.users:
			return False

		del self.users[user.id]

		if self.isCreator(user):
			self.creator = None
		return True


	def hasUser(self, user):
		return user.id in self.users


	def isCreator(self, user):
		if self.creator is None:
			return False
		return user.id == self.creator.id


	def setCreator(self, user):
		if user is not None and not self.hasUser(user):
			self.addUser(user)

		self.creator = user


	def __len__(self):
		return len(self.users)


	def generateRoomId(self, length=12):
		charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
		roomId = ""

		for _ in range(length):
			roomId += charset[random.randint(0, len(charset) - 1)]
		return roomId
