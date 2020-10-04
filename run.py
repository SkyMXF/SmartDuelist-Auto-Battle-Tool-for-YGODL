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
    time_str = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print("[%s]Entering gate..."%(time_str))
    duel.afterDuelActivityNext()
    if not street.isGatePage():
        reconnect_wrapper(street.streetToGate, 20)
    reconnect_wrapper(street.openGate, 1)
    reconnect_wrapper(street.selectGateLevel10, 2)
    reconnect_wrapper(street.beginGateDuel, 2)
    street.skipTalking()
    reconnect_wrapper(street.duelReallyBegin, 3)

    # enter duel
    time_str = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print("[%s]Duel!"%(time_str))
    while True:
        duel.skipDuelAnimation()
        myMonSeats = img_search.getMyMonsterSeatsList()
        if False in myMonSeats:
            time_str = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            print("[%s]Find empty seat, summon a monster..."%(time_str))
            duel.selectMonster()
            duel.summonMonster()
            duel.skipDuelAnimation()
        else:
            time_str = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            print("[%s]No empty seat"%(time_str))
        if img_search.duelEnd():
            break
        stage_id = duel.nextStage()
        if stage_id == 1:   # already end stage
            time_str = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            print("[%s]End round."%(time_str))
            continue
        
        time_str = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        print("[%s]Battle da!"%(time_str))
        duel.allMonsterAttack()
        duel.skipDuelAnimation()
        if img_search.duelEnd():
            break
        duel.nextStage()
        time_str = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        print("[%s]End round."%(time_str))
    
    time_str = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print("[%s]Duel end."%(time_str))
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
            time_str = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            print("[%s]Disconnected. Trying to reconnect..."%(time_str))
            street.reconnect()
            retry_wrapper(func, max_retry_times, exception=exception)
        else:
            raise e

if __name__ == "__main__":

    window.activeGameWindow()
    delay.standard_delay(1.0)

    battle_counter = 0
    while True:
        auto_gate_duel()
        battle_counter += 1
        time_str = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        print("[%s]Already finished %d duels."%(time_str, battle_counter))