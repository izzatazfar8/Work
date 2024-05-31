
# Author: Kahu

import logging
import traceback
import subprocess
import os
import subprocess
import sys
import re
import time
import argparse
import GenericCommand
import string
from datetime import date, datetime
import signal

#sample command : python audio_slave.py -s 172.30.249.127 -a 10.221.120.132 -lh 10.221.120.139 -t 4ch_16k_16m
#sample command : python audio_slave.py -s 172.30.249.127 -a 10.221.120.132 -lh 10.221.120.139 -t 8ch_16k_16m

script_name = str(sys.argv[0])
sut_ip = "172.30.249.127"
lh_ip = "10.221.120.139"
lh_gcs_port = "2300"
gcs_port = "2300" # GenericCommandServer default port is 2300
earhost_ip = "10.221.120.132" # AutoEar Windows machine IP
earhost_gcs_port = "2300"
threshold_ch0 = None
threshold_ch1 = None
threshold = 95
workingDir = "/home/siv_test_collateral/siv_val-io-test-apps/audio/"
audioFileDir = "/home/siv_test_collateral/siv_val-io-test-apps/audio/Audio_wav_files/"
logDir = "/home/siv_test_collateral/siv_val-io-test-apps/audio/Audio_log/"
rec_file_directory = "/home/siv_test_collateral/siv_val-io-test-apps/audio/Record_wav_files/"
logFile = "Audio_" + str(datetime.now().date()) + ".log"
debug = False
verdict = False
master = "master"
capture = "capture"
resultList = []
waveFileList = []
log = "Null"

usage="This program will execute gstreamer audio tests.\n"

parser = argparse.ArgumentParser(prog = script_name, description = usage)
parser.add_argument('-s', help='SUT IP')
parser.add_argument('-t', help='testid')
parser.add_argument('-a', help='AUTOEAR IP')
parser.add_argument('-lh', help='LEAFHILL IP')

args = parser.parse_args()

if args.s is not None:
    sut_ip = args.s
if args.a is not None:
    earhost_ip = args.a
if args.t is not None:
    testid= args.t
if args.lh is not None:
    lh_ip = args.lh

#gold_wav path
destination_file_dir = "C:\\audio_automation\Record_wav\kmb\\"
gold_sample = "C:\\audio_automation\Gold_wav_file\gold.wav"
gold_wav_base_location = "C:\\audio_automation\Gold_wav_file\gold\\"
    
def file_transfered(rec_file):
    print "Transferring: "+ rec_file_directory + rec_file
    AutoEarHost.timefiletransfer(rec_file_directory + rec_file, destination_file_dir + rec_file)
    if verdict and AutoEarHost.timefiletrace(destination_file_dir + rec_file):
        print "\n"
        message = "DEBUG: " + rec_file_directory + rec_file + " has been sent to " + earhost_ip
        
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
        
def Autoear_result_check(verdict,gold_sample,rec_file):
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
                
            message = "\nDEBUG: " + script_name + " has completed trial run.\n" 

def Start_GenericCommandServer():
    command = os.popen('ps ax').read()
    read_list = re.compile("\n").split(command)
    generic = True
    for line in read_list:
        if re.search("GenericCommandServer",line):          
            print "GenericCommandServer is Already Running"
            generic = False
            break
    if generic:
        subprocess.Popen(["python",workingDir+"GenericCommandServer.py"])
        subprocess.call(["echo","genericcommandserver is started"])
    else:
        print "done"

def PingAlive_check(_timeout,system_ip):
    print "Checking Pingalive..."
    time.sleep(10)
    system_alive = dut.pingalive(system_ip,timeout=_timeout)
    if system_alive:
        print "[SUT1]Reboot process completed"
    else:
        print "System is not alive, rebooting process failed"
    time.sleep(5)
 
Start_GenericCommandServer();  
dut = GenericCommand.GenericCommand()
dut.login(sut_ip,gcs_port)
lh = GenericCommand.GenericCommand()
lh.login(lh_ip,lh_gcs_port)
AutoEarHost = GenericCommand.GenericCommand()
AutoEarHost.login(earhost_ip, earhost_gcs_port)

Audio_Slave_path = "/home/root/Audio_slave/"
firmware_file = "/lib/firmware/5a98-INTEL-EDK2-2-tplg.bin"

def main():
    dut.execute("echo 'here execute alsamixer commands'")
    if testid == "4ch_16k_16m":
        rec_file = "4ch_16k_16m_slave_"+get_current_date()+get_current_time()+".wav"
        lh.execute("cp "+Audio_Slave_path+str(testid)+"/dfw_sst.bin "+firmware_file)
        lh.timeexecute("reboot")
        PingAlive_check(120,lh_ip)
        lh.execute("sh "+Audio_Slave_path+str(testid)+"/ssp3.sh")
        dut.timeexecute("arecord -Dhw:0,0 -r16000 -c4 -fS16_LE -d15 "+rec_file_directory+rec_file)
        lh.execute("aplay -Dhw:0,13 -r16000 -c4 -d20 -fS16_LE "+Audio_Slave_path+str(testid)+"/4ch_16k_16bit.wav")
        gold_sample = gold_wav_base_location + "4ch_16k_16m_slave.wav"
    elif testid == "8ch_16k_16m":
        rec_file = "8ch_16k_16m_slave_"+get_current_date()+get_current_time()+".wav"
        lh.execute("cp "+Audio_Slave_path+str(testid)+"/dfw_sst.bin "+firmware_file)
        lh.timeexecute("reboot")
        PingAlive_check(120,lh_ip)
        lh.execute("sh "+Audio_Slave_path+str(testid)+"/ssp3.sh")
        dut.timeexecute("arecord -Dhw:0,0 -r16000 -c8 -fS16_LE -d15 "+rec_file_directory+rec_file)
        lh.execute("aplay -Dhw:0,13 -r16000 -c8 -d20 -fS16_LE "+Audio_Slave_path+str(testid)+"/16k_16bit_8ch.wav")
        gold_sample = gold_wav_base_location + "8ch_16k_16m_slave.wav"
    else:
        dut.execute("echo 'no test case' ")
        sys.exit(1)
    print "Test done...."
    file_transfered(rec_file)
    Autoear_result_check(True,gold_sample,rec_file)

if __name__ == "__main__":
    main()
    
## EOF
