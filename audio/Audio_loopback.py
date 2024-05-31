
# Author: Athirah Basir
# Created: 25 OCT 2019
# Last updated: 15 DEC 2019

import logging
import traceback
import subprocess
import os
import sys
import re
import time
import argparse
import GenericCommand
import string
from datetime import date, datetime
import signal

# DEFAULT VARIABLES

threshold_ch0 = None
threshold_ch1 = None
sut_ip = "172.30.181.94" # SUT IP
sut_gcs_port = "2300"
thm_ip = "172.30.248.216" # THM IP
earhost_ip = "172.30.249.175" # AutoEar Windows machine IP
earhost_gcs_port = "2300"
threshold = 95
workingDir = "/home/siv_test_collateral/siv_val-io-test-apps/audio/"
logFile = "Audio_" + str(datetime.now().date()) + ".log"
debug = False
verdict = False
master = "master"
capture = "capture"
resultList = []
waveFileList = []

# Host machine configuration
host_os = "linux" # linux or windows
record_hw = "hw:0,0"
record_bit_depth = "32" # 16 or 32
record_fs = "48000"
record_ch = "2"
wait_to_kill = 30
duration = " -d " + str(wait_to_kill) + " " # seconds
sleepTime = wait_to_kill + 3
#gold_wav path
destination_file_dir = "C:\\audio_automation\Record_wav\kmb\\"
gold_sample = "C:\\audio_automation\Gold_wav_file\gold.wav"
gold_wav_base_location = "C:\\audio_automation\Gold_wav_file\gold\\"


# SUT configuration
HDMI_hw = "hw:0,3"
DP_hw = "hw:0,7"
HDA_hw = "hw:0,0"
SSP2_play_hw = "hw:0,0"
SSP2_record_hw = "hw:0,1"
SSP4_play_hw = "hw:0,2"
SSP4_record_hw = "hw:0,3"
SSP6_play_hw = "hw:0,0"
SSP6_record_hw = "hw:0,1"


# ***change port number***
generic_SSP1_play_hw = "hw:0,1"    #Port 1 - SSP0
generic_SSP1_rec_hw = "hw:0,1"


audioFileDir = "/home/siv_test_collateral/siv_val-io-test-apps/audio/Audio_wav_files/"
logDir = "/home/siv_test_collateral/siv_val-io-test-apps/audio/Audio_log/"
rec_file_directory = "/home/siv_test_collateral/siv_val-io-test-apps/audio/Record_wav_files/"
aplay_cmd = "aplay -vD " 
arecord_cmd = "arecord -vD "  

# FUNCTION DEFINITIONS

def get_current_time():
    #return time in <hour:minute:second> format"
    currentTime = datetime.time(datetime.now())
    time_Hour = currentTime.hour
    time_Minute = currentTime.minute
    time_Second = currentTime.second
    Time_now = str(time_Hour) + "_" + str(time_Minute) + "_" + str(time_Second)
    return Time_now

def get_current_date():
    #return date in YYYY-MM-DD format
    currentdate = datetime.date(datetime.now())
    date_year = currentdate.year
    date_month = currentdate.month
    date_day = currentdate.day
    date_now = str(date_year) + "-" + str(date_month) + "-" + str(date_day)
    return date_now

def write_log(filename='', line=''):
    target = open(str(filename), 'a')
    line = "[" + str(get_current_date()) + " " + str(get_current_time()) + "] \t" + str(line) + "\n"
    # Writes log in the format of: "[2015-12-02]    Comments" to the specified file
    target.write(line)
    target.close()

#flow 5
def result_parser(output,default_threshold):

    "Perform auto ear generated log result parsing"
    global dict
    global result_output
    dict = {}
    chl_list = []
    rate_list = []
    pass_list = []
    result_output = []
    date = ""
    result = True

    message = "***Extracting result from AUTOEAR server***"
    print message
    
    for line in output:
        print line
        if "Audio content size" in line:
            match_chl = re.search(r'channel \d',line)
            if match_chl:
                chl_list.append(match_chl.group(0))

        elif "Total Similarity" in line:
            match_rate = re.search(r'\d+.\d+',line)
            if match_rate:
                rate_list.append(match_rate.group(0))
    
    print "Retrieving data....."
    if not chl_list or not rate_list:
        print "***Failed to retrieve comparison result, the Audio Comparison App might has crashed***"
        #sys.exit(1)
    else:
        print chl_list
        print rate_list

    threshold_dict = {"0":threshold_ch0,"1":threshold_ch1}

    for rate in rate_list:
        if float(rate) >= default_threshold:
            pass_list.append("PASS")
        else:
            pass_list.append("FAIL")
    
    print pass_list    
    
    if "FAIL" in pass_list:
        result = "FAIL"
    elif "PASS" in pass_list:
        result = "PASS"
    
    return result

