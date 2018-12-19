from random import randint, choice
from time import sleep

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
        return [x for x in self.operators if x.is_active()]

    def is_active(self):
        if self.health > 0:
            temp_value = False
            for operator in self.operators:
                temp_value = temp_value or operator.is_active()
            return temp_value
        else:
            for operator in self.operators:
                operator.health = 0

    def attack(self, enemy_unit: Unit):
        mult_atack_success = 1
        for i in self.get_alive_oper():
            mult_atack_success *= i.attack_success
        self.attack_succes_prob = 0.5 * (1 + self.compute_health() / 100) * (mult_atack_success ** 1/len(self.operators)) # GAVG
        success_var = randint(0, 100)
        if (100 - self.attack_success_prob * 100) <= success_var:
            enemy_unit.under_attack(self.damage())
            for operator in self.get_alive_oper():
                operator.increment_experience()
        sleep(self.recharge /1000)

    def damage(self):
        sum_oper_exp = 0
        for operator in self.get_alive_oper():
            sum_oper_exp += (operator.experience /100)

        return 0.1 + sum_oper_exp

    def under_attack(self, damage):
        self.health -= damage * 0.6
        alive_operators = self.get_alive_oper()
        temp_operator = choice(alive_operators)
        temp_operator.under_attack(damage * 0.2)
        for operator in alive_operators:
            if temp_operator is operator:
                continue
            else:
                operator.under_attack(damage * 0.1)



class Tank(Vehicle):
    def __init__(self, number, color, attack_mode):
        super(Tank, self).__init__(number, color, attack_mode)
        self.operators = [Soldier(1, self.color, self.attack_mode),
                          Soldier(2, self.color, self.attack_mode),
                          Soldier(3, self.color, self.attack_mode)]

    def __repr__(self):
        return f"Tank #{self.number} from {self.color} team"

    def set_recharge(self):
        return randint(1000, 5000)




class Buggy(Vehicle):
    def __init__(self, number, color, attack_mode):
        super(Buggy, self).__init__(number, color, attack_mode)
        self.operators = [Soldier(1, self.color, self.attack_mode),
                          Soldier(2, self.color, self.attack_mode)]

    def __repr__(self):
        return f"Buggy #{self.number} from {self.color} team"

    def set_recharge(self):
        return randint(1000, 2500)


class Squad():
    "Represents units squad"
    def __init__(self, units_number: int, unit_type: str, color: str, attack_mode: int):
        self.units_number = units_number
        self.unit_type = unit_type
        self.color = color
        self.attack_mode = attack_mode
        self.units = []
        self.att_succ_prob = None

    def create_squad(self):
        number = 0
        for i in range(0, self.units_number):
            self.units.append(self.choice_unit_type(number, self.color,self.unit_type))

    def choice_unit_type(self, number: int, color: str, attack_mode: int, unit_type: str):
        if self.unit_type == 'soldier':
            return Soldier(number, color, attack_mode)
        if self.unit_type == 'tank':
            return Tank(number, color, attack_mode)
        if self.unit_type == 'buggy':
            return Buggy(number, color, attack_mode)


    def attack(self):
        multiple_att_prob = 1
        for unit in self.units:
            multiple_att_prob *= unit.attack_success_prob
        self.att_succ_prob = multiple_att_prob ** 1/len(self.units)

    def is_active(self):
        temp = None
        for unit in self.units:
            if unit.is_active():
                temp = True
                break
            else:
                temp = False
        return temp




tank = Tank(1, 'green', 2)
print(tank.recharge)
print(tank.health)
print(tank.total_health)
soldier = Soldier(1, 'green', 3)
print(soldier)
soldier.attack(tank)
soldier.attack(tank)
soldier.attack(tank)
soldier.attack(tank)
print(tank.health)