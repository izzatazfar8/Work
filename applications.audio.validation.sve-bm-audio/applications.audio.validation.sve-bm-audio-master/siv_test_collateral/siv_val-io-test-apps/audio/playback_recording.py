# Author: Kahu
# Edit: Kahu. Added encode feature
# Last Edit: Izzat (Able to run from THM),migrated to Python3

import logging
import traceback
import subprocess
import os
import subprocess
import sys
import re
import time
import argparse
import string
from datetime import date, datetime
import signal


script_name = str(sys.argv[0])
dev_1_ip = "10.221.123.93"
gcs_port = "2300" # GenericCommandServer default port is 2300
earhost_ip = "10.221.120.132" # AutoEar Windows machine IP
earhost_gcs_port = "2300"
threshold_ch0 = None
threshold_ch1 = None
threshold = 85
workingDir = "/home/siv_test_collateral/siv_val-io-test-apps/audio/"
audioFileDir = "/home/siv_test_collateral/siv_val-io-test-apps/audio/Audio_wav_files/"
logDir = "/home/siv_test_collateral/siv_val-io-test-apps/audio/Audio_log/"
rec_file_directory = "/home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/"
encode_rec_Dir = "/home/siv_test_collateral/siv_val-io-test-apps/audio/Record_wav_files/Encode_wav_files/"
encode_devtofile_Dir = "/home/siv_test_collateral/siv_val-io-test-apps/audio/Record_wav_files/Encode_devtofile/"
dev_to_file_enc = "aplay -v -Dhw:0,1 -d15 "+audioFileDir+ "16b_16k_2ch.wav | gst-launch-1.0 -e alsasrc device=hw:0,1 ! "
gst_kill = " & sleep 14;kill -2 $(pgrep gst-launch-1.0)"
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
parser.add_argument('-un','--username',help='Target machine username',default='root')
parser.add_argument('-ps','--password',help='Target machine password',default='')
parser.add_argument('-au','--autoearname',help='AutoEar machine username',default='AutoEar_EHL')
parser.add_argument('-ap','--autoearpass',help='AutoEar machine password',default='00ehl00')

args = parser.parse_args()

if args.s is not None:
    dev_1_ip = args.s
if args.a is not None:
    earhost_ip = args.a
if args.t is not None:
    testid= args.t
    
target_user = args.username
target_pass = args.password

autoear_user = args.autoearname
autoear_pass = args.autoearpass

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
    
def file_transfered(rec_file):

    #time.sleep(40)
    print("Transferring to AutoEar Machine: "+ rec_file_directory + rec_file)
    #AutoEarHost.timefiletransfer(rec_file_directory + rec_file, destination_file_dir + rec_file)
    #os.system("sshpass -p '00ehl00' scp -r " + rec_file_directory + rec_file + " AutoEar_EHL@10.221.120.139:/" + destination_file_dir + rec_file)
    #print("sshpass -p '00ehl00' scp -r " + rec_file_directory + rec_file + " AutoEar_EHL@10.221.120.139:/" + destination_file_dir + rec_file)
    sftp = AutoEarHost.open_sftp()
    sftp.put(rec_file_directory + rec_file , destination_file_dir + rec_file)
    #if verdict and AutoEarHost.timefiletrace(destination_file_dir + rec_file):
    print("\n")
    message = "DEBUG: " + rec_file_directory + rec_file + " has been sent to " + earhost_ip
    print (message)
    #sys.exit(1)
        
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
    print(message)
    
    for line in output:
        print(line)
        if "Audio content size" in line:
            match_chl = re.search(r'channel \d',line)
            if match_chl:
                chl_list.append(match_chl.group(0))

        elif "Total Similarity" in line:
            match_rate = re.search(r'\d+.\d+',line)
            if match_rate:
                rate_list.append(match_rate.group(0))
    
    print("Retrieving data.....")
    if not chl_list or not rate_list:
        result = False
        print("***Failed to retrieve comparison result, the Audio Comparison App might has crashed***")
        #sys.exit(1)
    else:
        print(chl_list)
        print(rate_list)

    threshold_dict = {"0":threshold_ch0,"1":threshold_ch1}

    for rate in rate_list:
        if float(rate) >= default_threshold:
            pass_list.append("PASS")
        else:
            pass_list.append("FAIL")
    
    print(pass_list)    
    
    if "FAIL" in pass_list:
        result = "FAIL"
    elif "PASS" in pass_list:
        result = "PASS"
    
    return result
        
