from models.character import Character
import random
import names
from termcolor import colored


class Priest(Character):
    def __init__(self, *args):
        if len(args) == 0:
            super().__init__(name=names.get_full_name(),
                             attack=random.randint(30, 60),
                             defense=random.randint(60, 80),
                             health=random.randint(70, 90),
                             crit=random.randint(5, 7),
                             initiative=random.randint(50, 60))


            self.parry=random.randint(30, 50)
            self.max_health = self.health
            self.recovery = self.defense/4

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


    def healing_system(self, ally):

        health_before_heal = ally.health

        if len(self.team_allies.person) > 0:
            if ally.health < ally.max_health:
                if (ally.health + self.recovery) >= ally.max_health:
                    ally.health = ally.max_health
                else:
                    ally.health = ally.health + self.recovery
        
        self.show_heal(health_before_heal, ally)


    def show_heal(self, health_before_heal, ally):
        print(f"""
            Le {colored("Priest", "white")} {self.name} a soigné {ally.name} à hauteur de {colored(self.recovery, "green")} points de vie
            Il avait {colored(health_before_heal, "green")} points de vie et a maitenant {colored(ally.health, "green")} points de vie
            Au début du combat, il possédait {colored(ally.max_health, "green")} points de vie
            """)