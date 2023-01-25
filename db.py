import sqlite3


def create_database():
    """Create all tables"""

    con = sqlite3.connect("database.db")
    cur = con.cursor()
    # cur.execute("DROP TABLE character")
    # cur.execute("DROP TABLE history")
    # cur.execute("DROP TABLE battle")
    # cur.execute("DROP TABLE team")

    try:
        cur.execute("""CREATE TABLE character(character_id INTEGER PRIMARY KEY AUTOINCREMENT, class TEXT, name TEXT, attack INTEGER, defense INTEGER, health INTEGER, 
                    crit INTEGER, initiative INTEGER, dodge INTEGER, recovery INTEGER, parry INTEGER, max_health INTEGER)
                    """)

        cur.execute("""CREATE TABLE history(history_id INTEGER PRIMARY KEY AUTOINCREMENT, character_id INTERGER, health_remaining INTEGER, battle_id INTEGER, team_id,  
        FOREIGN KEY(character_id) REFERENCES character(character_id), FOREIGN KEY(battle_id) REFERENCES battle(battle_id), FOREIGN KEY(team_id) REFERENCES team(team_id))
                    """)
        
        cur.execute("""CREATE TABLE battle(battle_id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, team_win TEXT, team_lose TEXT, tactic_win INTERGER, tactic_lose INTEGER)
                    """)
        
        cur.execute("""CREATE TABLE team(team_id INTEGER PRIMARY KEY AUTOINCREMENT, team_name TEXT, battle_id INTEGER, FOREIGN KEY(battle_id) REFERENCES battle(battle_id))
                    """)

    except sqlite3.OperationalError:
        print("La table existe déjà. Continuation du programme...")

    
    con.commit()
    con.close()


def insert_character(instance):
    """Insert every character in table character"""

    con = sqlite3.connect("database.db")
    cur = con.cursor()

    if instance.__class__.__name__ == "Warrior":

        cur.execute(f"""INSERT INTO character 
        (class, name, attack, defense, health, crit, initiative, dodge, recovery, parry, max_health)
        VALUES('{instance.__class__.__name__}', '{instance.name}', {instance.attack}, {instance.defense}, {instance.health}, 
        {instance.crit}, {instance.initiative}, false, false, {instance.parry}, {instance.max_health})
        """)

    elif instance.__class__.__name__ == "Mage":
        cur.execute(f"""INSERT INTO character 
        (class, name, attack, defense, health, crit, initiative, dodge, recovery, parry, max_health)
        VALUES('{instance.__class__.__name__}', '{instance.name}', {instance.attack}, {instance.defense}, {instance.health}, 
        {instance.crit}, {instance.initiative}, false, false, false, {instance.max_health})
        """)

    elif instance.__class__.__name__ == "Rogue":
        cur.execute(f"""INSERT INTO character 
        (class, name, attack, defense, health, crit, initiative, dodge, recovery, parry, max_health)
        VALUES('{instance.__class__.__name__}', '{instance.name}', {instance.attack}, {instance.defense}, {instance.health}, 
        {instance.crit}, {instance.initiative}, {instance.dodge}, false, false, {instance.max_health})
        """)

    elif instance.__class__.__name__ == "Priest":
        cur.execute(f"""INSERT INTO character 
        (class, name, attack, defense, health, crit, initiative, dodge, recovery, parry, max_health)
        VALUES('{instance.__class__.__name__}', '{instance.name}', {instance.attack}, {instance.defense}, {instance.health}, 
        {instance.crit}, {instance.initiative}, false, {instance.recovery}, {instance.parry}, {instance.max_health})
        """)

    con.commit()
    con.close()


def select_character():
    """Select 20 character to battle randomly"""

    con = sqlite3.connect("database.db")
    cur = con.cursor()

    res = cur.execute(f"""SELECT * from character where health > 0 ORDER BY random() LIMIT 20""")

    return res.fetchall()


