import logging
import time
import decimal

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.syncLogger import SyncLogger

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)


# Initialize the low-level drivers (don't list the debug drivers)
cflib.crtp.init_drivers(enable_debug_driver=False)
# Scan for Crazyflies and use the first one found
lg_batt = LogConfig(name='Battery', period_in_ms=10)
lg_batt.add_variable('pm.vbat', 'float')
lg_batt.add_variable('pm.state', 'float')

URI1 = 'radio://0/80/2M/E7E7E7E766'
URI2 = 'radio://0/80/250K'

cf = Crazyflie(rw_cache='./cache')
with SyncCrazyflie(URI2, cf=cf) as scf:
    with SyncLogger(scf, lg_batt) as logger:


        for log_entry in logger:
            timestamp = log_entry[0]
            data = log_entry[1]['pm.vbat']
            logconf_name = log_entry[2]
            print("%0.2f" % data)
            if data > 4.10:
                print("%0.2f" % data)





