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

		if self.creator.id == user.id:
			self.creator = None


	def __len__(self):
		return len(self.users)


	def generateRoomId(self, length=12):
		charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
		roomId = ""

		for i in range(length):
			roomId += charset[i]
		return roomId