def Autoear_result_check(verdict,gold_sample,rec_file):
            if verdict:
                try:
                    msg = "Auto ear is running ..."
                    print(msg)
                    auto_ear_cmd1 = "mkdir C:\\audio_automation\AudioCompare_Log"
                    stdin, stdout, stderr = AutoEarHost.exec_command(auto_ear_cmd1)
                    #auto_ear_cmd = "C:/WinAutoEar/AudioCompare.exe compare " + str(threshold) + " " + gold_sample + " " + destination_file_dir + rec_file + " C:/audio_automation/AudioCompare_Log/compare.log"
                    #print auto_ear_cmd
                    #AutoEarHost.timeexecute(auto_ear_cmd)
                    stdin, stdout, stderr = AutoEarHost.exec_command("C:\\WinAutoEar\AudioCompare.exe compare " + str(threshold) + " " + gold_sample + " " + destination_file_dir + rec_file + " C:\\audio_automation\AudioCompare_Log\compare.log")
                    
                    # Below is checks if AutoEar terminates automatically. Adapted from HDA script
                    counter = 0
                    timeout = 10
                    while counter <= timeout:
                        if counter >= timeout - 1:
                            task = "AudioCompare.exe"
                            stdin, stdout, stderr = AutoEarHost.exec_command("tasklist")
                            checker = stdout.read().decode("utf-8")
                            #print("DEBUG: " + checker)
                            #write_log(workingDir + logFile, message)
                            if "AudioCompare.exe" in checker:
                                AutoEarHost.exec_command("taskkill /F /im " + task)
                                message = "DEBUG: AudioCompare terminated."
                                print(message)
                                write_log(logDir + logFile, message)
                                break
                            else:
                                pass
                        time.sleep(1)
                        counter = counter + 1
                        
                    verdict = True
                    print ("DONE")
                    #sys.exit(1)

                except Exception as error:
                    type_, value_, traceback_ = sys.exc_info()
                    message = str(error)
                    print(message)
                    write_log(logDir + logFile, message)
                    message = traceback.format_tb(traceback_)
                    print(message)
                    write_log(logDir + logFile, message)
                    message = "ERROR: AutoEar failed to execute!"
                    verdict = False
                    
            #flow 6
            ## Parse AutoEar result & final verdict
            if verdict:
                #output1 = AutoEarHost.exec_command("scp -r C:\\audio_automation\AudioCompare_Log\compare.log root@10.221.120.148:/home/root")
				#sftp = AutoEarHost.open_sftp()
                #sftp.put(rec_file_directory + rec_file , destination_file_dir + rec_file)
                #output = AutoEarHost.exec_command("type C:\\audio_automation\AudioCompare_Log\compare.log")
                stdin, stdout, stderr = AutoEarHost.exec_command("type C:\\audio_automation\AudioCompare_Log\compare.log")
                #print (output2)
                #for line in stdout.readlines():
                 #print (line)
                otp = stdout.read().decode("utf-8")
                output_list = otp.split("\n")

                #print (output_list)
                                
                result = result_parser(output_list,threshold) # call function flow 5
                print("Final Result = " + str(result))
                
                for i in output_list:
                    if "compared" in i:
                        length = i.split(" ")[-1]
                        length = length[:-1]
                message = "DEBUG: Comparable length: " + str(length) + " sec"
                print(message)
                write_log(logDir + logFile, message)
                
                length = str(length)
                if len(length) > 1:
                    length = str(length)
                else:
                    length = int(length)
                
                print("results = " + str(result))
                print("length = " + str(length))
                print("logFile: " + logDir + logFile)
                
                stdin, stdout, stderr = AutoEarHost.exec_command("DEL C:\\audio_automation\Record_wav\kmb\*.wav*.fft")
                stdin, stdout, stderr = AutoEarHost.exec_command("DEL C:\\audio_automation\Gold_wav_file\gold\*.wav*.fft")
                cmd = "RENAME C:\\audio_automation\AudioCompare_Log\compare.log compare_" + "%date:~10,4%%date:~7,2%%date:~4,2%_%time:~0,2%%time:~3,2%" + "_volume_" + master + "_capture_" + capture + "_" + result + ".log"

                stdin, stdout, stderr = AutoEarHost.exec_command(cmd)
            
            else:
                message = "ERROR: AutoEar Result parsing error"
                print(message)
                write_log(logDir + logFile, message)
                verdict = False
                
            if verdict:
                message = "DEBUG: " + script_name + " has completed successfully.\n"
                print(message)
                write_log(logDir + logFile, message)
                print("....Audio execution completed")
            
            else:
                message = "ERROR: " + script_name + " has encountered an error during execution.\n"
                print(message)
                write_log(logDir + logFile, message)
                print(".....execution not completed")
                
            message = "\nDEBUG: " + script_name + " has completed trial run.\n" 

