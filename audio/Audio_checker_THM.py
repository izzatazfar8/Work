# jepson
# python3, replace GenericCommand and ssh_util using fabric
import os, re, sys, time, argparse, subprocess, time
#from fabric2 import Connection
#from fabric.api import run, env, settings, put, execute
# from fabric.operation import run, put
#from fabric.contrib.files import exists
#from invoke import UnexpectedExit
import paramiko

destPath = "/home/test/siv_test_collateral/siv_val-io-test-apps/audio"
file_to_check = "/home/Audio_checker.py"
script_name = str(sys.argv[0])
usage = "# python /home/THM/automation_script/Audio_checker_THM.py <IP> <option>"
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
args = parser.parse_args()


#python3 /home/siv_test_collateral/siv_val-io-test-apps/audio/new_audio_thm_checker.py -sut_ip 172.30.248.25 -op playback -drv HDA -bitdepth 32 -khz 48 -ch 2

#s
if args.os == "ubuntu":
    target_user = args.sut_user
    target_pass = args.sut_pass
    print ("Running on Ubuntu")
    os.system ("sudo cp -r siv_test_collateral_audio_SUT/ /home")
    
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
"""
if args.drv is not None:
     Driver = args.drv
else:
     print ("-drv missing")
     sys.exit(1) 
	 
if args.bitdepth is not None:
     bitdepth = args.bitdepth
else:
     print ("-bitdepth missing")
     sys.exit(1) 
	 
if args.khz is not None:
     rate = args.khz
else:
     print ("-khz missing")
     sys.exit(1) 
	 
if args.ch is not None:
     channel = args.ch
else:
     print ("-ch missing")
     sys.exit(1) 
	 
"""

sut = paramiko.SSHClient()
sut.set_missing_host_key_policy(paramiko.AutoAddPolicy())
sut.connect(hostname=sut_ip,port=22,username=target_user,password=target_pass,allow_agent=False,look_for_keys=False)
# proc = subprocess.Popen(["prog", "arg"], stdout=subprocess.PIPE)
host,port = sut_ip,22
# transport = paramiko.Transport((host,port))
# username,password = "root",""
# transport.connect(None,username,password)
# sftp = paramiko.SFTPClient.from_transport(transport)

if args.os == "ubuntu":
    stdin, stdout, stderr = sut.exec_command("cd /home/user/ ; sudo cp -r siv_test_collateral_audio_SUT /home/")
    stdin, stdout, stderr = sut.exec_command("cd /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio ; sudo cp -r Audio_checker_SUT_ubuntu.py Audio_checker_SUT.py")
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

    if option == "modules_checker":
        stdin, stdout, stderr = sut.exec_command("sudo python3 /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT.py -c modules")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)

    elif option == "alsa_checker":
        stdin, stdout, stderr = sut.exec_command("sudo python3 /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT.py -c alsa")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
    elif option == "sof_checker":
        stdin, stdout, stderr = sut.exec_command("python3 /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT.py -c sof")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
    elif option == "16bits":
        stdin, stdout, stderr = sut.exec_command("sudo python3 /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT.py -b 16 -s 48")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)

    elif option == "32bits":
        stdin, stdout, stderr = sut.exec_command("sudo python3 /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT.py -b 32 -s 48")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
		
    elif option == "32bits_8k":
        stdin, stdout, stderr = sut.exec_command("python3 /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT.py -b 32 -s 8")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
		
    elif option == "16bits_sof":
        stdin, stdout, stderr = sut.exec_command("python3 /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT.py -c sof_16b")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)

    elif option == "snd_hda":
        stdin, stdout, stderr = sut.exec_command("python3 /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT.py -c snd_hda")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)

    elif option == "hdaudioC0D0":
        stdin, stdout, stderr = sut.exec_command("python3 /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT.py -c hdaudioC0D0")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)

    elif option == "mic_jack":
        stdin, stdout, stderr = sut.exec_command("python3 /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT.py -c mic_jack")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)

    elif option == "playback_switch":
        stdin, stdout, stderr = sut.exec_command("python3 /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT.py -c playback_switch")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)

    elif option == "capture_switch":
        stdin, stdout, stderr = sut.exec_command("python3 /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT.py -c capture_switch")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)

    elif option == "aplay":
        stdin, stdout, stderr = sut.exec_command("python3 /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT.py -c aplay")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)

    elif option == "arecord":
        stdin, stdout, stderr = sut.exec_command("python3 /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT.py -c arecord")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
	
    elif option == "aplay_snd":
        stdin, stdout, stderr = sut.exec_command("python3 /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT.py -c aplay_snd")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)

    elif option == "arecord_snd":
        stdin, stdout, stderr = sut.exec_command("python3 /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT.py -c arecord_snd")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
    elif option == "snd":
        stdin, stdout, stderr = sut.exec_command("python3 /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT.py -c snd")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)

    elif option == "lspci":
        stdin, stdout, stderr = sut.exec_command("python3 /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT.py -c lspci")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)		
    elif option == "audio_lib":
        stdin, stdout, stderr = sut.exec_command("python3 /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT.py -c audio_lib")
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
    elif option == "rt5660_codec":
        stdin, stdout, stderr = sut.exec_command("python3 /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT.py -c rt5660_codec")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
    elif option == "rt5660_arecord":
        stdin, stdout, stderr = sut.exec_command("python3 /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT.py -c rt5660_arecord")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
    elif option == "rt5660_modules":
        stdin, stdout, stderr = sut.exec_command("python3 /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT.py -c rt5660_modules")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
    elif option == "usb_16bits":
        stdin, stdout, stderr = sut.exec_command("python3 /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT.py -c 16bits_usb")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
    
    elif option == "usb_32bits":
        stdin, stdout, stderr = sut.exec_command("python3 /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT.py -c 32bits_usb")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
    elif option == "dp_16bits":
        stdin, stdout, stderr = sut.exec_command("python3 /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT.py -c 16bits_dp")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
    elif option == "dp_32bits":
        stdin, stdout, stderr = sut.exec_command("python3 /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT.py -c 32bits_dp")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
    elif option == "play_16bits":
        stdin, stdout, stderr = sut.exec_command("python3 /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT.py -c 16bits_play")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
    elif option == "record_16bits":
        stdin, stdout, stderr = sut.exec_command("python3 /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT.py -c 16bits_record")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
    elif option == "play_32bits":
        stdin, stdout, stderr = sut.exec_command("python3 /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT.py -c 32bits_play")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
    elif option == "record_32bits":
        stdin, stdout, stderr = sut.exec_command("python3 /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT.py -c 32bits_record")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
    elif option == "play_16bits_sof":
        stdin, stdout, stderr = sut.exec_command("python3 /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT.py -c 16bits_play_sof")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
    elif option == "record_16bits_sof":
        stdin, stdout, stderr = sut.exec_command("python3 /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT.py -c 16bits_record_sof")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
    elif option == "play_32bits_sof":
        stdin, stdout, stderr = sut.exec_command("python3 /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT.py -c 32bits_play_sof")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
    elif option == "record_32bits_sof":
        stdin, stdout, stderr = sut.exec_command("python3 /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT.py -c 32bits_record_sof")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
main()
