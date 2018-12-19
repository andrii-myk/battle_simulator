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


class Soldier(Unit):
    """Class which represents soldier object"""
    def __init__(self, number: int, color: str, attack_mode: int):
        super(Soldier, self).__init__(number, color, attack_mode)
        self.experience = 1
        self.active = True
        self.color = color


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
            if (100 - self.attack_success_prob * 100)  <= success_var:
                print(self.damage())
                enemy_unit.under_attack(self.damage())
                self.increment_experience()
                print('enemy unit is under attack')
            else:
                print("Attack has been failured")


    def damage(self):
        return 0.05 + self.experience / 100


class Vehicle(Unit):
    """Class which represents base vehicle object"""
    def __init__(self, number, color, attack_mode):
        super(Vehicle, self).__init__(number, color, attack_mode)
        self.operators = []
        self.total_health = self.compute_health()


    def compute_health(self):
        temp_health = 0
        for operator in self.operators:
            temp_health += operator.health
        return (self.health + temp_health) / (len(self.operators) + 1)


    def get_alive_oper(self):
        return filter(lambda x: x.is_active() == True, self.operators)


    def is_active(self):
        if self.health > 0:
            temp_value = False
            for operator in self.operators:
                temp_value = temp_value or operator.is_active()
            return temp_value
        else:
            for operator in self.operators:
                operator.health = 0


    def attack(self):
        mult_atack_success = 1
        for i in self.get_alive_oper():
            mult_atack_success *= i.attack_success
        self.attack_succes = 0.5 * (1 + self.compute_health() / 100) * (mult_atack_success ** 1/len(self.operators)) # GAVG
        if


    def damage(self):
        sum_oper_exp = 0
        for operator in self.get_alive_oper():
            sum_oper_exp += operator.experience /100

        return 0.1 + sum_oper_exp


class Tank(Vehicle):
    def __init__(self, number, color, attack_mode):
        super(Tank, self).__init__(number, color, attack_mode)
        self.operators = [Soldier(1, self.color, self.attack_mode),
                          Soldier(2, self.color, self.attack_mode),
                          Soldier(3, self.color, self.attack_mode)]


    def set_recharge(self):
        return randint(1000, 5000)






class Buggy(Vehicle):
    def __init__(self, number, color, attack_mode):
        super(Buggy, self).__init__(number, color, attack_mode)
        self.operators = [Soldier(1, self.color, self.attack_mode),
                          Soldier(2, self.color, self.attack_mode)]


    def set_recharge(self):
        return randint(1000, 2500)






tank = Tank(1, 'green', 2)
print(tank.recharge)
print(tank.health)
print(tank.total_health)
soldier = Soldier(1, 2, 3)
print(soldier)
soldier.attack(tank)
soldier.attack(tank)
soldier.attack(tank)
soldier.attack(tank)
print(tank.health)