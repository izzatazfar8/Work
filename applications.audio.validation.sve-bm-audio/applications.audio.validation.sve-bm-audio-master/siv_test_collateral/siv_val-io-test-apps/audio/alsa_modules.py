# Unloading/loading ALSA or Module
# 
# Author: Athirah Basir
# Created: 12 DEC 2019

#Last Edit: Zulhisham, Izzat Azfar (Modified script to make it able to run from THM.

import os
import argparse
import sys
import re
import subprocess
import paramiko


workingDir = "/home/siv_test_collateral/siv_val-io-test-apps/audio/"
dev_1_ip = "10.221.120.134"
gcs_port = "2300" # GenericCommandServer default port is 2300

#Module directory
sut_mod_dir = "/home/siv_test_collateral/siv_val-io-test-apps/audio/sut_check_modules.log"
f_sut_dir = "/home/siv_test_collateral/siv_val-io-test-apps/audio/f_sut_check_modules.log"

#Alsa directory
sut_alsa_dir = "/home/siv_test_collateral/siv_val-io-test-apps/audio/sut_check_alsa.log"
f_alsa_dir = "/home/siv_test_collateral/siv_val-io-test-apps/audio/f_sut_check_alsa.log"

host_dir = "/home/siv_test_collateral/siv_val-io-test-apps/audio/"
alsa_alsa_dir = "/home/siv_test_collateral/siv_val-io-test-apps/audio/alsa.log"



script_name = str(sys.argv[0])
usage = "python unloading/loading.py -c modules / ALSA"

parser = argparse.ArgumentParser(prog=script_name,
                                 formatter_class=argparse.RawTextHelpFormatter,
                                 description=usage)

parser.add_argument('-c', metavar='--checker', help='modules or ALSA')
parser.add_argument('-i', help='dut IP')
parser.add_argument('-un','--username',help='Target machine username',default='root')
parser.add_argument('-ps','--password',help='Target machine password',default='')


args = parser.parse_args()

print(sys.argv[0:])

target_user = args.username
target_pass = args.password
dev_1_ip = args.i

"""
def Start_GenericCommandServer():
    command = os.popen('ps ax').read()
    #print("command:"+command)
    read_list = re.compile("\n").split(command)
    generic = True
    for line in read_list:
        if re.search("GenericCommandServer", line):
            print("GenericCommandServer is Already Running")
            generic = False
            break
    if generic:
        subprocess.Popen(["python", workingDir+"GenericCommandServer.py"])
        subprocess.call(["echo", "genericcommandserver is started"])
    else:
        print("done")
"""


#Start_GenericCommandServer()
dut = paramiko.SSHClient()
dut.set_missing_host_key_policy(paramiko.AutoAddPolicy())
dut.connect(hostname=dev_1_ip,username=target_user,password=target_pass,allow_agent=False,look_for_keys=False)


#1.2 function for check module
def alsa_checker():
    stdin,stdout,stderr = dut.exec_command("rm -rf /home/siv_test_collateral/siv_val-io-test-apps/audio/sut_check_alsa.log; rm -rf /home/siv_test_collateral/siv_val-io-test-apps/audio/f_sut_check_alsa.log")
    print("----- KMB ALSA  -----")

    
    if (os.path.isfile("/home/siv_test_collateral/siv_val-io-test-apps/audio/check_alsa.log")==0):
        print("Check Alsa file is missing !!! Exiting ...")
        sys.exit(0)

    stdin,stdout,stderr = dut.exec_command("dmesg | grep -i sound > /home/siv_test_collateral/siv_val-io-test-apps/audio/alsa.log")
    os.system("scp root@"+dev_1_ip+":"+alsa_alsa_dir+" "+host_dir)
    with open('/home/siv_test_collateral/siv_val-io-test-apps/audio/alsa.log') as file:
        contents = file.read()
        search_word = "Advanced Linux Sound Architecture Driver Initialized"
        if search_word in contents:
            print("Alsa checker : PASS \n")
        else:
            print ('Alsa checker : FAIL \n')
        

