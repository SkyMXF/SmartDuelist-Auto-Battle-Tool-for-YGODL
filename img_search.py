import os
from python_imagesearch import imagesearch

import delay
import window

template_dir = "templates"

DUEL_STAGE_SWITCH_RECT = (641, 339, 775, 453)
MONSTER_SELECTED_FLAG_RECT = (437, 418, 513, 491)
DUEL_FINISH_FLAG_RECT = (441, 556, 588, 598)
DUEL_FINISH_NEXT_RECT = (443, 557, 588, 602)
AFTER_DUEL_ACTIVITY_NEXT_RECT = (442, 463, 592, 508)

MY_MONSTER_SEATS_RECT = [(415, 315, 487, 408), (475, 315, 557, 408), (544, 315, 618, 408)]
OPPO_MONSTER_SEATS_RECT = [(420, 197, 450, 275), (482, 200, 550, 276), (544, 200, 610, 277)]

class ButtonNotFoundException(Exception):
    def __init__(self, button_subs="unknown button"):
        super(ButtonNotFoundException, self)
        self.button_subs = str(button_subs)
    
    def __str__(self):
        return "Button not found: %s"%(self.button_subs)

def pos_rel2abs(pos):
    if len(pos) == 2:
        return (pos[0] + window.game_window_rect[0], pos[1] + window.game_window_rect[1])
    elif len(pos) == 4:
        return (
            pos[0] + window.game_window_rect[0],
            pos[1] + window.game_window_rect[1],
            pos[2] + window.game_window_rect[0],
            pos[3] + window.game_window_rect[1]
        )

def isDisconnected():
    pos = imagesearch.imagesearcharea(
        os.path.join(template_dir, "disconnect.png"),
        *window.game_window_rect
    )
    if pos[0] == -1:
        return False
    return True

def findGate():
    gate_template_dir = os.path.join(template_dir, "gate")
    gate_list = ["gatedm.png", "gatedsod.png", "gategx.png", "gate5ds.png", "gatezexal.png"]
    for gate_name in gate_list:
        pos = imagesearch.imagesearcharea(
            os.path.join(gate_template_dir, gate_name),
            *window.game_window_rect,
            precision=0.6
        )
        if pos[0] != -1:
            break
    if pos[0] == -1:
        raise ButtonNotFoundException("gate")
    
    return pos_rel2abs(pos)

def isGatePageSelected():
    pos = imagesearch.imagesearcharea(
        os.path.join(template_dir, "gatePageOpen.png"),
        *window.game_window_rect
    )
    return pos[0] != -1

def isGateOpen():
    pos = imagesearch.imagesearcharea(
        os.path.join(template_dir, "gateBeginDuel.png"),
        *window.game_window_rect
    )
    return pos[0] != -1

def talkingEnd():
    pos = imagesearch.imagesearcharea(
        os.path.join(template_dir, "duelRealBegin.png"),
        *window.game_window_rect
    )
    return pos[0] != -1

def duelAnimationEnd():
    pos = imagesearch.imagesearcharea(
        os.path.join(template_dir, "duelStageSwitch.png"),
        *pos_rel2abs(DUEL_STAGE_SWITCH_RECT)
    )
    return pos[0] != -1

def duelEnd():
    pos = imagesearch.imagesearcharea(
        os.path.join(template_dir, "duelFinished.png"),
        *pos_rel2abs(DUEL_FINISH_FLAG_RECT)
    )
    return pos[0] != -1

def duelEndNextFlag():
    pos = imagesearch.imagesearcharea(
        os.path.join(template_dir, "duelEndNext.png"),
        *pos_rel2abs(DUEL_FINISH_NEXT_RECT)
    )
    return pos[0] != -1

def afterDuelActivityNextFlag():
    pos = imagesearch.imagesearcharea(
        os.path.join(template_dir, "afterDuelActivityNext.png"),
        *pos_rel2abs(AFTER_DUEL_ACTIVITY_NEXT_RECT)
    )
    if pos[0] != -1:
        return True
        
    pos = imagesearch.imagesearcharea(
        os.path.join(template_dir, "afterDuelActivityNext2.png"),
        *pos_rel2abs(AFTER_DUEL_ACTIVITY_NEXT_RECT)
    )
    return pos[0] != -1

def monsterSelected():
    pos = imagesearch.imagesearcharea(
        os.path.join(template_dir, "monsterSelectedFlag.png"),
        *pos_rel2abs(MONSTER_SELECTED_FLAG_RECT),
        precision=0.6
    )
    return pos[0] != -1

def getMyMonsterSeatsList():
    seats_list = []
    for seat_id in range(1, 4):
        pos = imagesearch.imagesearcharea(
            os.path.join(template_dir, "emptySeatMyMon%d.png"%(seat_id)),
            *pos_rel2abs(MY_MONSTER_SEATS_RECT[seat_id - 1]),
            precision=0.5
        )
        seats_list.append(pos == -1)

    return seats_list

def getOppoMonsterSeatsList():
    seats_list = []
    for seat_id in range(1, 4):
        pos = imagesearch.imagesearcharea(
            os.path.join(template_dir, "emptySeatOppoMon%d.png"%(seat_id)),
            *pos_rel2abs(OPPO_MONSTER_SEATS_RECT[seat_id - 1])
        )
        seats_list.append(pos == -1)

    return seats_list