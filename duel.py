import pyautogui
import random

import window
import img_search
import delay

SKIP_DUEL_ANIMATION_POS = (679, 131)#45x45
SKIP_DUEL_ANIMATION_MAX_TIMES = 100

SELECT_CARD_POS = (402, 548)#180x45
SELECT_CARD_MAX_TIMES = 5

SUMMON_MONSTER_POS = (458, 442)#30x30
SUMMON_MONSTER_MAX_TIMES = 3

MY_MONSTER_SEATS_POS = [(415, 315), (475, 315), (544, 315)]
OPPO_MONSTER_SEATS_POS = [(420, 197), (482, 200), (544, 200)]

NEXT_STAGE_POS = (689, 393)#24x24

DUEL_END_POS = (474, 568)#85x20
DUEL_END_NEXT_POS = (471, 568)#90x20
DUEL_END_NEXT_MAX_TIMES = 50
AFTER_DUEL_ACTIVITY_NEXT = (473, 476)#90x20
AFTER_DUEL_ACTIVITY_MAX_TIMES = 20

def clickRandomPos(pos, x_move_max, y_move_max):
    x_move = random.randint(0, x_move_max)
    y_move = random.randint(0, y_move_max)
    pyautogui.moveTo(pos[0] + x_move, pos[1] + y_move)
    delay.standard_delay(0.1)
    pyautogui.click()

def moveToRandomPos(pos, x_move_max, y_move_max, duration=0.0):
    x_move = random.randint(0, x_move_max)
    y_move = random.randint(0, y_move_max)
    pyautogui.moveTo(pos[0] + x_move, pos[1] + y_move, duration=duration)

def skipDuelAnimation():
    pos = img_search.pos_rel2abs(SKIP_DUEL_ANIMATION_POS)

    for _ in range(SKIP_DUEL_ANIMATION_MAX_TIMES):
        if img_search.duelAnimationEnd() or img_search.duelEnd():
            return
        clickRandomPos((pos[0] + 10, pos[1] + 10), 30, 30)
        delay.random_float_delay(0.2, 0.2)
        
    # retry too much times
    raise img_search.ButtonNotFoundException("talking end flag")

def summonMonster():
    selectMonster()
    for _ in range(SUMMON_MONSTER_MAX_TIMES):
        if not img_search.monsterSelected():
            return
        pos = img_search.pos_rel2abs(SUMMON_MONSTER_POS)
        clickRandomPos((pos[0] + 2, pos[1] + 2), 26, 26)
        delay.random_float_delay(0.6, 0.2)
    
    raise img_search.ButtonNotFoundException("monster summoned flag")

def selectMonster():
    # randomly select monster card
    for _ in range(SELECT_CARD_MAX_TIMES):
        if img_search.monsterSelected():
            return
        
        pos = img_search.pos_rel2abs(SELECT_CARD_POS)
        clickRandomPos((pos[0] + 5, pos[1] + 2), 170, 40)
        delay.random_float_delay(0.5, 0.2)
    
    raise img_search.ButtonNotFoundException("monster selected flag")

def nextStage():
    pos = img_search.pos_rel2abs(NEXT_STAGE_POS)
    clickRandomPos((pos[0] + 2, pos[1] + 2), 20, 20)
    delay.random_float_delay(0.3, 0.5)
    clickRandomPos((pos[0] + 2, pos[1] + 2), 20, 20)
    delay.random_float_delay(0.3, 0.5)

def allMonsterAttack():
    my_monster_seats = img_search.getMyMonsterSeatsList()
    for my_seat_id in range(len(my_monster_seats)):
        if my_monster_seats[my_seat_id]:
            oppo_monster_seats = img_search.getOppoMonsterSeatsList()
            for oppo_seat_id in range(len(oppo_monster_seats)):
                if oppo_monster_seats[oppo_seat_id] or oppo_seat_id == 2:
                    # battle
                    pos = img_search.pos_rel2abs(MY_MONSTER_SEATS_POS[my_seat_id])
                    moveToRandomPos((pos[0] + 27, pos[1] + 32), 15, 20)
                    pyautogui.mouseDown()
                    pos = img_search.pos_rel2abs(OPPO_MONSTER_SEATS_POS[oppo_seat_id])
                    moveToRandomPos((pos[0] + 27, pos[1] + 32), 15, 20, duration=0.5)
                    pyautogui.mouseUp()
                    skipDuelAnimation()
                    delay.random_float_delay(0.8, 0.2)

def afterDuelNext():
    pos = img_search.pos_rel2abs(DUEL_END_NEXT_POS)
    for _ in range(DUEL_END_NEXT_MAX_TIMES):
        if img_search.duelEndNextFlag():
            clickRandomPos((pos[0] + 2, pos[1] + 2), 86, 16)
            delay.random_float_delay(0.3, 0.2)
            return
        delay.random_float_delay(0.5, 0.2)
    
    # retry too much times
    raise img_search.ButtonNotFoundException("duel end next flag")

def afterDuelActivityNext():
    pos = img_search.pos_rel2abs(AFTER_DUEL_ACTIVITY_NEXT)
    overtime_flag = True
    for _ in range(AFTER_DUEL_ACTIVITY_MAX_TIMES):
        if img_search.afterDuelActivityNextFlag():
            overtime_flag = False
            break
        delay.random_float_delay(0.3, 0.2)
    
    if overtime_flag:
        raise img_search.ButtonNotFoundException("after duel activity next flag")

    for _ in range(AFTER_DUEL_ACTIVITY_MAX_TIMES):
        if not img_search.afterDuelActivityNextFlag():
            return
        clickRandomPos((pos[0] + 2, pos[1] + 2), 86, 16)
        delay.random_float_delay(0.3, 0.2)
        
    raise img_search.ButtonNotFoundException("after duel activity next flag")

def endDuel():
    pos = img_search.pos_rel2abs(DUEL_END_POS)
    clickRandomPos((pos[0] + 2, pos[1] + 2), 81, 16)
    delay.random_float_delay(0.3, 0.5)

    afterDuelNext()
    afterDuelNext()

    afterDuelActivityNext()
    