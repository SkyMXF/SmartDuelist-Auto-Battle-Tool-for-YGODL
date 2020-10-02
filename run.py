import random
import time

import window
import street
import duel
import img_search
import delay

DEFAULT_EXCEPTION = img_search.ButtonNotFoundException

def auto_gate_duel():
    # enter gate
    if not street.isGatePage():
        reconnect_wrapper(street.streetToGate, 20)
    reconnect_wrapper(street.openGate, 20)
    reconnect_wrapper(street.waitGateOpen, 1)
    reconnect_wrapper(street.selectGateLevel10, 2)
    reconnect_wrapper(street.beginGateDuel, 2)
    street.skipTalking()
    reconnect_wrapper(street.duelReallyBegin, 3)

    # enter duel
    while True:
        duel.skipDuelAnimation()
        myMonSeats = img_search.getMyMonsterSeatsList()
        if False in myMonSeats:
            duel.selectMonster()
            duel.summonMonster()
            duel.skipDuelAnimation()
        if img_search.duelEnd():
            break
        duel.nextStage()
        duel.allMonsterAttack()
        duel.skipDuelAnimation()
        if img_search.duelEnd():
            break
        duel.nextStage()
    
    duel.endDuel()

def retry_wrapper(func, max_retry_times, exception=DEFAULT_EXCEPTION):
    """retry for several times, or raise the exception
    """
    retry_times = 0
    finished, e = try_once(func, exception)
    while not finished:
        retry_times += 1
        if retry_times > max_retry_times:
            raise e
        finished, e = try_once(func, exception)

def try_once(func, exception):
    """kernel function for retry_wrapper
    """
    try:
        func()
    except exception as e:
        return False, e
    return True, exception()

def reconnect_wrapper(func, max_retry_times, exception=DEFAULT_EXCEPTION):
    try:
        retry_wrapper(func, max_retry_times, exception=exception)
    except DEFAULT_EXCEPTION as e:
        if img_search.isDisconnected():
            street.reconnect()
            retry_wrapper(func, max_retry_times, exception=exception)
        else:
            raise e

if __name__ == "__main__":

    window.activeGameWindow()
    delay.standard_delay(1.0)
    auto_gate_duel()