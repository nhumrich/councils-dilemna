from uuid import uuid4

class User:
    id = None
    name = None
    game_id = None
    money = 8
    power = 8

    def __init__(self, name, money, power):
        self.id = str(uuid4())
        self.name = name
        self.money = money
        self.power = power

    def spend_money(amount_to_spend):
        # TODO prevent negative
        self.money = self.money - amount_to_spend
        return self.money

    def gain_money(amount_to_gain):
        self.money = self.money + amount_to_gain
        return self.money

    def flex(power_to_spend):
        # TODO prevent negative
        self.power = self.power - self.power_to_spend
        return self.power

    def cower(power_to_gain):
        self.power = self.power + power_to_gain
        return self.power
