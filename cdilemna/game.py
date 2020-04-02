import random

class Game:
    def __init__(self, owner_id):
        self.players = []
        self.seating = {}
        self.owner_id = owner_id
        self.status = 'SETUP'
        self.player_turn = None

    def add_player(self, user_id):
        self.players.append(user_id)

    def remove_player(self, user_id):
        if user_id in self.players:
            self.players.remove(user_id)

    def get_players(self):
        return self.players

    def get_owner_id(self):
        return self.owner_id

    def start_game(self):
        self.status = 'IN_PROGRESS'