# ARGUMENT PARSER

script_name = str(sys.argv[0])
usage="Usage: This program requires test cases parameters to run \n\
       Required parameters for audio automation -> -f -b -s -m \n\
       Eg. python /home/siv_test_collateral/siv_val-io-test-apps/audio/Audio_loopback.py -f 8 -b 16 -s 1 -m TDM6 -i 172.30.181.90 -e 172.30.249.175 \n\
	   python /home/siv_test_collateral/siv_val-io-test-apps/audio/Audio_loopback.py -f 8 -b 16 -s 1 -m I2S -i 172.30.181.90 -e 172.30.249."

parser = argparse.ArgumentParser(prog = script_name,
                                 formatter_class=argparse.RawTextHelpFormatter,
                                 description = usage)
parser.add_argument('-i', metavar='--IP', help='SUT IP')
parser.add_argument('-thm', metavar='--thm_ip' ,help='THM IP')
parser.add_argument('-e', metavar='--earhost' ,help='AutoEar IP')
parser.add_argument('-t', metavar='--threshold', help='Threshold of audio comparison: number')
parser.add_argument('-d', metavar='--debug',help='Debug option: on, off')
parser.add_argument('-T', metavar='--testcase',help='testCaseID')
parser.add_argument('-f', metavar='--f',help='1. Audio file sampling rate')
parser.add_argument('-b', metavar='--bit',help='2. Audio file bit depth')
parser.add_argument('-s', metavar='--Port',help='3. Port')
parser.add_argument('-m', metavar='--SSP_M',help='4. SSP Mode')
parser.add_argument('-C', metavar='--SSP_CLK',help='5. SSP Clock')
parser.add_argument('-c', metavar='--CLK_D',help='6. Clock domain')
parser.add_argument('-F', metavar='--F',help='7. Image sampling rate')
parser.add_argument('-B', metavar='--B',help='8. Image bit depth')
parser.add_argument('-S', metavar='--slot',help='9. Slot width')
parser.add_argument('-D', metavar='--delay',help='10. Frame sync delay')
parser.add_argument('-p', metavar='--p',help='11. Data polarity')
parser.add_argument('-P', metavar='--P',help='12. Frame sync polarity')
parser.add_argument('-a', metavar='--boot',help='13. Bootable device')
parser.add_argument('-z', metavar='--testapp',help='14. Test application')
parser.add_argument('-g', metavar='--compositor',help='15. Graphics compositor = X11 / Wayland')

args = parser.parse_args()
   
if args.t is not None:
    threshold = int(args.t)
    
if args.d is not None:
    debug = True
    #verdict = True 

if args.i is not None:
 	sut_ip = args.i	
		
# if args.thm is not None:
	# thm_ip = args.thm
	
if args.e is not None:
 	earhost_ip = args.e	


ch_dict = {
"TDM1" : "1"
,"I2S" : "2"
,"TDM4" : "4"
,"TDM6" : "6"
,"TDM8" : "8"
}

channel_number = ch_dict[args.m]
audioFile = args.b + "b_" + args.f + "k_" + channel_number + "ch.wav"
    

