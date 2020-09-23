#!/usr/bin/env python3

import urx
import threading
import time
import os

is_vibrating = False 

def get_fh(run):
    fh = open(f"hack/configurations-{run}.csv", 'w')
    fh.write('is_vibrating, x, y, z, rx, ry, rz, base, shoulder, elbow, wrist_1, wrist_2, wrist_3\n')
    return fh

def record_configuration():
    max_lines = 5
    has_vibrated = False
    line = 0
    run = 0
    fh = get_fh(run)
    try:
        while True:

            line += 1
            if line == max_lines:
                fh.close()
                fh = get_fh(run)

                if not has_vibrated:
                    os.remove(f"hack/configurations-{run}.csv")

                run += 1
                line = 0
                has_vibrated = False

            if is_vibrating:
                has_vibrated = True

            location = robot.getl()
            joints = robot.getj()
            template = "{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}\n" 
            record = template.format(is_vibrating, *location, *joints)
            fh.write(record)
            time.sleep(0.1)
    except ValueError:
        pass

robot = urx.Robot('192.168.5.42')
time.sleep(2)  #leave some time to robot to process the setup commands

r_th = threading.Thread(target=record_configuration)
r_th.start()

while True:
    i = input("is_vibrating: (y/n) ")
    if i == 'y':
        is_vibrating = True
    elif i == 'n':
        is_vibrating = False
