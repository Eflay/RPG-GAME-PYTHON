from models.character import Character
import random
import names


class Mage(Character):
    def __init__(self, *args):
        if len(args) == 0:
            super().__init__(name=names.get_full_name(),
                             attack=random.randint(100, 150),
                             defense=random.randint(20, 40),
                             health=random.randint(60, 70),
                             crit=random.randint(5, 7),
                             initiative=random.randint(60, 70))

            self.max_health=self.health
                
        else:
            self.id = args[0]
            self.name = args[2]
            self.attack = args[3]
            self.defense = args[4]
            self.health = args[5]
            self.crit = args[6]
            self.initiative = args[7]
            self.dodge = args[8]
            self.recovery = args[9]
            self.parry = args[10]
            self.max_health = args[11]

        