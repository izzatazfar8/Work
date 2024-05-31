# jepson
# python3, replace GenericCommand and ssh_util using fabric
import os, re, sys, time, argparse, subprocess, time
#from fabric2 import Connection
#from fabric.api import run, env, settings, put, execute
# from fabric.operation import run, put
#from fabric.contrib.files import exists
#from invoke import UnexpectedExit
import paramiko
import argparse

destPath = "/home/test/siv_test_collateral/siv_val-io-test-apps/audio"
file_to_check = "/home/Audio_checker.py"
script_name = str(sys.argv[0])
usage = "# python /home/THM/automation_script/Audio_checker_THM.py <IP> <option>"
pvtkey='/home/adlp3/.ssh/id_rsa'
parser = argparse.ArgumentParser(prog=script_name, description=usage)
parser.add_argument('-sut_ip', help='SUT IP')
parser.add_argument('-sut_user', help='SUT User')
parser.add_argument('-sut_pass', help='SUT Password')
parser.add_argument('-os', help='OS')
parser.add_argument('-thm_ip', help='THM IP')
#parser.add_argument('-op', help='Option = [modules_checker, alsa_checker, 16bits, 32bits]')
parser.add_argument('-op', help='Option = [playback, driver_check]')
parser.add_argument('-drv', help='Driver = [HDA, SOF]')
parser.add_argument('-bitdepth', help='bitdepth = [8bits, 16bits, 24bits, 32bits]')
parser.add_argument('-khz', help='rate = [8, 16, 48]')
parser.add_argument('-ch', help='channel = [2, 4, 8]')
parser.add_argument('-codec', help='codec = [hda, sof, snd]')
parser.add_argument('-pvt', help='Pvt-key at your THM : ex: /home/adlp3/rsa_pvt')
args = parser.parse_args()

def scp_files(username, password, ip_address):
    command = f"cd /home/applications.audio.validation.sve-bm-audio/ ; sudo sshpass -p '{password}' scp -o StrictHostKeyChecking=no -rv siv_test_collateral/siv_val-io-test-apps/audio/siv_test_collateral_audio_SUT/ {username}@{ip_address}:/home/user"
    #command = f"cd /home/applications.audio.validation.sve-bm-audio/ ; sudo cp -r siv_test_collateral/ /home/ ; sudo sshpass -p '{password}' scp -o StrictHostKeyChecking=no -rv siv_test_collateral/siv_val-io-test-apps/audio/siv_test_collateral_audio_SUT/ {username}@{ip_address}:/home/user"
    return os.system(command)

if args.sut_user is not None and args.sut_pass is not None and args.sut_ip is not None:
        result = scp_files(args.sut_user, args.sut_pass, args.sut_ip)
        print(result)
else:
        print("Please provide both username (-sut_user), password (-sut_pass), and IP address (-sut_ip).")

#python3 /home/siv_test_collateral/siv_val-io-test-apps/audio/new_audio_thm_checker.py -sut_ip 172.30.248.25 -op playback -drv HDA -bitdepth 32 -khz 48 -ch 2
if args.os == "ubuntu":
    target_user = args.sut_user
    target_pass = args.sut_pass
    print ("Running on Ubuntu")
    #result = os.system("cd /home/applications.audio.validation.sve-bm-audio/ ; sshpass -p 'user1234' sudo scp -r siv_test_collateral/siv_val-io-test-apps/audio/siv_test_collateral_audio_SUT/ user@" + args.sut_ip + ":/home/user")
    result = os.system("cd /home/applications.audio.validation.sve-bm-audio/ ;  sshpass -p" + target_pass + "; sudo scp -r siv_test_collateral/siv_val-io-test-apps/audio/siv_test_collateral_audio_SUT/ user@" + target_user + ":/home/user")
    print(result)

    
else:
    target_user = args.sut_user
    target_pass = args.sut_pass
    print ("Running on Yocto")

if args.sut_ip is not None:
    sut_ip = args.sut_ip
else:
    print ("-sut_ip missing")
    sys.exit(1)

if args.os is not None:
    os = args.os
if args.op is not None:
     option = args.op
else:
     print ("-op missing")
     sys.exit(1)