## MAIN
def main():
    global threshold
    global gold_sample
    ## Initialize SUT, AutoEarHost, create objects
	#--------------------------------------------------------------------------------------------------
	#STARTING:
    if not debug:
        AutoEarHost = GenericCommand.GenericCommand()
        AutoEarHost.login(earhost_ip, earhost_gcs_port)
	#flow 1
    message = "DEBUG: Host Operating System is " + host_os
    print message
    write_log(logDir + logFile, message)

    # TRANSFER ORI AUDIO FILES FROM THM
    origin = "/home/siv_test_collateral/siv_val-io-test-apps/audio/"
    
    i = 0
    items = []
    
    if debug:
        #WIP4: debug option
        print "sut_ip: " + sut_ip
        print "gcs_port: " + gcs_port
        print "earhost_ip: " + earhost_ip
        print "earhost_gcs_port: " + earhost_gcs_port
        print "threshold: " + str(threshold)
        print "logFile: " + workingDir + logFile
        
        print "cmdRecord: " + cmdRecord
        print "cmdHTML5Record: " + cmdHTML5Record
        print "cmdHDARecord: " + cmdHDARecord
        
    if args.s == "HDMI":
        ALSA_hw = HDMI_hw
        cmdChangeHDMIPulse = "cp "+ origin +"/hdmi_pulse/default.pa /etc/pulse/default.pa"
        os.system(cmdChangeHDMIPulse)
    elif args.s == "DP":
        ALSA_hw = DP_hw
        cmdChangeDPPulse = "cp "+ origin +"/dp_pulse/default.pa /etc/pulse/default.pa"
        os.system(cmdChangeDPPulse)
    elif args.s == "AudioJack":
        ALSA_hw = HDA_hw
        cmdChangeHDAPulse = "cp "+ origin +"/hda_pulse/default.pa /etc/pulse/default.pa"
        os.system(cmdChangeHDAPulse)
    else:
        ALSA_hw = HDMI_hw
                   
    aplay_cmd = "aplay -vD "
    arecord_cmd = "arecord -vD " 
    LE_cmd = "_LE " 
 
    if args.z == "chromium":
        browser = "google-chrome"
    elif args.z == "epiphany":
        browser = "epiphany -p"
    else:
        browser = args.z   
        
    #all playback command
    cmdHDMI_DP_Playback = aplay_cmd + ALSA_hw + duration + audioFileDir + audioFile
    cmdHDMIandDP_Playback = aplay_cmd + HDMI_hw + " -d 600 " + audioFileDir + "32bits_sine_mix_1.wav" + " & " + aplay_cmd + DP_hw + " -d 600 " + audioFileDir + "32bits_sine_mix_2.wav" #audioFile, duration, need a different gold wave file too
    cmdHDA_Playback = aplay_cmd + HDA_hw + duration + audioFileDir + audioFile
    cmdSSP_dummy_Playback = aplay_cmd + SSP2_play_hw + duration + audioFileDir + audioFile
    cmdSSP_WM8731_Playback = aplay_cmd + SSP4_play_hw + duration + audioFileDir + audioFile
    cmdSSP_TI_Playback = aplay_cmd + SSP6_play_hw + duration + audioFileDir + audioFile
    
    if args.g == "X11":
        cmdHTML5Playback = "xinit /usr/bin/" + str(browser) + " file://" + audioFileDir + args.b + "bits.html &"
    elif args.g == "wayland":
        cmdHTML5Playback = "/usr/bin/" + str(browser) + " file://" + audioFileDir + args.b + "bits.html &"   

    if str(host_os).upper() == "WINDOWS":
        cmdRecord = "" #WIP
        cmdHTML5Record = "" #WIP
        cmdHDARecord = "" #WIP
	#--------------------------------------------------------------------------------------
	#flow 2
    else:
        rec_file = get_current_date() + "_" + get_current_time() + "_" + args.b + "_" + args.f + "_" + args.m + "_" + args.s + ".wav"
      
        waveFileList.append(rec_file)
        
        print "\nRecorded file name changed to: " + rec_file
        #----------------------------------------------------------------------------------------------------------------------------------
        #WIP3: need configuration for arecord
        global record_hw, record_bit_depth
        
        if args.s in ['HDMI', 'DP'] and args.z not in ['midori', 'epiphany', 'firefox', 'chromium']:
            print "using default recording settings"
        elif args.s == "HDMIandDP" and args.z not in ['midori', 'epiphany', 'firefox', 'chromium']:
            print "using default recording settings"
        elif args.s == "AudioJack" and args.z not in ['midori', 'epiphany', 'firefox', 'chromium']:
            record_bit_depth = args.b
        elif args.g == "X11" and args.z in ['midori', 'epiphany', 'firefox', 'chromium']:
            print "using default recording settings"
        elif args.g == "wayland" and args.z in ['midori', 'epiphany', 'firefox', 'chromium']:
            print "using default recording settings"
        elif args.s == "SSP2":
            record_hw = SSP2_record_hw
            record_bit_depth = args.b
        elif args.s == "SSP4":
            record_hw = SSP4_record_hw 
            record_bit_depth = args.b
        elif args.s in ['SSP6', 'ex_speaker']:
            record_hw = SSP6_record_hw 
            record_bit_depth = args.b
        
        if record_bit_depth == "24":
            record_bit_depth = "24_3" #win autoear can't detect S24_LE format
            LE_cmd = "LE" 
        
        cmdRecord = arecord_cmd + record_hw + " -fS" + str(record_bit_depth) + LE_cmd + " -c " + str(record_ch) + " -r " + record_fs + duration + " " + rec_file_directory + rec_file
        
    if not debug: 
        if args.s in ['HDMI', 'DP'] and args.z not in ['midori', 'epiphany', 'firefox', 'chromium']:
            alsa_settings('hda')
            cmd_play_and_record = cmdRecord + " & " + cmdHDMI_DP_Playback
            message = "DEBUG: " + script_name + ": " + args.s + " test triggered..."
            print "\n"
            print message
            write_log(workingDir + logFile, message)
            
            message = "DEBUG: Playback and recording on SUT started"
            print message
            print "[SUT COMMAND] " + cmd_play_and_record
            run = subprocess.Popen(cmd_play_and_record, stdout=subprocess.PIPE, shell = True, preexec_fn=os.setsid)
            write_log(workingDir + logFile, message)

        elif args.s in ['HDMI', 'DP'] and args.z in ['midori', 'epiphany', 'firefox', 'chromium'] and args.g == "X11":
            alsa_settings('hda')
            threshold = 0 #pass as long as playback through HDMI/DP can be completed without system error, HDMI/DP functionalities are checked manually
            cmd_play_and_record = cmdRecord + " & " + cmdHTML5Playback
            message = "DEBUG: " + script_name + ": " + args.z + "HTML5 X11 test triggered..."
            print message
            write_log(workingDir + logFile, message)

            message = "DEBUG: Playback and recording on SUT started"
            print message
            print "[SUT COMMAND] " + cmd_play_and_record
            run = subprocess.Popen(cmd_play_and_record, stdout=subprocess.PIPE, shell = True, preexec_fn=os.setsid)
            write_log(workingDir + logFile, message)
            os.system("killall " + str(args.z))

        elif args.s in ['HDMI', 'DP'] and args.z in ['midori', 'epiphany', 'firefox', 'chromium'] and args.g == "wayland":
            alsa_settings('hda')
            threshold = 0 #pass as long as playback through HDMI/DP can be completed without system error, HDMI/DP functionalities are checked manually
            cmd_play_and_record = cmdRecord + " & " + cmdHTML5Playback
            message = "DEBUG: " + script_name + ": " + args.z + "HTML5 wayland test triggered..."
            print message
            write_log(workingDir + logFile, message)

            message = "DEBUG: Playback and recording on SUT started"
            print message
            print "[SUT COMMAND] " + cmd_play_and_record

            os.environ['XDG_RUNTIME_DIR']='/tmp' #setup wayland environment
            os.system("unset DISPLAY")
            os.system("weston --tty=1 &")
            time.sleep(5)

            run = subprocess.Popen(cmd_play_and_record, stdout=subprocess.PIPE, shell = True, preexec_fn=os.setsid)
            write_log(workingDir + logFile, message)
            time.sleep(sleepTime)
            os.system("killall " + str(args.z))
            os.system("killall weston")
        
        elif args.s == "HDMIandDP" and args.z not in ['midori', 'epiphany', 'firefox', 'chromium']:
            alsa_settings('hda')
            cmd_play_and_record = cmdRecord + " & " + cmdHDMIandDP_Playback
            message = "DEBUG: " + script_name + ": 1 HDMI & 1 DP test triggered..."
            print "\n"
            print message
            write_log(workingDir + logFile, message)

            message = "DEBUG: Playback and recording on SUT started"
            print message
            print "[SUT COMMAND] " + cmd_play_and_record
            run = subprocess.Popen(cmd_play_and_record, stdout=subprocess.PIPE, shell = True, preexec_fn=os.setsid)
            write_log(workingDir + logFile, message)
        
        elif args.s == "AudioJack" and args.z not in ['midori', 'epiphany', 'firefox', 'chromium']:
            alsa_settings('hda')
            cmd_play_and_record = cmdRecord + " & " + cmdHDA_Playback
            message = "DEBUG: " + script_name + ": HDA test triggered..."
            print "\n"
            print message
            write_log(workingDir + logFile, message)
            
            message = "DEBUG: Playback and recording on SUT started"
            print message
            print "[SUT COMMAND] " + cmd_play_and_record
            run = subprocess.Popen(cmd_play_and_record, stdout=subprocess.PIPE, shell = True, preexec_fn=os.setsid)
            write_log(workingDir + logFile, message)
        
        elif args.g == "X11" and args.z in ['midori', 'epiphany', 'firefox', 'chromium']:
            alsa_settings('hda')
            cmd_play_and_record = cmdRecord + " & " + cmdHTML5Playback
            message = "DEBUG: " + script_name + ": " + args.z + "HTML5 X11 test triggered..."
            print message
            write_log(workingDir + logFile, message)
            
            message = "DEBUG: Playback and recording on SUT started"
            print message
            print "[SUT COMMAND] " + cmd_play_and_record
            run = subprocess.Popen(cmd_play_and_record, stdout=subprocess.PIPE, shell = True, preexec_fn=os.setsid)
            write_log(workingDir + logFile, message)
            #time.sleep(sleepTime)
            os.system("killall " + str(args.z))
        
        elif args.g == "wayland" and args.z in ['midori', 'epiphany', 'firefox', 'chromium']:
            alsa_settings('hda')
            cmd_play_and_record = cmdRecord + " & " + cmdHTML5Playback
            message = "DEBUG: " + script_name + ": " + args.z + "HTML5 wayland test triggered..."
            print message
            write_log(workingDir + logFile, message)
            
            message = "DEBUG: Playback and recording on SUT started"
            print message
            print "[SUT COMMAND] " + cmd_play_and_record
            
            os.environ['XDG_RUNTIME_DIR']='/tmp' #setup wayland environment
            os.system("unset DISPLAY")
            os.system("weston --tty=1 &")
            time.sleep(5)
                       
            run = subprocess.Popen(cmd_play_and_record, stdout=subprocess.PIPE, shell = True, preexec_fn=os.setsid)
            write_log(workingDir + logFile, message)
            time.sleep(sleepTime)
            os.system("killall " + str(args.z))
            os.system("killall weston")
			
		#flow - 3 ----------------------------------------------------------------------------------------------------------------------
        elif args.s in ["1", "2", "3", "4", "5", "6"] and args.m in ["TDM1", "I2S", "TDM4", "TDM6", "TDM8"]:
         
            generic_ssp_dict = {
            "1" : {"play_hw" : generic_SSP1_play_hw, "rec_hw" : generic_SSP1_rec_hw}
            # ,"2" : {"play_hw" : generic_SSP2_play_hw, "rec_hw" : generic_SSP2_rec_hw}
            # ,"3" : {"play_hw" : generic_SSP3_play_hw, "rec_hw" : generic_SSP3_rec_hw}
            # ,"4" : {"play_hw" : generic_SSP4_play_hw, "rec_hw" : generic_SSP4_rec_hw}
            # ,"5" : {"play_hw" : generic_SSP5_play_hw, "rec_hw" : generic_SSP5_rec_hw}
            # ,"6" : {"play_hw" : generic_SSP6_play_hw, "rec_hw" : generic_SSP6_rec_hw}
            }

            fs_dict = {
            "8" : 8000
            ,"11.025" : 11025
            ,"12" : 12000
            ,"16" : 16000
            ,"18.9" : 18900
            ,"22.05" : 22050
            ,"24" : 24000
            ,"32" : 32000
            ,"44.1" : 44100
            ,"48" : 48000
            ,"64" : 64000
            ,"88.2" : 88200
            ,"96" : 96000
            ,"176.4" : 176400
            ,"192" : 192000
            }

            gold_sample = gold_wav_base_location + args.b + "b_" + args.f + "k_" + channel_number + "ch.wav"
            generic_audioFile = audioFile

            cmdgenericRecord = arecord_cmd + generic_ssp_dict[args.s]["rec_hw"] + " -fS" + str(args.b) + LE_cmd + " -c " + str(channel_number) + " -r " + str(fs_dict[args.f]) + duration + " " + rec_file_directory + rec_file
            cmdSSP_generic_Playback = aplay_cmd + generic_ssp_dict[args.s]["play_hw"] + duration + audioFileDir + generic_audioFile
			#audio record first and do playback in background
            cmd_play_and_record = cmdgenericRecord + " & " + cmdSSP_generic_Playback
            message = "DEBUG: " + script_name + ": " + args.s + " port generic test triggered..."
            print "\n"
            print message
            write_log(logDir + logFile, message)

            message = "DEBUG: Playback and recording on SUT started"
            print message
            print "[SUT COMMAND] " + cmdgenericRecord
            print "[SUT COMMAND] " + cmdSSP_generic_Playback
            run = subprocess.Popen(cmdgenericRecord, stdout=subprocess.PIPE, shell = True, preexec_fn=os.setsid)
            time.sleep(5)
            run = subprocess.Popen(cmdSSP_generic_Playback, stdout=subprocess.PIPE, shell = True, preexec_fn=os.setsid)
            write_log(logDir + logFile, message)
            #-------------------------------------------------------------------------------------------------------------------------------------
        elif args.s in ["SSP1", "SSP2", "SSP3", "SSP4", "SSP5", "SSP6"] and args.m in ["TDM4", "TDM6", "TDM8"]:
            alsa_settings('dummy')

            gold_sample_dict = {
            "TDM4" : {"48" : "C:\\audio_automation\goldwavfile\gold_4ch_48k.wav", "96" : "C:\\audio_automation\goldwavfile\gold_4ch_96k.wav", "192" : "C:\\audio_automation\goldwavfile\gold_4ch_192k.wav"}
            ,"TDM6" : {"48" : "C:\\audio_automation\goldwavfile\gold_6ch_48k.wav", "96" : "C:\\audio_automation\goldwavfile\gold_6ch_96k.wav", "192" : "C:\\audio_automation\goldwavfile\gold_6ch_192k.wav"}
            ,"TDM8" : {"48" : "C:\\audio_automation\goldwavfile\gold_8ch_48k.wav", "96" : "C:\\audio_automation\goldwavfile\gold_8ch_96k.wav", "192" : "C:\\audio_automation\goldwavfile\gold_8ch_192k.wav"}
            }

            generic_audiofile_dict = {
            "TDM4" : {"48" : "4ch_48k_sine.wav", "96" : "4ch_96k_sine.wav", "192" : "4ch_192k_sine.wav"}
            ,"TDM6" : {"48" : "6ch_48k_sine.wav", "96" : "6ch_96k_sine.wav", "192" : "6ch_192k_sine.wav"}
            ,"TDM8" : {"48" : "8ch_48k_sine.wav", "96" : "8ch_96k_sine.wav", "192" : "8ch_192k_sine.wav"}
            }

            generic_ssp_dict = {
            "SSP1" : {"play_hw" : generic_SSP1_play_hw, "rec_hw" : generic_SSP1_rec_hw}
            ,"SSP2" : {"play_hw" : generic_SSP2_play_hw, "rec_hw" : generic_SSP2_rec_hw}
            ,"SSP3" : {"play_hw" : generic_SSP3_play_hw, "rec_hw" : generic_SSP3_rec_hw}
            ,"SSP4" : {"play_hw" : generic_SSP4_play_hw, "rec_hw" : generic_SSP4_rec_hw}
            ,"SSP5" : {"play_hw" : generic_SSP5_play_hw, "rec_hw" : generic_SSP5_rec_hw}
            ,"SSP6" : {"play_hw" : generic_SSP6_play_hw, "rec_hw" : generic_SSP6_rec_hw}
            }

            #ch_dict = {
            #"I2S" : 2
            #,"TDM4" : 4
            #,"TDM6" : 6
            #,"TDM8" : 8
            #}

            fs_dict = {
            "48" : 48000
            ,"96" : 96000
            ,"192" : 192000
            }

            gold_sample = gold_sample_dict[args.m][args.f]
            generic_audioFile = generic_audiofile_dict[args.m][args.f]

            cmdgenericRecord = arecord_cmd + generic_ssp_dict[args.s]["rec_hw"] + " -fS" + str(args.b) + LE_cmd + " -c " + str(ch_dict[args.m]) + " -r " + str(fs_dict[args.f]) + duration + " " + rec_file_directory + rec_file
            cmdSSP_generic_Playback = aplay_cmd + generic_ssp_dict[args.s]["play_hw"] + duration + audioFileDir + generic_audioFile

            cmd_play_and_record = cmdgenericRecord + " & " + cmdSSP_generic_Playback
            message = "DEBUG: " + script_name + ": " + args.s + " generic test triggered..."
            print "\n"
            print message
            write_log(workingDir + logFile, message)

            message = "DEBUG: Playback and recording on SUT started"
            print message
            print "[SUT COMMAND] " + cmd_play_and_record
            run = subprocess.Popen(cmd_play_and_record, stdout=subprocess.PIPE, shell = True, preexec_fn=os.setsid)
            write_log(workingDir + logFile, message)
        
        elif args.s == "SSP2":
            alsa_settings('dummy')
            cmd_play_and_record = cmdRecord + " & " + cmdSSP_dummy_Playback
            message = "DEBUG: " + script_name + ": " + args.s + " dummy test triggered..."
            print "\n"
            print message
            write_log(workingDir + logFile, message)

            message = "DEBUG: Playback and recording on SUT started"
            print message
            print "[SUT COMMAND] " + cmd_play_and_record
            run = subprocess.Popen(cmd_play_and_record, stdout=subprocess.PIPE, shell = True, preexec_fn=os.setsid)
            write_log(workingDir + logFile, message)
            
        elif args.s == "SSP4":
            alsa_settings('wm')
            gold_sample = "C:\\audio_automation\goldwavfile\gold_wm.wav"
            cmd_play_and_record = cmdRecord + " & " + cmdSSP_WM8731_Playback
            message = "DEBUG: " + script_name + ": " + args.s + " WM8731 test triggered..."
            print "\n"
            print message
            write_log(workingDir + logFile, message)

            message = "DEBUG: Playback and recording on SUT started"
            print message
            print "[SUT COMMAND] " + cmd_play_and_record
            run = subprocess.Popen(cmd_play_and_record, stdout=subprocess.PIPE, shell = True, preexec_fn=os.setsid)
            write_log(workingDir + logFile, message)
        
        elif args.s in ['SSP6', 'ex_speaker'] and args.C == "Master":
            alsa_settings('ti_master')
            cmd_play_and_record = cmdRecord + " & " + cmdSSP_TI_Playback
            message = "DEBUG: " + script_name + ": " + args.s + " TI codec master test triggered..."
            print "\n"
            print message
            write_log(workingDir + logFile, message)

            message = "DEBUG: Playback and recording on SUT started"
            print message
            print "[SUT COMMAND] " + cmd_play_and_record
            run = subprocess.Popen(cmd_play_and_record, stdout=subprocess.PIPE, shell = True, preexec_fn=os.setsid)
            write_log(workingDir + logFile, message)
        
        elif args.s in ['SSP6', 'ex_speaker'] and args.C == "Slave":
            alsa_settings('ti_slave')
            cmd_play_and_record = cmdRecord + " & " + cmdSSP_TI_Playback
            message = "DEBUG: " + script_name + ": " + args.s + " TI codec slave test triggered..."
            print "\n"
            print message
            write_log(workingDir + logFile, message)

            message = "DEBUG: Playback and recording on SUT started"
            print message
            print "[SUT COMMAND] " + cmd_play_and_record
            run = subprocess.Popen(cmd_play_and_record, stdout=subprocess.PIPE, shell = True, preexec_fn=os.setsid)
            write_log(workingDir + logFile, message)
           
        #WIP5: error handling
        #1 when cant get result from autoear
        else:
            message = "ERROR: Insufficient parameters. Try HDMI, DP, HTML5, HDA or SSP"
            print message
            write_log(workingDir + logFile, message)
            verdict = False

        time.sleep(wait_to_kill + 5)
        os.killpg(os.getpgid(run.pid), signal.SIGTERM)
        #os.system("killall arecord")
        

        ## On end of playback, stop recording sample
        if str(host_os).upper() == "WINDOWS":
            command = "" #WIP
		
		#flow 4 ---------------------------------------------------------------------------------------------------------------
        else:
            command = "pkill arecord"
                
            # NOTE: ADD FUNCTION TO CHECK RECORDING IS TRULY DEAD
            message = "\n[STOP RECORDING]" + script_name + ": Host Recording stopped."
            print message
            write_log(logDir + logFile, message)
            
            verdict = True
            
            ## Send file from host (recording machine) to AutoEar machine
            message = "DEBUG: Sending audio file to AutoEar..."
            print message
            print "\n"
            write_log(logDir + logFile, message)
            AutoEarHost.timefiletransfer(rec_file_directory + rec_file, destination_file_dir + rec_file)
            
            # Check if file has been transferred
            if verdict and AutoEarHost.timefiletrace(destination_file_dir + rec_file):
                print "\n"
                message = "DEBUG: " + rec_file_directory + rec_file + " has been sent to " + earhost_ip
                print message
                print "\n "
                write_log(logDir + logFile, message)
                verdict = True
                
            else:
                message = "ERROR: Fail to send "+ rec_file_directory + rec_file +" to " + earhost_ip
                print message
                write_log(logDir + logFile, message)
                verdict = False

            ## Trigger AutoEar to Compare result
            if verdict:
                try:
                    msg = "Auto ear is running ..."
                    print msg
                    AutoEarHost.execute("mkdir C:\\audio_automation\AudioCompare_Log")
                    auto_ear_cmd = "C:\\WinAutoEar\AudioCompare.exe compare " + str(threshold) + " " + gold_sample + " " + destination_file_dir + rec_file + " C:\\audio_automation\AudioCompare_Log\compare.log"
                    #print auto_ear_cmd
                    #AutoEarHost.timeexecute(auto_ear_cmd)
                    AutoEarHost.execute(auto_ear_cmd)
                
                    # Below is checks if AutoEar terminates automatically. Adapted from HDA script
                    counter = 0
                    timeout = 10
                    while counter <= timeout:
                        if counter >= timeout - 1:
                            task = "AudioCompare.exe"
                            checker = AutoEarHost.execute("tasklist")
                            print "DEBUG: " + checker
                            #write_log(workingDir + logFile, message)
                            if "AudioCompare.exe" in checker:
                                AutoEarHost.execute("taskkill /F /im " + task)
                                message = "DEBUG: AudioCompare terminated."
                                print message
                                write_log(logDir + logFile, message)
                                break
                            else:
                                pass
                        time.sleep(1)
                        counter = counter + 1
                        
                    verdict = True

                except Exception, error:
                    type_, value_, traceback_ = sys.exc_info()
                    message = str(error)
                    print message
                    write_log(logDir + logFile, message)
                    message = traceback.format_tb(traceback_)
                    print message
                    write_log(logDir + logFile, message)
                    message = "ERROR: AutoEar failed to execute!"
                    verdict = False
					
			#flow 6
            ## Parse AutoEar result & final verdict
            if verdict:
                output = AutoEarHost.execute("type C:\\audio_automation\AudioCompare_Log\compare.log")
                output_list = output.split("\n")
                #for line in output_list:
                    #print line
                result = result_parser(output_list,threshold) # call function flow 5
                print "Final Result = " + str(result)
                
                for i in output_list:
                    if "compared" in i:
                        length = i.split(" ")[-1]
                        length = length[:-1]
                message = "DEBUG: Comparable length: " + str(length) + " sec"
                print message
                write_log(logDir + logFile, message)
                
                length = str(length)
                if len(length) > 1:
                    length = float(length)
                else:
                    length = int(length)
                
                print "results = " + str(result)
                print "length = " + str(length)
                print "logFile: " + logDir + logFile
                
                AutoEarHost.execute("DEL C:\\audio_automation\Record_wav\kmb\*.wav*.fft")
                AutoEarHost.execute("DEL C:\\audio_automation\Gold_wav_file\gold\*.wav*.fft")
                cmd = "RENAME C:\\audio_automation\AudioCompare_Log\compare.log compare_" + "%date:~10,4%%date:~7,2%%date:~4,2%_%time:~0,2%%time:~3,2%" + "_volume_" + master + "_capture_" + capture + "_" + result + ".log"

                AutoEarHost.execute(cmd)
            
            else:
                message = "ERROR: AutoEar Result parsing error"
                print message
                write_log(logDir + logFile, message)
                verdict = False
        
        if verdict:
			message = "DEBUG: " + script_name + " has completed successfully.\n"
			print message
			write_log(logDir + logFile, message)
			print "....Audio execution completed"
			
        else:
			message = "ERROR: " + script_name + " has encountered an error during execution.\n"
			print message
			write_log(logDir + logFile, message)
			print ".....execution not completed"
        
    else:
        verdict = True
        
        message = "\nDEBUG: " + script_name + " has completed trial run.\n"               
    
if __name__ == "__main__":
    main()
    
## EOF
