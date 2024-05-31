# jepson
# python3, replace GenericCommand and ssh_util using fabric
import os, re, sys, time, argparse, subprocess, time
from fabric2 import Connection
from fabric.api import run, env, settings, put, execute
# from fabric.operation import run, put
from fabric.contrib.files import exists
from invoke import UnexpectedExit
import paramiko

destPath = "/home/test/siv_test_collateral/siv_val-io-test-apps/audio"
file_to_check = "/home/Audio_checker.py"
script_name = str(sys.argv[0])
usage = "# python /home/THM/automation_script/Audio_checker_THM.py <IP> <option>"
parser = argparse.ArgumentParser(prog=script_name, description=usage)
parser.add_argument('-sut_ip', help='SUT IP')
parser.add_argument('-thm_ip', help='THM IP')
parser.add_argument('-op', help='Option = [modules_checker, alsa_checker, 16bits, 32bits]')
args = parser.parse_args()

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

# sut = Connection(host=sut_ip,user=user,connect_kwargs=con_kwargs)

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

    #print("\nCopying scripts to SUT...\n")
    #stdin, stdout, stderr = sut.exec_command("rm -r /home/siv_test_collateral_audio_SUT")
    #time.sleep(3)
    #os.system("scp -r /home/siv_test_collateral/siv_val-io-test-apps/audio/siv_test_collateral_audio_SUT root@" + sut_ip + ":/home/")
    #time.sleep(3)

    if option == "modules_checker":
        stdin, stdout, stderr = sut.exec_command("python3 /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/ww18_sut_audio.py -c modules")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)

    elif option == "alsa_checker":
        stdin, stdout, stderr = sut.exec_command("python3 /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/ww18_sut_audio.py -c alsa")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)

    elif option == "16bits":
        stdin, stdout, stderr = sut.exec_command("python3 /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/ww18_sut_audio.py -b 16 -s 48")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)

    elif option == "32bits":
        stdin, stdout, stderr = sut.exec_command("python3 /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/ww18_sut_audio.py -b 32 -s 48")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)

main()
