from abc import ABC, abstractmethod
import random
import time
from termcolor import colored

class Character(ABC):
    """
    Mother class of warrior, rogue, priest and mage
    Create attributes of the different classes like attack, health, ...
    Do the fighting system
    """

    @abstractmethod
    def __init__(self, name, attack, defense, health, crit, initiative, id=None):
        self.id = id
        self.name = name
        self.attack = attack
        self.defense = defense
        self.health = health
        self.crit = crit
        self.initiative = initiative
        self.max_health = health

    def stats(self):
        """Print to the user the statistic of classes and their team"""

        print(f"""Le {self.color_character(self)} {self.name} dispose de :
{colored(self.attack, "red")} points d'attaque, {colored(self.defense, "red")} points de défense, {colored(self.health, "green")} points de vie, {colored(self.crit, "red")} % de chance de critique, {colored(self.parry, "red")} % de chance de parade, {colored(self.initiative, "red")} points d'initiative, {colored(self.dodge, "red")} % chance d'esquive et {colored(self.recovery, "green")} de soin
            """)

    def color_character(self, character):
        """Make different color based on class name"""
        
        if character.__class__.__name__ == "Warrior":
            return colored(character.__class__.__name__, "magenta")
        elif character.__class__.__name__ == "Rogue":
            return colored(character.__class__.__name__, "blue")

        elif character.__class__.__name__ == "Mage":
            return colored(character.__class__.__name__, "cyan")

        else:
            return colored(character.__class__.__name__, "white")


    def show_fight(self, character):
        """Print to the user each fight in battle"""

        print(f"""
            {character.name} {self.color_character(character)} a {colored(character.health, "green")} points de vie avant l'attaque\n
            Il reste {colored(self.health_after_attack if self.health_after_attack >= 0 else "0", "green")} points de vie à {character.name}\n
            Il s'est fait attaqué par {self.name} {self.color_character(self)} qui lui a mis {colored(self.damage, "red")} points de dégats !\n
            La défense de {character.name} était de {colored(character.defense, "red")} et
            l'attaque de {self.name} était de {colored(self.attack, "red")} !
            """)        

    def fighting_system(self, ennemy):
        """
        Compute chance to make a critical strike, dodge or parry
        Do each fight based on initiative
        Print to user dead of character
        """

        random_percentage_crit = random.randint(0, 100)
        random_percentage_dodge = random.randint(0, 100)
        random_percentage_parry = random.randint(0, 100)
        
        try:
            if ennemy.health > 0 and self.health > 0: 
                if ennemy.defense >= self.attack: 
                    if self.crit >= random_percentage_crit: 
                        print(f"""
                        {colored("Critique -- Ignore la défense", "yellow")}
                        """)
                        self.damage = self.attack
                    else:
                        self.damage = 0
                else:
                    if ennemy.dodge >= random_percentage_dodge or ennemy.parry >= random_percentage_parry: 
                        print(f"""
                        {colored("Esquive ou parade", "yellow")}
                        """)
                        self.damage = 0
                    else:
                        if self.crit >= random_percentage_crit: 
                            print(f"""
                            {colored("Critique -- Ignore la défense", "yellow")}
                            """)
                            self.damage = self.attack
                        else:
                            self.damage = self.attack - ennemy.defense

                self.health_after_attack = ennemy.health - self.damage

                self.show_fight(ennemy)

                ennemy.health = self.health_after_attack

                if self.health_after_attack <= 0:
                    self.health_after_attack = 0
                    self.team_ennemies.ennemies_dead.append(ennemy)
                    print(f"""
                    Le {self.color_character(ennemy)} {ennemy.name} est mort !
                    """)
                    self.team_ennemies.person.remove(ennemy)

        except AttributeError:
            pass                  


    def split_between_tactics(self, lock ,allies, ennemies, tactic):
        """Split between tactics use by teams and compute initiative"""

        self.team_ennemies = ennemies
        self.team_allies = allies

        while self.health > 0 and len(ennemies.person) > 0:
            lock.acquire()

            if tactic == 1:
                self.random_attack(allies, ennemies)
            elif tactic == 2:
                self.focus_low_health(allies, ennemies)
            elif tactic == 3:
                self.focus_priest(allies, ennemies)
            elif tactic == 4:
                self.priest_heal_low_health(allies, ennemies)
            elif tactic == 5:
                self.focus_highest_attack(allies, ennemies)
            elif tactic == 6:
                self.multiple_damage(allies, ennemies)

            lock.release()
            time.sleep((1000/self.initiative)/1000)
        
    def verify_max_health(self, person_in_team):
        """Verify if priest heal a character who have not his maximum health"""

        person_max_health_number = 0

        for person in person_in_team:
            if person.health == person.max_health:
                person_max_health_number += 1
        
        if person_max_health_number == len(person_in_team):
            return False

        return True


    def pickup_random_character(self, person_in_team):
        """Choose a random character in the list provide in parameter and return it"""

        try:
            random_number = random.randint(0, len(person_in_team)-1)
            person_random = person_in_team[random_number]

            if self.__class__.__name__ == "Priest": # Si c'est un prêtre
                if self.healing: # Si le prêtre soigne
                    if person_random.health == person_random.max_health: # Verifie que la vie de l'allié est = à sa vie max
                        if self.verify_max_health(person_in_team): # Vérifie qu'il reste bien des personnes ayant leurs points de vie en dessous de leur max_health
                            return self.pickup_random_character(person_in_team) # Si oui, réitère la fonction jusqu'à trouver une bonne personne

            return person_random
        except ValueError:
            pass

    def random_attack(self, allies, ennemies):
        """Split between attack or heal for random attack"""

        random_percentage_healing = random.randint(0, 100)
        percentage_heal = 50
        self.healing = False
            
        if self.__class__.__name__ == "Priest":
            if percentage_heal >= random_percentage_healing:
                self.healing = True
                self.healing_system(self.pickup_random_character(allies.person))
            else:
                self.fighting_system(self.pickup_random_character(ennemies.person))
        else:
            self.fighting_system(self.pickup_random_character(ennemies.person))

    def search_lowest_health(self, person_in_team):
        """Search the character with lowest health in the list provided in parameter and return it"""

        try:
            person_lowest_health = person_in_team[0].health
            person_object = person_in_team[0]

            for person in person_in_team:
                if person_lowest_health > person.health:
                    person_lowest_health = person.health
                    person_object = person
            
            return person_object
        except IndexError:
            pass

    def focus_low_health(self, allies, ennemies):
        """Split between attack or heal for low health focus"""

        random_percentage_healing = random.randint(0, 100)
        percentage_heal = 50
        self.healing = False

            
        if self.__class__.__name__ == "Priest":
            if percentage_heal >= random_percentage_healing:
                self.healing = True
                self.healing_system(self.pickup_random_character(allies.person))
            else:
                self.fighting_system(self.search_lowest_health(ennemies.person))

        else:
            self.fighting_system(self.search_lowest_health(ennemies.person))
        

    def search_priest(self, person_in_team):
        """Search the character Priest in the list provided in parameter and return it, if any return random character"""

        for person in person_in_team:
            if person.__class__.__name__ == "Priest":
                return person

        return self.pickup_random_character(person_in_team)

    def focus_priest(self, allies, ennemies):
        """Split between attack or heal for priest focus"""
        
        random_percentage_healing = random.randint(0, 100)
        percentage_heal = 50
        self.healing = False

            
        if self.__class__.__name__ == "Priest":
            if percentage_heal >= random_percentage_healing:
                self.healing = True
                self.healing_system(self.pickup_random_character(allies.person))
            else:
                self.fighting_system(self.search_priest(ennemies.person))

        else:
            self.fighting_system(self.search_priest(ennemies.person))

    def priest_heal_low_health(self, allies, ennemies):
        """Split between attack or heal for heal low health"""        

        if self.__class__.__name__ == "Priest":
            self.healing_system(self.search_lowest_health(allies.person))
        else:
            self.fighting_system(self.pickup_random_character(ennemies.person))


    def search_highest_attack(self, person_in_team):
        """Search the character with highest attack in the list provided in parameter"""

        try:
            person_highest_attack = person_in_team[0].attack
            person_object = person_in_team[0]

            for person in person_in_team:
                if person_highest_attack < person.attack:
                    person_highest_attack = person.attack
                    person_object = person
            
            return person_object
        except IndexError:
            pass

    def focus_highest_attack(self, allies, ennemies):
        """Split between attack or heal for high attack focus"""

        random_percentage_healing = random.randint(0, 100)
        percentage_heal = 50
        self.healing = False

            
        if self.__class__.__name__ == "Priest":
            if percentage_heal >= random_percentage_healing:
                self.healing = True
                self.healing_system(self.pickup_random_character(allies.person))
            else:
                self.fighting_system(self.search_highest_attack(ennemies.person))

        else:
            self.fighting_system(self.search_highest_attack(ennemies.person))

    def multiple_damage(self, allies, ennemies):
        random_percentage_healing = random.randint(0, 100)
        percentage_heal = 50
        self.healing = False
            
        if self.__class__.__name__ == "Priest":
            if percentage_heal >= random_percentage_healing:
                self.healing = True
                self.healing_system(self.pickup_random_character(allies.person))
            else:
                self.fighting_system(self.pickup_random_character(ennemies.person))

        elif self.__class__.__name__ == "Mage":
            if self.attack > 75:
                self.attack = self.attack/3

            i = 0
            while i < 3:
                self.fighting_system(self.pickup_random_character(ennemies.person))
                i += 1

        else:
            self.fighting_system(self.pickup_random_character(ennemies.person))