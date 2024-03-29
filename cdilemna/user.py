from uuid import uuid4

class User:
    id = None
    name = None
    game_id = None
    money = 8
    power = 8

    def __init__(self, name, incoming_id = None):
        if incoming_id is not None:
            self.id = incoming_id
        else:
            self.id = str(uuid4())
        self.name = name
        self.money = 8
        self.power = 8

    def spend_money(self, amount_to_spend):
        # TODO prevent negative
        self.money = self.money - amount_to_spend
        return self.money

    def gain_money(self, amount_to_gain):
        self.money = self.money + amount_to_gain
        return self.money

    def spend_power(self, power_to_spend):
        # TODO prevent negative
        self.power = self.power - power_to_spend
        return self.power

    def gain_power(self, power_to_gain):
        self.power = self.power + power_to_gain
        return self.power

    def join_game(self, game_id):
        self.game_id = game_id
