# For alsa utility test
# 
# Author: Athirah Basir
# Last updated: 17 Feb 2020

import os
import argparse
import sys


def alsa_checker():
	os.system("rm -rf /home/siv_test_collateral/siv_val-io-test-apps/audio/sut_check_alsa_utility.log")
	print "----- Checking ALSA -----"

	if (os.path.isfile("/home/siv_test_collateral/siv_val-io-test-apps/audio/check_alsa_utility.log")==0):
		print "THM file is missing !!! Exiting ..."
		sys.exit(0)

	os.system("amixer -c0 scontrols > /home/siv_test_collateral/siv_val-io-test-apps/audio/sut_check_alsa_utility.log")
	os.system("diff /home/siv_test_collateral/siv_val-io-test-apps/audio/check_alsa_utility.log /home/siv_test_collateral/siv_val-io-test-apps/audio/sut_check_alsa_utility.log > /home/siv_test_collateral/siv_val-io-test-apps/audio/alsa_utility_compare.log") 
	if (os.stat("/home/siv_test_collateral/siv_val-io-test-apps/audio/alsa_utility_compare.log").st_size == 0):
		alsa_check = 1
		print "Alsa utility_checker : PASS"
	else:
		alsa_check = 0
		print "Alsa utility_checker : FAIL"


def main():
    print "----- ALSA utility testing -----"
    script_name = str(sys.argv[0])
    usage="python alsa_utility.py -c alsamixer"

    parser = argparse.ArgumentParser(prog = script_name,
                                 formatter_class=argparse.RawTextHelpFormatter,
                                 description = usage)

    parser.add_argument('-c', metavar='--checker', help='alsamixer')

    args = parser.parse_args()

    print sys.argv[0:]

    if args.c is None:
        print "Insufficient parameters !! "
        sys.exit(0)
    elif args.c == "alsamixer":
        alsa_checker()
    else:
        print "Invalid parameters !! "
        sys.exit(0)


main();