def update_character_instruction(team_win, team_win_dead, team_lose_dead):
    """SQL nstruction to update character table after battle"""

    con = sqlite3.connect("database.db")
    cur = con.cursor()

    for pers in team_win.person:
        cur.execute(f"""UPDATE character set health={pers.health} where name='{pers.name}'""")
    
    for pers in team_win_dead:
        pers.health = 0

        cur.execute(f"""UPDATE character set health={pers.health} where name='{pers.name}'""")

    for pers in team_lose_dead:
        pers.health = 0

        cur.execute(f"""UPDATE character set health={pers.health} where name='{pers.name}'""")
    
    con.commit()


def update_character(team_a_after_battle, team_b_after_battle, team_a_dead, team_b_dead):

    if len(team_a_after_battle.person) > 0:
        update_character_instruction(team_a_after_battle, team_a_dead, team_b_dead)

    elif len(team_b_after_battle.person) > 0:
        update_character_instruction(team_b_after_battle, team_b_dead, team_a_dead)


def update_history_instruction(team_win, team_win_dead, team_lose_dead, team_lose):
    """SQL instructions to update history table"""

    con = sqlite3.connect("database.db")
    cur = con.cursor()

    res_max_id = cur.execute("SELECT MAX(battle_id) from battle").fetchall()[0][0]
    res_id_team_1 = cur.execute(f"SELECT team_id from team WHERE team_name = '{team_win.team_name}'").fetchall()[0][0]
    res_id_team_2 = cur.execute(f"SELECT team_id from team WHERE team_name = '{team_lose.team_name}'").fetchall()[0][0]


    for pers in team_win.person:
        cur.execute(f"""INSERT INTO history 
                (character_id, health_remaining, battle_id, team_id)
                VALUES('{pers.id}', {pers.health}, {res_max_id}, {res_id_team_1})
                """)

    for pers in team_win_dead:
        cur.execute(f"""INSERT INTO history 
                (character_id, health_remaining, battle_id, team_id)
                VALUES('{pers.id}', 0,{res_max_id}, {res_id_team_1})
                """)
    
    for pers in team_lose_dead:
        cur.execute(f"""INSERT INTO history 
                (character_id, health_remaining, battle_id, team_id)
                VALUES('{pers.id}', 0, {res_max_id}, {res_id_team_2})
                """)

    con.commit()
    con.close()

def update_history(team_a_after_battle, team_b_after_battle, team_a_dead, team_b_dead):

    if len(team_a_after_battle.person) > 0:
        update_history_instruction(team_a_after_battle, team_a_dead, team_b_dead, team_b_after_battle)
        

    elif len(team_b_after_battle.person) > 0:
        update_history_instruction(team_b_after_battle, team_b_dead, team_a_dead, team_a_after_battle)


def update_battle_instruction(team_win, team_lose):
    """SQL instruction update battle table"""

    con = sqlite3.connect("database.db")
    cur = con.cursor()


    cur.execute(f"""INSERT INTO battle
                (date, team_win, team_lose, tactic_win, tactic_lose)
                VALUES(strftime('%Y-%m-%d %H-%M','now'),'{team_win.team_name}', '{team_lose.team_name}', {team_win.tactic}, {team_lose.tactic})
                """)

    con.commit()
    con.close()


def update_battle(team_a_after_battle, team_b_after_battle):

    if len(team_a_after_battle.person) > 0:
        update_battle_instruction(team_a_after_battle, team_b_after_battle)
        

    elif len(team_b_after_battle.person) > 0:
        update_battle_instruction(team_b_after_battle, team_a_after_battle)


def update_team(team):
    """SQL instruction update team table"""

    con = sqlite3.connect("database.db")
    cur = con.cursor()

    res_max_id = cur.execute("SELECT MAX(battle_id) from battle").fetchall()[0][0]

    cur.execute(f"""INSERT INTO team
                (team_name, battle_id)
                VALUES('{team.team_name}',{res_max_id})
                """)

    con.commit()
    con.close()