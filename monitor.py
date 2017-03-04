#!/usr/bin/python

from subprocess import call, check_output
import time
import shlex
import sys

import signal

def handler(signum, frame):
#   call(shlex.split("echo -ne '\e[u''\e[0m'"))
  sys.exit()

RED = "\e[1;31m"
GREEN = "\e[1;32m"
YELLOW = "\e[1;33m"

while True:
  temp_float = float(check_output(shlex.split("vcgencmd measure_temp"))[5:-3])
  temp = "T=" + str(temp_float) + '\'C'

  if (temp_float < 50.0):
    temp = GREEN + temp
  elif (temp_float < 70.0):
    temp = YELLOW + temp
  else:
    temp = RED + temp

  throttled_int = int(check_output(shlex.split("vcgencmd get_throttled"))[-2:])

  throttled = ""
  if (throttled_int & 0x1):
    throttled = throttled + RED + "V"
  else:
    throttled = throttled + GREEN + "V"
  if (throttled_int & 0x2):
    throttled = throttled + RED + "F"
  else:
    throttled = throttled + GREEN + "F"
  if (throttled_int & 0x4):
    throttled = throttled + RED + "T"
  else:
    throttled = throttled + GREEN + "T"

  freq_float = float(check_output(shlex.split("cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq"))) / 1000.0 / 1000.0;
  freq = "F=" + str(freq_float) + "G"

  if (freq_float < 0.8):
    freq = GREEN + freq
  elif (freq_float < 1.3):
    freq = YELLOW + freq
  else:
    freq = RED + freq

  echo_string = "\e[s\e[1;60H" + temp + " " + freq + " " + throttled + "\e[u\e[0m"

  call(["echo", "-ne", echo_string])

  # debug
  # print temp
  # print throttled
  # print freq
    
  time.sleep(1)

