import threading
from models.team import Team
from db import update_character, update_history, update_battle, update_team
from termcolor import colored

class Battle:
    """Initiate Battle class by creating two teams and assign tactics provided by user input"""

    def __init__(self, characters):
        self.team_a = self.team_create(characters[10:])
        self.team_b = self.team_create(characters[:10])
        self.team_a_tactic = self.team_a.tactics()
        self.team_b_tactic = self.team_b.tactics()

    def team_create(self, characters):
        team = Team(characters)
        return team

    def get_message(self, team):
        """Print to the user teams compositions"""

        print(f"""\n L'équipe {team.team_name} est composé de :\n""")

        for pers in team.person:
            pers.stats()

    def show_info(self):
        self.get_message(self.team_a)
        self.get_message(self.team_b)

    def color_character(self, character):
        """Make color for each class"""

        if character.__class__.__name__ == "Warrior":
            return colored(character.__class__.__name__, "magenta")
        elif character.__class__.__name__ == "Rogue":
            return colored(character.__class__.__name__, "blue")

        elif character.__class__.__name__ == "Mage":
            return colored(character.__class__.__name__, "cyan")

        else:
            return colored(character.__class__.__name__, "white")

    def fight(self):
        """Assign a thread for each character and start it with calling split_between_tatics"""

        thread_list = []
        
        lock = threading.Lock()

        for character in self.team_a.person:
            thread = threading.Thread(target=character.split_between_tactics, args=[lock, self.team_a, self.team_b, self.team_a_tactic])
            thread.start()
            thread_list.append(thread)

        for character in self.team_b.person:
            thread = threading.Thread(target=character.split_between_tactics, args=[lock, self.team_b, self.team_a, self.team_b_tactic])
            thread.start()
            thread_list.append(thread)

        for thread in thread_list:
            thread.join()

        self.end()

    
    def show_results(self, team_a, team_b):
        """Print to the user results of the battle"""

        if len(team_a.person) > 0:
            print(f"L'équipe {team_a.team_name} a gagné cette bataille avec la tactique {team_a.tactic} !")
            print("Il reste :")

            for i in range(len(team_a.person)):
                print(f"""{team_a.person[i].name} qui est un {self.color_character(team_a.person[i])}""")
        
        else:
            print(f"L'équipe {team_b.team_name} a gagné cette bataille avec la tactique {team_b.tactic} !")
            print("Il reste :")

            for i in range(len(team_b.person)):
                print(f"""{team_b.person[i].name} qui est un {self.color_character(team_b.person[i])}""")

    def end(self):
        """Calling functions to update database"""

        print("BATTLE FINISHED !")

        update_character(self.team_a, self.team_b, self.team_a.ennemies_dead, self.team_b.ennemies_dead)
        update_battle(self.team_a, self.team_b)
        update_team(self.team_a)
        update_team(self.team_b)
        update_history(self.team_a, self.team_b, self.team_a.ennemies_dead, self.team_b.ennemies_dead)



        self.show_results(self.team_a, self.team_b)