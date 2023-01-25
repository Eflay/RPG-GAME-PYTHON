from models.character import Character
import random
import names


class Rogue(Character):
    def __init__(self, *args):
        if len(args) == 0:
            super().__init__(name=names.get_full_name(),
                             attack=random.randint(40, 60),
                             defense=random.randint(30, 50),
                             health=random.randint(70, 80),
                             crit=random.randint(15, 20),
                             initiative=random.randint(75, 90))

            self.dodge=random.randint(40, 70)

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


