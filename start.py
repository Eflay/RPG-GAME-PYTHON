from db import *
import random
from models.warrior import Warrior
from models.mage import Mage
from models.rogue import Rogue
from models.priest import Priest
from models.battle import Battle

def start():

    create_database()

    classes = (Warrior, Mage, Rogue, Priest)

    for i in range(20):
        instance = random.choice(classes)()
        insert_character(instance)

    list_all = list(select_character())

    list_of_characters = []
    for i in range(len(list_all)):
        x = list(list_all[i])
        list_of_characters.append(x)

    new_battle = Battle(list_of_characters)
    new_battle.show_info()
    new_battle.fight()