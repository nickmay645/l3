# -*- coding: utf-8 -*-
#
#     ||          ____  _ __
#  +------+      / __ )(_) /_______________ _____  ___
#  | 0xBC |     / __  / / __/ ___/ ___/ __ `/_  / / _ \
#  +------+    / /_/ / / /_/ /__/ /  / /_/ / / /_/  __/
#   ||  ||    /_____/_/\__/\___/_/   \__,_/ /___/\___/
#
#  Copyright (C) 2016 Bitcraze AB
#
#  Crazyflie Nano Quadcopter Client
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA  02110-1301, USA.
"""
Simple example that connects to the crazyflie at `URI` and runs a figure 8
sequence. This script requires some kind of location system, it has been
tested with (and designed for) the flow deck.

Change the URI variable to your Crazyflie configuration.
"""
import logging
import time
import math

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie


# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

def box(cf):

    for _ in range(10):
        cf.commander.send_hover_setpoint(0, 0.5, 0, 0.6)
        time.sleep(0.1)


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
    div = steps / height
    for z in range(steps):
        cf.commander.send_hover_setpoint(0, 0, 0, height - (z/div))
        time.sleep(0.1)
    cf.commander.send_hover_setpoint(0, 0, 0, 0)
    time.sleep(0.1)


def left(cf, t, deg, height):
    steps = t * 10
    for _ in range(steps):
        cf.commander.send_hover_setpoint(0, deg, 0, height)
        time.sleep(0.1)

def right(cf, t, deg, height):
    steps = t * 10
    for _ in range(steps):
        cf.commander.send_hover_setpoint(0, -deg, 0, height)
        time.sleep(0.1)


def up(cf, t, start, end):
    steps = t * 10
    dif = end - start
    div = steps / dif
    for h in range(steps):
        #print(start + (h/div))
        cf.commander.send_hover_setpoint(0, 0, 0, start + (h/div))
        time.sleep(0.1)
    cf.commander.send_hover_setpoint(0, 0, 0, end)
    time.sleep(0.1)

def down(cf, t, start, end):
    steps = t * 10
    dif = end - start
    div = steps / dif
    for h in range(steps):
        #print(start - (h/div))
        cf.commander.send_hover_setpoint(0, 0, 0, start + (h/div))
        time.sleep(0.1)
    cf.commander.send_hover_setpoint(0, 0, 0, end)
    time.sleep(0.1)

def posHold(cf, t, height):
    steps = 10 * t
    for _ in range(steps):
        cf.commander.send_hover_setpoint(0, 0, 0, height)
        time.sleep(0.1)


def circle(cf):
    damp_roll = 1

    def heightmod(hi):
        damp = 4
        base = 0.2
        val = (hi/damp) + base
        return val


    for angle in range(90):
        r = math.cos(math.radians(angle))/damp_roll
        h = math.sin(math.radians(angle*2))
        cf.commander.send_hover_setpoint(0, r, 0, heightmod(h))
        time.sleep(0.01)

        #print(r1, h1)
    #print("2 \n\n")
    for angle in range(45):
        r = -1 * math.sin(math.radians(angle))/damp_roll
        h = 1 + math.sin(math.radians(angle))
        cf.commander.send_hover_setpoint(0, r, 0, heightmod(h))
        time.sleep(0.01)

        #print(r2, h2)
    #print("3 \n\n")
    for angle in range(45):
        r = -1 * math.cos(math.radians(angle))/damp_roll
        h = 2 - math.sin(math.radians(angle))
        cf.commander.send_hover_setpoint(0, r, 0, heightmod(h))
        time.sleep(0.01)

        #print(r3, h3)
    #print("4 \n\n")
    for angle in range(45):
        r = math.sin(math.radians(angle*2))/damp_roll
        h = math.cos(math.radians(angle*2))
        #print(r4, h4)
        cf.commander.send_hover_setpoint(0, r, 0, heightmod(h))
        time.sleep(0.01)

def minuteSequenceA(cf):
        takeOff(cf, 1, 0.2)
        left(cf,1,0.2,0.15)


        #loops back and forth
        loops = 15
        t_est_min = (loops * 14) / 60
        t_est_sec = (loops * 14) % 60
        print("Time est: %i" % t_est_min, "min %i" % t_est_sec, "sec")

        for x in range(loops):
            l = x + 1
            print("Loop: %i is running" % l)
            #posHold(cf, 1, 0.3)
            right(cf, 2, 0.25, 0.15)
            up(cf, 1, 0.15, 0.4)
            #posHold(cf, 1, 0.4)
            left(cf, 2, 0.25, 0.4)
            down(cf, 1, 0.4, 0.15)


        #landing
        right(cf,1,0.2,0.15)
        land(cf,2,0.15)


        cf.commander.send_stop_setpoint()


def run():
    cflib.crtp.init_drivers(enable_debug_driver=False)

    URI1 = 'radio://0/80/2M/E7E7E7E766'

    with SyncCrazyflie(URI1, cf=Crazyflie(rw_cache='./cache')) as scf:
        cf = scf.cf

        cf.param.set_value('kalman.resetEstimation', '1')
        time.sleep(0.1)
        cf.param.set_value('kalman.resetEstimation', '0')
        time.sleep(2)


        minuteSequenceA(cf)


        cf.commander.send_stop_setpoint()

run()