if args.codec is not None:
     codec = args.codec

sut = paramiko.SSHClient()
sut.set_missing_host_key_policy(paramiko.AutoAddPolicy())

if args.pvt is not None:
    pvtkey = args.pvt
    print (pvtkey)
    sut.connect(hostname=sut_ip, username=target_user, key_filename=pvtkey)
    print("SSH key-authetication established successfully.")
else:
    sut.connect(hostname=sut_ip, port=22, username=target_user, password=target_pass, allow_agent=False, look_for_keys=False)
    print("SSH password authentication established successfully.")
host,port = sut_ip,22
# transport = paramiko.Transport((host,port))
# username,password = "root",""
# transport.connect(None,username,password)
# sftp = paramiko.SFTPClient.from_transport(transport)

if args.os == "ubuntu":
    stdin, stdout, stderr = sut.exec_command("cd /home/user/ ; sudo cp -r siv_test_collateral_audio_SUT /home/")
    #stdin, stdout, stderr = sut.exec_command("cd /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio ; sudo cp -r sof-mtl.ri /lib/firmware/intel/sof-ipc4/mtl/")
    #stdin, stdout, stderr = sut.exec_command("cd /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio ; sudo cp -r sof-mtl-rt711-2ch.tplg /lib/firmware/intel/sof-ace-tplg/")
    #stdin, stdout, stderr = sut.exec_command("cd /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio ; sudo cp -r Audio_checker_SUT_ubuntu.py Audio_checker_SUT.py")
    #stdin, stdout, stderr = sut.exec_command("sudo reboot")
    #time.sleep(30)
    print ("Running on Ubuntu")
else:
    stdin, stdout, stderr = sut.exec_command("sudo cp -r /home/hspe/siv_test_collateral_audio_SUT/ /home/")
    print ("Running on ubuntu")

if args.codec == "sof":
    stdin, stdout, stderr = sut.exec_command("sudo cp -r /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/sof-adl-s.ri /lib/firmware/intel/sof/ ")
    stdin, stdout, stderr = sut.exec_command("sudo cp -r /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/sof-hda-generic.tplg /lib/firmware/intel/sof-tplg/ ") 
    stdin, stdout, stderr = sut.exec_command("sudo cp -r /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/blacklist_hda.conf /etc/modprobe.d/ ")
    #stdin, stdout, stderr = sut.exec_command("sudo reboot ")
    #time.sleep(50)
    print ("SOF Audio is loaded")
if args.codec == "snd":
    stdin, stdout, stderr = sut.exec_command("sudo cp -r /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/sof-adl-s.ri /lib/firmware/intel/sof/ ")
    stdin, stdout, stderr = sut.exec_command("sudo cp -r /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/sof-hda-generic.tplg /lib/firmware/intel/sof-tplg/ ") 
    stdin, stdout, stderr = sut.exec_command("sudo cp -r /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/blacklist_hda.conf /etc/modprobe.d/ ")
    #stdin, stdout, stderr = sut.exec_command("sudo reboot ")
    #time.sleep(50)
    print ("Soundwire Audio is loaded")
else:
    stdin, stdout, stderr = sut.exec_command("sudo cp -r /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/blacklist_hda.conf /etc/modprobe.d/ ")
    #stdin, stdout, stderr = sut.exec_command("sudo reboot ")
    #time.sleep(50)
    print ("HDA is loaded")

