from random import randint
from time import sleep

class Soldier(Unit):
    """Class which represents soldier object"""
    def __init__(self, number: int, color: str, attack_mode: int):
        super(Soldier, self).__init__(number, color, attack_mode)
        self.experience = 1
        self.active = True
        self.color = color

    def __repr__(self):
        return f"Soldier #{self.number} from {self.color} team"

    def increment_experience(self):
        """Watching experience is in range 1-50"""
        if self.experience < 50:
            self.experience += 1

    def is_active(self):
        return True if self.health > 0 else False

    def attack(self, enemy_unit: Unit):
        if self.is_active():
            self.attack_success_prob = 0.5 * (1 + self.health / 100) * randint(50 + self.experience, 100) /100
            success_var = randint(0, 100)
            if (100 - self.attack_success_prob * 100) <= success_var:
                print(self.damage())
                enemy_unit.under_attack(self.damage())
                self.increment_experience()
                print('enemy unit is under attack')
            else:
                print("Attack has been failured")
        sleep(self.recharge/1000)

    def damage(self):
        return 0.05 + self.experience / 100