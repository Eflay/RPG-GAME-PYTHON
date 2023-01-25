import random
from models.warrior import Warrior
from models.mage import Mage
from models.rogue import Rogue
from models.priest import Priest


class Team:
    """
    Initialized a team by providing a team_name
    And make the teamp composition
    """

    def __init__(self, characters):
        
        self.team_name = self.naming()
        self.person = []
        self.ennemies_dead = []
        self.team_compose(characters)

    def naming(self):
        f = open("./teams.txt", "r")
        name = f.readlines()
        return random.choice(name)

    def team_compose(self, characters):
        """For each character in the list provided in parameter, instanciate it"""
        
        for i in range(10):
            if characters[i][1] == "Mage":
                character = Mage(characters[i][0], characters[i][1], characters[i][2], characters[i][3], characters[i][4], characters[i][5], characters[i][6], characters[i][7], characters[i][8], characters[i][9], characters[i][10], characters[i][11])
            elif characters[i][1] == "Rogue":
                character = Rogue(characters[i][0], characters[i][1], characters[i][2], characters[i][3], characters[i][4], characters[i][5], characters[i][6], characters[i][7], characters[i][8], characters[i][9], characters[i][10], characters[i][11])
            elif characters[i][1] == "Priest":
                character = Priest(characters[i][0], characters[i][1], characters[i][2], characters[i][3], characters[i][4], characters[i][5], characters[i][6], characters[i][7], characters[i][8], characters[i][9], characters[i][10], characters[i][11])
            elif characters[i][1] == "Warrior":
                character = Warrior(characters[i][0], characters[i][1], characters[i][2], characters[i][3], characters[i][4], characters[i][5], characters[i][6], characters[i][7], characters[i][8], characters[i][9], characters[i][10], characters[i][11])
        
            self.person.append(character)

    
    def tactics(self):
        """Ask user about which tactics the team should use"""

        self.tactic = int(input(f"""
        Choisissez une tactique pour l'équipe {self.team_name} :

        1. Random
        2. Focus low health
        3. Focus Priest
        4. Heal low health
        5. Focus highest attack
        6. Multiple target Mage
        
        -------------------

        Votre choix : """))

        if self.tactic < 7 and self.tactic > 0:
            return self.tactic
        else:
            print("\nVeuillez choisir un nombre entre 1 et 6 !\n")
            self.tactics()
