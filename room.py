import random


class Room:
	def __init__(self, roomId=None):
		self.id = roomId
		if self.id is None:
			self.id = self.generateRoomId(12)

		self.users = {}


	def addUser(self, user):
		self.users[user.id] = user


	def __len__(self):
		return len(self.users)


	def generateRoomId(self, length=12):
		charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
		roomId = ""

		for i in range(length):
			roomId += charset[i]
		return roomId
