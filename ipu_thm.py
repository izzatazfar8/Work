
import os, re, sys, time, argparse, subprocess, time
from invoke import UnexpectedExit
import paramiko

destPath = "/home/test/siv_test_collateral/siv_val-io-test-apps/audio"
file_to_check = "/home/Audio_checker.py"
script_name = str(sys.argv[0])
usage = "# python /home/THM/automation_script/Audio_checker_THM.py <IP> <option>"
parser = argparse.ArgumentParser(prog=script_name, description=usage)
parser.add_argument('-sut_ip', help='SUT IP')
parser.add_argument('-thm_ip', help='THM IP')
#parser.add_argument('-op', help='Option = [modules_checker, alsa_checker, 16bits, 32bits]')
parser.add_argument('-op', help='Option = [playback, driver_check]')

args = parser.parse_args()


#python3 /home/siv_test_collateral/siv_val-io-test-apps/audio/new_audio_thm_checker.py -sut_ip 172.30.248.25 -op playback -drv HDA -bitdepth 32 -khz 48 -ch 2

target_user = 'root'
target_pass = ''

if args.sut_ip is not None:
    sut_ip = args.sut_ip
else:
    print ("-sut_ip missing")
    sys.exit(1)

if args.op is not None:
     option = args.op
else:
     print ("-op missing")
     sys.exit(1)

sut = paramiko.SSHClient()
sut.set_missing_host_key_policy(paramiko.AutoAddPolicy())
sut.connect(hostname=sut_ip,port=22,username=target_user,password=target_pass,allow_agent=False,look_for_keys=False)
# proc = subprocess.Popen(["prog", "arg"], stdout=subprocess.PIPE)
host,port = sut_ip,22
# transport = paramiko.Transport((host,port))
# username,password = "root",""
# transport.connect(None,username,password)
# sftp = paramiko.SFTPClient.from_transport(transport)

def main():

    if option == "ipu_driver_checker":
        stdin, stdout, stderr = sut.exec_command("python3 /home/root/ipu_checker.py -c ipu_driver_checker")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)

    elif option == "ipu_modules_checker":
        stdin, stdout, stderr = sut.exec_command("python3 /home/root/ipu_checker.py -c ipu_modules_checker")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
		
    elif option == "playback":
        stdin, stdout, stderr = sut.exec_command("python3 /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/new_audio_SUT_checker.py -op " + option + " -drv " +Driver + " -b " + bitdepth + " -s " + rate + " -ch " + channel)
        execcommand = ("python3 /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/new_audio_SUT_checker.py -op " + option + " -drv " +Driver + " -b " + bitdepth + " -s " + rate + " -ch " + channel)
        print (execcommand)
		
        #stdin, stdout, stderr = sut.exec_command("python3 /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/new_audio_SUT_checker.py -op playback -drv HDA -b 32 -s 48 #-ch 2")
		
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)

main()
