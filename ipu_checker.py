import os
import argparse
import sys
# import logging
# import traceback
# import subprocess
# import re
import time
# from typing import TextIO

# import GenericCommand
# import string
# from datetime import date, datetime
# import signal

def driver_checker():
    print("----- IPU driver Checking -----")
    os.system("dmesg | grep ipu > /home/root/ipu.log")

    #verdict = false
    with open('/home/root/ipu.log') as f:
        if 'intel-ipu6 intel-ipu: enabling device' and 'intel-ipu6 intel-ipu: FW version' and 'intel-ipu6 intel-ipu: IPU driver' in f.read():
          print ("IPU Driver PASS")
        else:
          print ("IPU Driver FAILED")

def modules_checker():
    print("----- IPU Modules Checking -----")
    os.system("lsmod | grep ipu > /home/root/ipu_modules.log")

    #verdict = false
    with open('/home/root/ipu_modules.log') as f:
        if 'intel_ipu6_psys' and 'intel_ipu6_isys' and 'videobuf2_dma_contig' and 'videobuf2_v4l2' and 'videobuf2_common' and 'intel_ipu6' and 'ar0234' in f.read():
          print ("IPU Modules PASS")
        else:
          print ("IPU Modules FAILED")  
	 		 
def exposure():
    print("----- Exposure Checking -----")
    os.system("v4l2-ctl --all -d /dev/v4l-subdev5 > /home/root/exposure_check.log")

    #verdict = false
    with open('/home/root/exposure_check.log') as f:
        if 'exposure 0x00980911 (int)    : min=0 max=2355 step=2 default=2355 value=2355' in f.read():
          print ("Exposure PASS")
        else:
          print ("Exposure FAILED")	

def digital_gain():
    print("----- Digital Value Gain Checking -----")
    os.system("v4l2-ctl --all -d /dev/v4l-subdev5 > /home/root/digitalgain_check.log")

    #verdict = false
    with open('/home/root/digitalgain_check.log') as f:
        if 'digital_gain 0x009f0905 (int)    : min=0 max=2047 step=2 default=128 value=128' in f.read():
          print ("Digital Gain PASS")
        else:
          print ("Digital Gain FAILED")
          
def analog_gain():
    print("----- Analog Gain Value Checking -----")
    os.system("v4l2-ctl --all -d /dev/v4l-subdev5 > /home/root/analoggain_check.log")

    #verdict = false
    with open('/home/root/analoggain_check.log') as f:
        if 'analogue_gain 0x009e0903 (int)    : min=0 max=127 step=2 default=14 value=14' in f.read():
          print ("Analog Gain PASS")
        else:
          print ("Analog Gain FAILED")
          
def check_binary():
    print("----- Binary loaded Checking -----")
    os.system("dmesg | grep ipu > /home/root/check_binary.log")

    #verdict = false
    with open('/home/root/check_binary.log') as f:
        if 'cpd file name: intel/ipu6ep_fw.bin' in f.read():
          print ("Binary Loaded PASS")
        else:
          print ("Binary Loaded FAILED")
          
def main():
    print("----- IPU Module/Firmware Checking -----")
    script_name = str(sys.argv[0])
    usage = "python ipu_checker.py -c ipu_modules_checker"

    parser = argparse.ArgumentParser(prog=script_name,
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     description=usage)

    parser.add_argument('-c', metavar='--checker', help='driver/modules checker')


    args = parser.parse_args()

    print(sys.argv[0:])

    if args.c == "ipu_driver_checker":
        driver_checker()
    elif args.c == "ipu_modules_checker":
        modules_checker()
    elif args.c == "exposure":
        exposure()
    elif args.c == "digital_gain":
        digital_gain()
    elif args.c == "analog_gain":
        analog_gain()
    elif args.c == "check_binary":
        check_binary()
    else:
        print("Invalid parameters !! ")
        sys.exit(0)


main()