# Establish connection for remote execution
print("\n===========================================================================================")
try:
    
        print("Executing Test")
        import paramiko
        dut = paramiko.SSHClient()
        dut.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        dut.connect(hostname=dev_1_ip,username=target_user,password=target_pass,allow_agent=False,look_for_keys=False)
        
        AutoEarHost = paramiko.SSHClient()
        AutoEarHost.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        AutoEarHost.connect(hostname=earhost_ip,username='hspe',password='root@123',allow_agent=False,look_for_keys=False)
        AutoEarHost.exec_command("ipconfig")
except Exception as e:
    print("ERROR: "    + str(e))
    print("Something went wrong while establishing remote connection")
    print("Exiting...")
    sys.exit(1)
print("===========================================================================================")

"""
def Start_GenericCommandServer():
    command = os.popen('ps ax').read()
    #print("command:"+command)
    read_list = re.compile("\n").split(command)
    generic = True
    for line in read_list:
        if re.search("GenericCommandServer",line):          
            print("GenericCommandServer is Already Running")
            generic = False
            break
    if generic:
        subprocess.Popen(["python",workingDir+"GenericCommandServer.py"])
        subprocess.call(["echo","genericcommandserver is started"])
    else:
        print("done")
 
Start_GenericCommandServer();  
dut = GenericCommand.GenericCommand()
dut.login(dev_1_ip,gcs_port)
AutoEarHost = GenericCommand.GenericCommand()
AutoEarHost.login(earhost_ip, earhost_gcs_port)
"""
def main():
    dut.exec_command("echo 'here execute alsamixer commands'")
    if testid == "HD":
        rec_file = "HD_16b_48k"+get_current_date()+get_current_time()+".wav"
        stdin,stdout,stderr = dut.exec_command("gst-launch-1.0 filesrc location="+audioFileDir+"aaclc_enc.mp4 ! qtdemux ! aacparse ! avdec_aac ! audioconvert ! audio/x-raw,format=S16LE, channels=2 ! wavenc ! filesink location ="+rec_file_directory+rec_file)
        os.system("scp root@"+dev_1_ip+":"+rec_file_directory+rec_file+" "+rec_file_directory)
        gold_sample = gold_wav_base_location + "gold_HD_16b_48k.wav"
    
    elif testid == "ADPCM_decode":
        rec_file = "adpcm_dec"+get_current_date()+get_current_time()+".wav"
        stdin,stdout,stderr = dut.exec_command("gst-launch-1.0 filesrc location="+audioFileDir+"adpcm_enc.mka ! matroskademux ! adpcmdec ! audioconvert ! audio/x-raw,format=S16LE, channels=2 ! wavenc ! filesink location ="+rec_file_directory+rec_file)
        os.system("scp root@"+dev_1_ip+":"+rec_file_directory+rec_file+" "+rec_file_directory)
        gold_sample = gold_wav_base_location + "adpcm_dec.wav"
    elif testid == "16b_48k_2ch":
        rec_file = "16b_48k_2ch"+get_current_date()+get_current_time()+".wav"
        stdin,stdout,stderr = dut.exec_command("aplay -Dhw:0,1 -d10 "+audioFileDir+"16b_48k_2ch.wav & arecord -Dhw:0,1 -fS16_LE -c2 -r48000 -d10 "+rec_file_directory+rec_file)
        os.system("scp root@"+dev_1_ip+":"+rec_file_directory+rec_file+" "+rec_file_directory)
        gold_sample = gold_wav_base_location + "16b_48k_2ch.wav"
    elif testid == "HD_16b_48k":
        stdin,stdout,stderr = dut.exec_command("amixer -c0 cset numid=5,iface=MIXER,name='Capture Switch' on & amixer -c0 cset numid=3 1")
        rec_file = "adl_16bits_record"+get_current_date()+get_current_time()+".wav"
        stdin,stdout,stderr = dut.exec_command("arecord -d30 -vD hw:0,0 -fS16_LE -r48000 -c2 " + rec_file_directory + rec_file +" & aplay -d30 -vD hw:0,0 /home/AIC_HDA_HDMI_DP/16bits.wav")
        time.sleep(30)
        os.system("scp root@"+dev_1_ip+":"+rec_file_directory+rec_file+" "+rec_file_directory)
        gold_sample = gold_wav_base_location + "adl_16bits.wav"
		
    elif testid == "HD_32b_48k":
        rec_file = "HD_32b_48k"+get_current_date()+get_current_time()+".wav"
        stdin,stdout,stderr = dut.exec_command("amixer -c0 cset numid=5,iface=MIXER,name='Capture Switch' on & amixer -c0 cset numid=3 1")
        stdin,stdout,stderr = dut.exec_command("arecord -d30 -vD hw:0,0 -fS32_LE -r48000 -c2 " + rec_file_directory + rec_file +" & aplay -d30 -vD hw:0,0 /home/AIC_HDA_HDMI_DP/32bits.wav")
        time.sleep(30)
        os.system("scp root@"+dev_1_ip+":"+rec_file_directory+rec_file+" "+rec_file_directory)
        gold_sample = gold_wav_base_location + "32bits_gold.wav"

    elif testid == "SOF_16b_48k":
        rec_file = "sof_16b_48k"+get_current_date()+get_current_time()+".wav"
        #stdin,stdout,stderr = dut.exec_command("amixer -c0 cset numid=5,iface=MIXER,name='Capture Switch' on & amixer -c0 cset numid=3 1")
        stdin,stdout,stderr = dut.exec_command("arecord -d30 -vD hw:0,0 -fS16_LE -r48000 -c2 " + rec_file_directory + rec_file +" & aplay -d30 -vD hw:0,0 /home/AIC_HDA_HDMI_DP/16bits.wav")
        time.sleep(30)
        os.system("scp root@"+dev_1_ip+":"+rec_file_directory+rec_file+" "+rec_file_directory)
        gold_sample = gold_wav_base_location + "gold_sof_16b.wav"
		
    elif testid == "SOF_32b_48k":
        rec_file = "sof_32b_48k"+get_current_date()+get_current_time()+".wav"
        #stdin,stdout,stderr = dut.exec_command("amixer -c0 cset numid=5,iface=MIXER,name='Capture Switch' on & amixer -c0 cset numid=3 1")
        stdin,stdout,stderr = dut.exec_command("arecord -d10 -vD plughw:0,0 -fS32_LE -r48000 -c2 " + rec_file_directory + rec_file +" & aplay -d10 -vD plughw:0,0 /home/AIC_HDA_HDMI_DP/32bits.wav")
        time.sleep(30)
        os.system("scp root@"+dev_1_ip+":"+rec_file_directory+rec_file+" "+rec_file_directory)
        gold_sample = gold_wav_base_location + "gold_sof_32b.wav"
    else:
        stdin,stdout,stderr = dut.exec_command("echo 'no test case' ")
        sys.exit(1)
    print("Test done....")
    file_transfered(rec_file)
    Autoear_result_check(True,gold_sample,rec_file)

if __name__ == "__main__":
    main()
    
## EOF