def main():
	
	
    if option == "snd_script":
        stdin, stdout, stderr = sut.exec_command("sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c snd_script")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(80)
        output = stdout.readlines()
        sut.close()
        print ("DONE")
        sys.exit(0)

    if option == "modules_checker":
        stdin, stdout, stderr = sut.exec_command("sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c modules")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)

    elif option == "alsa_checker":
        stdin, stdout, stderr = sut.exec_command("sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c alsa")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
    elif option == "sof_checker":
        stdin, stdout, stderr = sut.exec_command("sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c sof")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
    elif option == "16bits":
        stdin, stdout, stderr = sut.exec_command("sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -b 16 -s 48")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)

    elif option == "32bits":
        stdin, stdout, stderr = sut.exec_command("sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -b 32 -s 48")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
		
    elif option == "32bits_8k":
        stdin, stdout, stderr = sut.exec_command("sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -b 32 -s 8")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
		
    elif option == "16bits_sof":
        stdin, stdout, stderr = sut.exec_command("sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c sof_16b")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)

    elif option == "snd_hda":
        stdin, stdout, stderr = sut.exec_command("sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c snd_hda")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)

    elif option == "hdaudioC0D0":
        stdin, stdout, stderr = sut.exec_command("sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c hdaudioC0D0")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)

    elif option == "mic_jack":
        stdin, stdout, stderr = sut.exec_command("sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c mic_jack")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)

    elif option == "playback_switch":
        stdin, stdout, stderr = sut.exec_command("sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c playback_switch")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)

    elif option == "capture_switch":
        stdin, stdout, stderr = sut.exec_command("sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c capture_switch")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)

    elif option == "aplay":
        stdin, stdout, stderr = sut.exec_command("sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c aplay")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)

    elif option == "arecord":
        stdin, stdout, stderr = sut.exec_command("sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c arecord")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
	
    elif option == "aplay_snd":
        stdin, stdout, stderr = sut.exec_command("sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c aplay_snd")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)

    elif option == "arecord_snd":
        stdin, stdout, stderr = sut.exec_command("sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c arecord_snd")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
    elif option == "snd":
        stdin, stdout, stderr = sut.exec_command("sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c snd")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)

    elif option == "lspci":
        stdin, stdout, stderr = sut.exec_command("sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c lspci")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)		
    elif option == "audio_lib":
        stdin, stdout, stderr = sut.exec_command("sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c audio_lib")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
    elif option == "playback":
        stdin, stdout, stderr = sut.exec_command("sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/new_audio_SUT_checker.py -op " + option + " -drv " +Driver + " -b " + bitdepth + " -s " + rate + " -ch " + channel)
        execcommand = ("python3 /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/new_audio_SUT_checker.py -op " + option + " -drv " +Driver + " -b " + bitdepth + " -s " + rate + " -ch " + channel)
        print (execcommand)
		
        #stdin, stdout, stderr = sut.exec_command("sudo python3 /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/new_audio_SUT_checker.py -op playback -drv HDA -b 32 -s 48 #-ch 2")
		
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
    elif option == "rt5660_codec":
        stdin, stdout, stderr = sut.exec_command("sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c rt5660_codec")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
    elif option == "rt5660_arecord":
        stdin, stdout, stderr = sut.exec_command("sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c rt5660_arecord")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
    elif option == "rt5660_modules":
        stdin, stdout, stderr = sut.exec_command("sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c rt5660_modules")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
    elif option == "usb_16bits":
        stdin, stdout, stderr = sut.exec_command("sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c 16bits_usb")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
    
    elif option == "usb_32bits":
        stdin, stdout, stderr = sut.exec_command("sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c 32bits_usb")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
    elif option == "dp_16bits":
        stdin, stdout, stderr = sut.exec_command("sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c 16bits_dp")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
    elif option == "dp_32bits":
        stdin, stdout, stderr = sut.exec_command("sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c 32bits_dp")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
    elif option == "play_16bits":
        stdin, stdout, stderr = sut.exec_command("sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c 16bits_play")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
    elif option == "record_16bits":
        stdin, stdout, stderr = sut.exec_command("sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c 16bits_record")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
    elif option == "play_32bits":
        stdin, stdout, stderr = sut.exec_command("sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c 32bits_play")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
    elif option == "record_32bits":
        stdin, stdout, stderr = sut.exec_command("sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c 32bits_record")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
    elif option == "play_16bits_sof":
        stdin, stdout, stderr = sut.exec_command("sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c 16bits_play_sof")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
    elif option == "record_16bits_sof":
        stdin, stdout, stderr = sut.exec_command("sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c 16bits_record_sof")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
    elif option == "play_32bits_sof":
        stdin, stdout, stderr = sut.exec_command("sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c 32bits_play_sof")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
    elif option == "record_32bits_sof":
        stdin, stdout, stderr = sut.exec_command("sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c 32bits_record_sof")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
        print ("AUDIO")
main()
