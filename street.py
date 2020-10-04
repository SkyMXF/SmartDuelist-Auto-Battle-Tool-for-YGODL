import pyautogui
import random

import window
import img_search
import delay

GATE_POS = (337, 580)#25x25
PVP_POS = (440, 580)
SHOP_POS = (535, 580)
WORKSHOP_POS = (556, 580)

GATE_POS = (563, 260)#40x40
GATE_LEVEL_10_POS = (392, 418)#25x20
GATE_DUEL_START_POS = (449, 523)#140x20

WAIT_FOR_GATE_MAX_TIMES = 15
WAIT_FOR_GATE_PAGE_MAX_TIMES = 3
RECONNECT_POS = (535, 340)#100x30

SKIP_TALKING_POS = (328, 224)#50x50
SKIP_TALKING_MAX_TIMES = 30

DUEL_REALLY_BEGIN_POS = (452, 524)#125x20

def clickRandomPos(pos, x_move_max, y_move_max):
    x_move = random.randint(0, x_move_max)
    y_move = random.randint(0, y_move_max)
    pyautogui.moveTo(pos[0] + x_move, pos[1] + y_move)
    delay.standard_delay(0.1)
    pyautogui.click()

def streetToGate():
    pos = img_search.pos_rel2abs(GATE_POS)
    clickRandomPos((pos[0] + 5, pos[1] + 5), 15, 15)
    delay.random_float_delay(0.8, 0.2)
    
def streetToPVP():
    pos = img_search.pos_rel2abs(PVP_POS)
    clickRandomPos((pos[0] + 5, pos[1] + 5), 15, 15)
    delay.random_float_delay(0.8, 0.2)

def streetToShop():
    pos = img_search.pos_rel2abs(SHOP_POS)
    clickRandomPos((pos[0] + 5, pos[1] + 5), 15, 15)
    delay.random_float_delay(0.8, 0.2)

def streetToWorkshop():
    pos = img_search.pos_rel2abs(WORKSHOP_POS)
    clickRandomPos((pos[0] + 5, pos[1] + 5), 15, 15)
    delay.random_float_delay(0.8, 0.2)

def isGatePage():
    for _ in range(WAIT_FOR_GATE_PAGE_MAX_TIMES):
        if img_search.isGatePageSelected():
            return True
        delay.random_float_delay(0.5, 0.5)
        
    # retry too much times
    return False

def openGate():
    pos = img_search.pos_rel2abs(GATE_POS)
    for _ in range(WAIT_FOR_GATE_MAX_TIMES):
        if img_search.isGateOpen():
            return
        clickRandomPos((pos[0] + 5, pos[1] + 5), 30, 30)
        delay.random_float_delay(1.0, 0.2)

    # retry too much times
    raise img_search.ButtonNotFoundException("gate open flag")

def selectGateLevel10():
    pos = img_search.pos_rel2abs(GATE_LEVEL_10_POS)
    clickRandomPos((pos[0] + 5, pos[1] + 5), 15, 10)
    delay.random_float_delay(0.3, 0.2)

def beginGateDuel():
    pos = img_search.pos_rel2abs(GATE_DUEL_START_POS)
    clickRandomPos((pos[0] + 20, pos[1] + 5), 100, 10)
    delay.random_float_delay(0.5, 0.2)

def reconnect():
    pos = img_search.pos_rel2abs(RECONNECT_POS)
    clickRandomPos((pos[0] + 10, pos[1] + 5), 80, 20)
    delay.random_float_delay(0.5, 0.2)

def skipTalking():
    pos = img_search.pos_rel2abs(SKIP_TALKING_POS)

    for _ in range(SKIP_TALKING_MAX_TIMES):
        if img_search.talkingEnd():
            return
        clickRandomPos((pos[0] + 10, pos[1] + 10), 30, 30)
        delay.random_float_delay(0.2, 0.2)
        
    # retry too much times
    raise img_search.ButtonNotFoundException("talking end flag")

def duelReallyBegin():
    pos = img_search.pos_rel2abs(DUEL_REALLY_BEGIN_POS)
    clickRandomPos((pos[0] + 10, pos[1] + 5), 105, 10)
    delay.random_float_delay(0.8, 0.2)