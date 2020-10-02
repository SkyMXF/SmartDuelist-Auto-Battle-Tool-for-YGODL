import time
import random

def standard_delay(t):
    #print("Sleep %.4fs"%t)
    time.sleep(t)

def random_float_delay(t, float_region=0.1):
    float_time = random.random() * float_region * t
    #print("Sleep %.4f"%(t + float_time))
    time.sleep(t + float_time)