def modules_filter():
    print("-----Module Built-In: -----")

    stdin,stdout,stderr = dut.exec_command('cat /home/siv_test_collateral/siv_val-io-test-apps/audio/sut_check_modules.log | cut -d " " -f 1 >> /home/siv_test_collateral/siv_val-io-test-apps/audio/f_sut_check_modules.log')
    
        
    
    with open("/home/siv_test_collateral/siv_val-io-test-apps/audio/sut_check_modules.log", "r") as fil:
         data = fil.readlines()
    
         for line in data:
             words = line.split()
             #print words[0]
             with open("/home/siv_test_collateral/siv_val-io-test-apps/audio/f_sut_check_modules.log", "a") as fil2:
                 fil2.write(words[0])
                 fil2.write("\n")

    os.system("scp root@"+dev_1_ip+":"+sut_mod_dir+" "+host_dir)
    os.system("scp root@"+dev_1_ip+":"+f_sut_dir+" "+host_dir)

#sftp = dut.open_sftp()
#sftp.get(sut_mod_dir,host_dir)
#sftp.get(f_sut_dir,host_dir)
#sftp.close()

def modules_checker():
    stdin,stdout,stderr = dut.exec_command('uname -r')
    uname = stdout.read().decode("utf-8")
    uname = uname[:-1]

    stdin,stdout,stderr = dut.exec_command("rm -rf /home/siv_test_collateral/siv_val-io-test-apps/audio/sut_check_modules.log; rm -rf /home/siv_test_collateral/siv_val-io-test-apps/audio/f_sut_check_modules.log")
    #os.system("rm -rf /home/siv_test_collateral/siv_val-io-test-apps/audio/sut_check_modules.log; rm -rf /home/siv_test_collateral/siv_val-io-test-apps/audio/f_sut_check_modules.log")
    print("----- Modules Checking -----")

    
    if (os.path.isfile("/home/siv_test_collateral/siv_val-io-test-apps/audio/check_module.log")==0):
        print("Check Module file is missing !!! Exiting ...")
        sys.exit(0)

    stdin,stdout,stderr = dut.exec_command("cat /lib/modules/"+uname+"/modules.builtin | grep -i sound > /home/siv_test_collateral/siv_val-io-test-apps/audio/sut_check_modules.log")
    # os.system("cat /lib/modules/"+uname+"/modules.builtin | grep -i sound > /home/siv_test_collateral/siv_val-io-test-apps/audio/sut_check_modules.log")
    modules_filter()
    os.system("grep -Ff /home/siv_test_collateral/siv_val-io-test-apps/audio/f_sut_check_modules.log /home/siv_test_collateral/siv_val-io-test-apps/audio/check_module.log > /home/siv_test_collateral/siv_val-io-test-apps/audio/modules_compare.log")
    os.system("diff /home/siv_test_collateral/siv_val-io-test-apps/audio/modules_compare.log /home/siv_test_collateral/siv_val-io-test-apps/audio/check_module.log > /home/siv_test_collateral/siv_val-io-test-apps/audio/modules_compare1.log")
    #if os.system("du -k /home/siv_test_collateral/siv_val-io-test-apps/audio/modules_compare1.log | cut -f 1") == 0:
    if (os.stat("/home/siv_test_collateral/siv_val-io-test-apps/audio/modules_compare1.log").st_size == 0):
        mod_check = 1
        print("\n")
        print("Module checker : PASS \n")
    else:
        mod_check = 0
        print("\n")
        print("Module checker : FAIL \n")




print("----- Unloading/loading testing -----")

if args.c is None:
    print("Insufficient parameters !! ")
    sys.exit(0)
elif args.c == "modules":
    modules_checker()
elif args.c == "ALSA":
    alsa_checker()
elif args.i is not None:
    dev_1_ip = args.i
else:
    print("Invalid parameters !! ")
    sys.exit(0)



