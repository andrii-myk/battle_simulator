from random import randint

class Unit():
    """Base class for all units"""
    def __init__(self, number, color, attack_mode):
        self.health = 100
        self.recharge = self.set_recharge()
        self.number = number
        self.color = color
        self.attack_mode = attack_mode
        self.attack_success_prob = None

    def set_recharge(self):
        return randint(100, 2000)

    def under_attack(self, damage):
        self.health -= damage
