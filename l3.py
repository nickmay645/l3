#!/usr/bin/env python3 #the script is python3
import logging
import time
import math
import decimal

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.syncLogger import SyncLogger
import sys


class ExecutionTime:
    def __init__(self):
        self.start_time = time.time()

    def duration(self):
        return time.time() - self.start_time


# Only output errors from the logging framework
timer = ExecutionTime()
# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)



def takeOff(cf, t, height):
    steps = t * 10
    div = steps / height
    for z in range(steps):
        cf.commander.send_hover_setpoint(0, 0, 0, z/div)
        time.sleep(0.1)
    cf.commander.send_hover_setpoint(0, 0, 0, height)
    time.sleep(0.1)

def land(cf, t, height):
    steps = t * 10
    div = steps / (height + 0.1)
    for z in range(steps):
        cf.commander.send_hover_setpoint(0, 0, 0, (height+0.1) - (z/div))
        time.sleep(0.1)
    
def left(cf, t, deg, height):
    steps = t * 10
    for _ in range(steps):
        cf.commander.send_hover_setpoint(0, deg, 0, height)
        time.sleep(0.1)

def right(cf, t, deg, height):
    steps = t * 100
    for _ in range(steps):
        cf.commander.send_hover_setpoint(0, -deg, 0, height)
        time.sleep(0.01)

def up(cf, t, start, end):
    steps = t * 10
    dif = end - start
    div = steps / dif
    for h in range(steps):
        cf.commander.send_hover_setpoint(0, 0, 0, start + (h/div))
        time.sleep(0.1)
    cf.commander.send_hover_setpoint(0, 0, 0, end)
    time.sleep(0.1)

def down(cf, t, start, end):
    steps = t * 10
    dif = end - start
    div = steps / dif
    for h in range(steps):
        cf.commander.send_hover_setpoint(0, 0, 0, start + (h/div))
        time.sleep(0.1)
    cf.commander.send_hover_setpoint(0, 0, 0, end)
    time.sleep(0.1)

def posHold(cf, t, height):
    steps = 100 * t
    for _ in range(steps):
        cf.commander.send_hover_setpoint(0, 0, 0, height)
        time.sleep(0.01)

def hover(cf):
    takeOff(cf, 1, 0.4)
    posHold(cf, 1, 0.4)
    for _ in range(5):
        right(cf,1,0.7,0.4)
        left(cf,1,0.7,0.4)
    posHold(cf, 1, 0.4)
    land(cf, 1, 0.4)

def basicLoop(cf):
    height = 0.4
    takeOff(cf,1,height)
    posHold(cf,3,height)
    for x in range(3):
        print("Pass: %i" % int(x+1), "of 3")
        right(cf,6,0.08,height)
        down(cf,2,height,height-0.1)
        left(cf, 6, 0.08, height-0.1)
        up(cf,2,height-0.1,height)
        posHold(cf, 2, height)
    print('Landing, reorientate drone.')    
    land(cf,1,height)

def batt(uri):
    # Only output errors from the logging framework
    logging.basicConfig(level=logging.ERROR)


    # Initialize the low-level drivers (don't list the debug drivers)
    cflib.crtp.init_drivers(enable_debug_driver=False)
    # Scan for Crazyflies and use the first one found
    lg_batt = LogConfig(name='Battery', period_in_ms=10)
    lg_batt.add_variable('pm.vbat', 'float')    
    lg_batt.add_variable('pm.state', 'float')

   
    cf = Crazyflie(rw_cache='./cache')
    with SyncCrazyflie(uri, cf=cf) as scf:
        with SyncLogger(scf, lg_batt) as logger:


            for log_entry in logger:
                timestamp = log_entry[0]
                data = log_entry[1]['pm.vbat']
                logconf_name = log_entry[2]
                print("Battery is %i %% "  % ((data/4.2)*100), "at %0.2f V" % data)
                break




def run(uri):
    cflib.crtp.init_drivers(enable_debug_driver=False)
    
    with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:
        cf = scf.cf

        cf.param.set_value('kalman.resetEstimation', '1')
        time.sleep(0.1)
        cf.param.set_value('kalman.resetEstimation', '0')
        time.sleep(2)

        for x in range(4):
            print("Loop: %i" % int(x+1), "of 4")
            basicLoop(cf)
            if(x != 3):
                time.sleep(11)
        
        #hover(cf)
        
        cf.commander.send_stop_setpoint()
        print('Finished in %i min %0.1f sec ' % (timer.duration()/60, timer.duration()%60))



                  



# ================= MAIN ================= #
running = 1
while(running):
    print('\n\n\nL3 Crazyflie Controller')
    print('----------------------------')
    uriBase = 'radio://0/80/2M/E7E7E7E7'
    droneNum =input('Drone number: ')
    URIcomplete = uriBase + droneNum
    print('1) Check Battery\n2) Run Sequence\n3) Quit\n')
    choice = int(input())
    if (choice == 1):
        print('Checking Battery...')
        time.sleep(0.5)
        batt(URIcomplete)
        #stuff
    elif (choice == 2):
        print('Running Sequence...')
        time.sleep(0.5)
        run(URIcomplete)
    elif(choice == 3):
        running = 0
        print('Quitting...')
        time.sleep(0.5)
    else:
        print('Choice not valid. Please try again.')
          

