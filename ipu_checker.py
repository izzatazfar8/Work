
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
	 		 
	
 	
def main():
    print("----- Audio Built In driver testing -----")
    script_name = str(sys.argv[0])
    usage = "python Audio_checker.py -c modules"
    usage = "python Audio_checker.py -b 16 -s 48"

    parser = argparse.ArgumentParser(prog=script_name,
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     description=usage)

    parser.add_argument('-c', metavar='--checker', help='modules')
    parser.add_argument('-b', metavar='--checker', help='bit_depth')
    parser.add_argument('-s', metavar='--checker', help='sampling_rate')

    args = parser.parse_args()

    print(sys.argv[0:])

    if args.c == "ipu_driver_checker":
        driver_checker()
    elif args.c == "ipu_modules_checker":
        modules_checker()

    else:
        print("Invalid parameters !! ")
        sys.exit(0)


main()
