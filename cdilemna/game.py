import random

class Game:
    def __init__(self, owner_id):
        self.players = []
        self.seating = {}
        self.owner_id = owner_id
        self.status = 'SETUP'
        self.player_turn = None

    def addPlayer(self, user_id):
        self.players.append(playerId)

    def removePlayer(self, user_id):
        if user_id in self.players:
            self.players.remove(user_id)

    def startGame(self):
        self.status = 'IN_PROGRESS'
