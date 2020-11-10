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
		del self.users[user.id]

		if self.isCreator(user):
			self.creator = None


	def hasUser(self, user):
		return user.id in self.users


	def isCreator(self, user):
		if self.creator is None:
			return False
		return user.id == self.creator.id


	def __len__(self):
		return len(self.users)


	def generateRoomId(self, length=12):
		charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
		roomId = ""

		for _ in range(length):
			roomId += charset[random.randint(0, len(charset))]
		return roomId
