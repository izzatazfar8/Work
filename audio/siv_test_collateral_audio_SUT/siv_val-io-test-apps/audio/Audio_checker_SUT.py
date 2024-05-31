# Load Audio Built In driver 
# 
# Author: Jepson
# Created: 17 FEB 2020
# Updated: 15 JUL 2020


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

def sof_checker():
    print("----- SOF Checking -----")

    if os.path.isfile("/home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/check_onboard_sof.log") == 0:
        print("Check onboard ALSA file is missing !!! Exiting ...")
        sys.exit(0)
    
    os.system("dmesg | grep sof > /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/sut_check_sof.log")
    os.system("cat /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/sut_check_sof.log | cut -c16- | sed -n '3,22p' > /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/final_sof.log")	
    os.system(
        "diff /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/final_sof.log /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/check_onboard_sof.log > /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/sof_compare1.log")
    if os.stat("/home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/sof_compare1.log").st_size == 0:
        mod_check = 1
        print("\n")
        print("SOF checker : PASS \n")
    else:
        mod_check = 0
        print("\n")
        print("SOF checker : FAIL \n")




def modules_filter():
    print("----- Second steps -----")

    with open("/home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/sut_check_lsmod.log", "r") as fil:
        data = fil.readlines()

        for line in data:
            words = line.split()
            # print words[0]
            with open("/home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/f_sut_check_lsmod.log",
                      "a") as fil2:
                fil2.write(words[0])
                fil2.write("\n")


def modules_checker():
    os.system("rm -rf /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/sut_check_lsmod.log; rm -rf /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/f_sut_check_lsmod.log")

    print("----- Modules Checking -----")

    if os.path.isfile("/home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/check_onboard_module.log") == 0:
        print("Check Module file is missing !!! Exiting ...")
        sys.exit(0)
    # need to edit with new kernel release
    os.system("lsmod | grep -i snd > /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/sut_check_lsmod.log")
    modules_filter()
    os.system(
        "grep -Ff /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/f_sut_check_lsmod.log /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/check_onboard_module.log > /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/module_compare.log")
    os.system(
        "diff /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/module_compare.log /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/check_onboard_module.log > /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/module_compare1.log")
    if os.stat("/home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/module_compare1.log").st_size == 0:
        mod_check = 1
        print("\n")
        print("Modules checker : PASS \n")
    else:
        mod_check = 0
        print("\n")
        print("Modules checker : FAIL \n")


"""def alsa_checker():
    print("----- ALSA Checking -----")

    if os.path.isfile("/home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/check_onboard_alsa.log") == 0:
        print("Check onboard ALSA file is missing !!! Exiting ...")
        sys.exit(0)
    # need to edit kernel release
    os.system("aplay -l > /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/sut_check_alsa.log")
    os.system(
        "diff /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/sut_check_alsa.log /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/check_onboard_alsa.log > /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/alsa_compare1.log")
    if os.stat("/home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/alsa_compare1.log").st_size == 0:
        mod_check = 1
        print("\n")
        print("ALSA checker : PASS \n")
    else:
        mod_check = 0
        print("\n")
        print("ALSA checker : FAIL \n")

"""

def alsa_checker():
    print("----- Alsa Checker -----")
   
    os.system("dmesg | grep audio > /home/root/alsa_checker.log")

    #verdict = false
    
    with open('/home/root/alsa_checker.log') as f:
        if 'snd_hda_intel' in f.read():
          print ("Alsa Checker PASS")
        else:
          print ("Alsa Checker FAILED")
    
	
def onboard_hdmi_checker():
    print("----- ALSA Checking -----")

    if os.path.isfile("/home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/check_onboard_hdmi_alsa.log") == 0:
        print("Check HDMI ALSA file is missing !!! Exiting ...")
        sys.exit(0)
    # need to edit with new kernel release
    os.system("aplay -l > /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/sut_check_hdmi_alsa.log")
    os.system("diff /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/sut_check_hdmi_alsa.log /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/check_onboard_hdmi_alsa.log > /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/hdmi_alsa_compare1.log")
    if os.stat("/home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/hdmi_alsa_compare1.log").st_size == 0:
        mod_check = 1
        print("\n")
        print("ALSA checker : PASS \n")
    else:
        mod_check = 0
        print("\n")
        print("ALSA checker : FAIL \n")


def f_16bit_48k():
    print("----- 16bits Bitdepth Checking -----")

    if os.path.isfile("/home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/check_onboard_16bits_format.log") == 0:
        print("Check bit depth file is missing !!! Exiting ...")
        sys.exit(0)

    audio_file_dir = "/home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_wav_files/2ch_48k_s16_le.wav"
    cmd_playback = "aplay -vD hw:0,0 " + audio_file_dir + " 2> /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/sut_check_16bitdepth.log"

    print(cmd_playback)
    os.system(cmd_playback)
    time.sleep(5)

    os.system("diff /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/sut_check_16bitdepth.log /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/check_onboard_16bits_format.log > /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/16bitdepth_compare1.log")
    if os.stat("/home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/16bitdepth_compare1.log").st_size == 0:
        mod_check = 1
        print("\n")
        print("Bitdepth checker : PASS \n")
    else:
        mod_check = 0
        print("\n")
        print("Bitdepth checker : FAIL \n")


def f_32bit_48k():
    print("----- 32bits Bitdepth Checking -----")

    if os.path.isfile("/home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/check_onboard_32bits_format.log") == 0:
        print("Check bit depth file is missing !!! Exiting ...")
        sys.exit(0)

    audio_file_dir = "/home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_wav_files/2ch_48k_s32_le.wav"
    cmd_playback = "aplay -vD hw:0,0 " + audio_file_dir + " 2> /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/sut_check_32bitdepth.log"

    print(cmd_playback)
    os.system(cmd_playback)
    time.sleep(5)

    os.system("diff /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/sut_check_32bitdepth.log /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/check_onboard_32bits_format.log > /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/32bitdepth_compare1.log")
    if os.stat("/home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/32bitdepth_compare1.log").st_size == 0:
        mod_check = 1
        print("\n")
        print("Bitdepth checker : PASS \n")
    else:
        mod_check = 0
        print("\n")
        print("Bitdepth checker : FAIL \n")

def f_16bit_8k():
    print("----- 32bits Bitdepth Checking -----")

    if os.path.isfile("/home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/check_f_16bit_8k.log") == 0:
        print("Check bit depth file is missing !!! Exiting ...")
        sys.exit(0)

    audio_file_dir = "/home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_wav_files/2ch_8k_s16_le.wav"
    cmd_playback = "aplay -vD hw:0,0 " + audio_file_dir + " 2> /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/sut_check_f_16bit_8k.log"

    print(cmd_playback)
    os.system(cmd_playback)
    time.sleep(5)

    os.system("diff /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/sut_check_f_16bit_8k.log /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/check_f_16bit_8k_format.log > /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/f_16bit_8k_compare1.log")
    if os.stat("/home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/f_16bit_8k_compare1.log").st_size == 0:
        mod_check = 1
        print("\n")
        print("Bitdepth checker : PASS \n")
    else:
        mod_check = 0
        print("\n")
        print("Bitdepth checker : FAIL \n")

def f_32bit_8k():
    print("----- 32bits Bitdepth Checking -----")

    if os.path.isfile("/home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/check_f_32bit_8k.log") == 0:
        print("Check bit depth file is missing !!! Exiting ...")
        sys.exit(0)

    audio_file_dir = "/home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_wav_files/2ch_8k_s32_le.wav"
    cmd_playback = "aplay -vD plughw:0,0 " + audio_file_dir + " 2> /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/sut_check_f_32bit_8k.log"

    print(cmd_playback)
    os.system(cmd_playback)
    time.sleep(5)

    os.system("diff /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/sut_check_f_32bit_8k.log /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/check_f_32bit_8k.log > /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/f_32bit_8k_compare1.log")
    if os.stat("/home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/f_32bit_8k_compare1.log").st_size == 0:
        mod_check = 1
        print("\n")
        print("Bitdepth checker : PASS \n")
    else:
        mod_check = 0
        print("\n")
        print("Bitdepth checker : FAIL \n")

def f_16bit_16k():
    print("----- 32bits Bitdepth Checking -----")

    if os.path.isfile("/home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/check_f_16bit_16k.log") == 0:
        print("Check bit depth file is missing !!! Exiting ...")
        sys.exit(0)

    audio_file_dir = "/home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_wav_files/2ch_16k_s16_le.wav"
    cmd_playback = "aplay -vD hw:0,0 " + audio_file_dir + " 2> /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/sut_check_f_16bit_16k.log"

    print(cmd_playback)
    os.system(cmd_playback)
    time.sleep(5)

    os.system("diff /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/sut_check_f_16bit_16k.log /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/check_f_16bit_16k.log > /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/f_16bit_16k_compare1.log")
    if os.stat("/home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/f_16bit_16k_compare1.log").st_size == 0:
        mod_check = 1
        print("\n")
        print("Bitdepth checker : PASS \n")
    else:
        mod_check = 0
        print("\n")
        print("Bitdepth checker : FAIL \n")
		
def f_32bit_16k():
    print("----- 32bits Bitdepth Checking -----")

    if os.path.isfile("/home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/check_f_32bit_16k.log") == 0:
        print("Check bit depth file is missing !!! Exiting ...")
        sys.exit(0)

    audio_file_dir = "/home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_wav_files/2ch_16k_s32_le.wav"
    cmd_playback = "aplay -vD hw:0,0 " + audio_file_dir + " 2> /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/sut_check_f_32bit_16k.log"

    print(cmd_playback)
    os.system(cmd_playback)
    time.sleep(5)

    os.system("diff /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/sut_check_f_32bit_16k.log /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/check_f_32bit_16k.log > /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/f_32bit_16k_compare1.log")
    if os.stat("/home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/f_32bit_16k_compare1.log").st_size == 0:
        mod_check = 1
        print("\n")
        print("Bitdepth checker : PASS \n")
    else:
        mod_check = 0
        print("\n")
        print("Bitdepth checker : FAIL \n")		


def sof_16b():
    print("----- 16bits Bitdepth SOF Checking -----")

    if os.path.isfile("/home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/sof_debug_check_16b.log") == 0:
        print("Check bit depth file is missing !!! Exiting ...")
        sys.exit(0)

    audio_file_dir = "/home/AIC_HDA_HDMI_DP/16bits.wav"
    cmd_playback = "aplay -d10 -vD hw:0,0 " + audio_file_dir + " 2> /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/sut_check_sof_16b.log"

    print(cmd_playback)
    os.system(cmd_playback)
    time.sleep(5)

    os.system("diff /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/sut_check_sof_16b.log /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/sof_debug_check_16b.log > /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/sof_16b_compare1.log")
    if os.stat("/home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/sof_16b_compare1.log").st_size == 0:
        mod_check = 1
        print("\n")
        print("Bitdepth checker : PASS \n")
    else:
        mod_check = 0
        print("\n")
        print("Bitdepth checker : FAIL \n")	

def snd_hda():
    print("----- snd_hda Checking -----")
    os.system("dmesg | grep audio > /home/root/snd_hda.log")

    #verdict = false
    with open('/home/root/snd_hda.log') as f:
        if 'snd_hda' in f.read():
          print ("snd_hda PASS")
        else:
          print ("snd_hda FAILED")
def hdaudioC0D0():
    print("----- hdaudioC0D0 Checking -----")
    os.system("dmesg | grep audio > /home/root/hdaudioC0D0.log")

    #verdict = false
    with open('/home/root/hdaudioC0D0.log') as f:
        if 'hda' in f.read():
          print ("hdaudioC0D0 PASS")
        else:
          print ("hdaudioC0D0 FAILED")
def mic_jack():
    print("----- mic_jack Checking -----")
    os.system("amixer -c0 contents > /home/root/mic_jack.log")

    #verdict = false
    with open('/home/root/mic_jack.log') as f:
        if 'Jack' in f.read():
          print ("mic_jack PASS")
        else:
          print ("mic_jack FAILED")

def playback_switch():
    print("----- playback_switch Checking -----")
    os.system("amixer -c0 contents > /home/root/playback_switch.log")

    #verdict = false
    with open('/home/root/playback_switch.log') as f:
        if 'Playback' in f.read():
          print ("playback_switch PASS")
        else:
          print ("playback_switch FAILED")
def capture_switch():
    print("----- capture_switch Checking -----")
    os.system("amixer -c0 contents > /home/root/capture_switch.log")

    #verdict = false
    with open('/home/root/capture_switch.log') as f:
        if 'Playback' in f.read():
          print ("capture_switch PASS")
        else:
          print ("capture_switch FAILED")

def aplay():
    print("----- aplay Checking -----")
    os.system("aplay -l > /home/root/aplay.log")

    #verdict = false
    with open('/home/root/aplay.log') as f:
        if 'HDA Intel PCH' in f.read():
          print ("aplay PASS")
        else:
          print ("aplay FAILED")
def aplay_snd():
    print("----- aplay Checking -----")
    os.system("aplay -l > /home/root/aplay_snd.log")

    #verdict = false
    with open('/home/root/aplay_snd.log') as f:
        if 'sof-soundwire' in f.read():
          print ("Test PASS")
        else:
          print ("Test FAILED")
def arecord():
    print("----- arecord Checking -----")
    os.system("arecord -l > /home/root/arecord.log")

    #verdict = false
    with open('/home/root/arecord.log') as f:
        if 'CAPTURE Hardware Devices' in f.read():
          print ("arecord PASS")
        else:
          print ("arecord FAILED")
def audio_lib():
    print("----- audio_lib Checking -----")
    os.system("lsmod > /home/root/audio_lib.log")

    #verdict = false
    with open('/home/root/audio_lib.log') as f:
        if 'snd_hda_codec' in f.read():
          print ("audio_lib PASS")
        else:
          print ("audio_lib FAILED")
def rt5660_codec():
    print("----- rt5660_codec Checking -----")
    os.system("aplay -l > /home/root/rt5660_codec.log")

    #verdict = false
    with open('/home/root/rt5660_codec.log') as f:
        if 'card 0: sofehlrt5660 [sof-ehl-rt5660], device 0: Headset' in f.read():
          print ("rt5660_codec PASS")
        else:
          print ("rt5660_codec FAILED")
def rt5660_modules():
    print("----- rt5660_modules Checking -----")
    os.system("lsmod | grep -i snd > /home/root/rt5660_modules.log")

    #verdict = false
    with open('/home/root/rt5660_modules.log') as f:
        if 'snd_soc_ehl_rt5660' in f.read():
          print ("rt5660_modules PASS")
        else:
          print ("rt5660_modules FAILED")
def rt5660_arecord():
    print("----- rt5660_arecord Checking -----")
    os.system("arecord -l > /home/root/rt5660_arecord.log")

    #verdict = false
    with open('/home/root/rt5660_arecord.log') as f:
        if 'card 0: sofehlrt5660 [sof-ehl-rt5660], device 0: Headset' in f.read():
          print ("rt5660_arecord PASS")
        else:
          print ("rt5660_arecord FAILED")
def usb_32bits():
    print("----- 32bits_usb Checking -----")
    os.system("aplay -Dhw:1,0 -r48000 -fs16_le -c2 -vvv 16bits.wav > /home/root/32bits_usb.log")

    with open('/home/root/32bits_usb.log') as f:
        if 'Max peak (12000 samples): 0x000054d4 ####' in f.read():
          print ("32bits_usb PASS")
        else:
          print ("32bits_usb FAILED. Please connect any USB headset/speaker to USB Port")
def usb_16bits():
    print("----- usb_16bits Checking -----")
    os.system("aplay -Dhw:1,0 -r48000 -fs16_le -c2 -vvv 16bits.wav > /home/root/usb_16bits.log")

    with open('/home/root/usb_16bits.log') as f:
        if 'Max peak (12000 samples): 0x000054d4 ####' in f.read():
          print ("usb_16bits PASS")
        else:
          print ("usb_16bits FAILED. Please connect any USB headset/speaker to USB Port")
def dp_16bits():
    print("----- dp_16bits Checking -----")
    os.system("aplay -Dhw:0,3 -r48000 -fs16_le -c2 -vvv 16bits.wav > /home/root/dp_16bits.log")

    with open('/home/root/dp_16bits.log') as f:
        if 'Max peak (12000 samples): 0x000054d4 ####' in f.read():
          print ("dp_16bits PASS")
        else:
          print ("dp_16bits FAILED. Please connect SUT to Monitor via DP, then audio jack speaker/headset to audio jack from monitor")
def dp_32bits():
    print("----- dp_32bits Checking -----")
    os.system("aplay -Dhw:0,3 -r48000 -fs16_le -c2 -vvv 16bits.wav > /home/root/dp_32bits.log")

    with open('/home/root/dp_32bits.log') as f:
        if 'Max peak (12000 samples): 0x000054d4 ####' in f.read():
          print ("dp_32bits PASS")
        else:
          print ("dp_32bits FAILED. Please connect SUT to Monitor via DP, then audio jack speaker/headset to audio jack from monitor")	

def play_16bits():
    print("----- play_16bits Checking -----")
    os.system("aplay -Dhw:0,0 -r48000 -fs16_le -c2 -vvv 16bits.wav > /home/root/play_16bits.log")

    with open('/home/root/play_16bits.log') as f:
        if 'Max peak (12000 samples): 0x000054d4 ####' in f.read():
          print ("play_16bits PASS")
        else:
          print ("play_16bits FAILED.")

def record_16bits():
    print("----- record_16bits Checking -----")
    os.system("arecord -D hw:0,0 -r 48000 -c 2 -fS16_LE recorded_1.wav -vvv > /home/root/record_16bits.log")

    with open('/home/root/record_16bits.log') as f:
        if 'Max peak (12000 samples): 0x000054d4 ####' in f.read():
          print ("record_16bits PASS")
        else:
          print ("record_16bits FAILED.")

def play_16bits_sof():
    print("----- play_16bits_sof Checking -----")
    os.system("aplay -Dhw:0,0 -r48000 -fs16_le -c2 -vvv 16bits.wav > /home/root/play_16bits_sof.log")

    with open('/home/root/play_16bits_sof.log') as f:
        if 'Max peak (12000 samples): 0x000054d4 ####' in f.read():
          print ("play_16bits_sof PASS")
        else:
          print ("play_16bits_sof FAILED.")

def record_16bits_sof():
    print("----- record_16bits_sof Checking -----")
    os.system("arecord -D hw:0,0 -r 48000 -c 2 -fS16_LE recorded_1.wav -vvv > /home/root/record_16bits_sof.log")

    with open('/home/root/record_16bits_sof.log') as f:
        if 'Max peak (12000 samples): 0x000054d4 ####' in f.read():
          print ("record_16bits_sof PASS")
        else:
          print ("record_16bits_sof FAILED.")

def play_32bits_sof():
    print("----- play_32bits_sof Checking -----")
    os.system("aplay -D plughw:0,0 -r48000 -fs32_le -c2 -vvv 32bits.wav > /home/root/play_32bits_sof.log")

    with open('/home/root/play_32bits_sof.log') as f:
        if 'Max peak (12000 samples): 0x000054d4 ####' in f.read():
          print ("play_32bits_sof PASS")
        else:
          print ("play_32bits_sof FAILED.")

def record_32bits_sof():
    print("----- record_32bits_sof Checking -----")
    os.system("arecord -D plughw:0,0 -r 48000 -c 2 -fS32_LE recorded_1.wav -vvv > /home/root/record_32bits_sof.log")

    with open('/home/root/record_32bits_sof.log') as f:
        if 'Max peak (12000 samples): 0x000054d4 ####' in f.read():
          print ("record_32bits_sof PASS")
        else:
          print ("record_32bits_sof FAILED.")

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

    if os.path.isdir("/home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log") == 0:
        os.system("mkdir /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log")
    elif os.path.isdir("/home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log") == 1:
        print("Audio_log directory existed... Execution continue...")
    else:
        print("Audio_log directory is missing...")
        sys.exit(0)

    if args.c == "modules":
        modules_checker()
    elif args.c == "alsa":
        modules_checker()
    elif args.c == "alsa_hdmi":
        onboard_hdmi_checker()
    elif args.b == "16" and args.s == "48":
        f_16bit_48k()
    elif args.b == "32" and args.s == "48":
        f_32bit_48k()
	
    elif args.b == "16" and args.s == "8":
        f_16bit_8k()
    elif args.b == "32" and args.s == "8":
        f_32bit_8k()
    elif args.b == "16" and args.s == "16":
        f_16bit_16k()
    elif args.b == "32" and args.s == "16":
        f_32bit_16k()
    elif args.c == "sof_16b":
        sof_16b()
    elif args.c == "sof":
        sof_checker()

    elif args.c == "snd_hda":
        snd_hda()
    elif args.c == "hdaudioC0D0":
        hdaudioC0D0()
    elif args.c == "mic_jack":
        mic_jack()
    elif args.c == "playback_switch":
        playback_switch()
    elif args.c == "capture_switch":
        capture_switch()
    elif args.c == "aplay":
        aplay()
    elif args.c == "aplay_snd":
        aplay_snd()
    elif args.c == "arecord":
        arecord()
    elif args.c == "audio_lib":
        audio_lib()
    elif args.c == "rt5660_codec":
        rt5660_codec()
    elif args.c == "rt5660_modules":
        rt5660_modules()
    elif args.c == "rt5660_arecord":
        rt5660_arecord()
    elif args.c == "32bits_usb":
        audio_lib()
    elif args.c == "16bits_usb":
        aplay()
    elif args.c == "16bits_dp":
        dp_16bits()
    elif args.c == "32bits_dp":
        dp_32bits()
    elif args.c == "16bits_play":
        play_16bits()
    elif args.c == "16bits_record":
        record_16bits()
    elif args.c == "16bits_play_sof":
        play_16bits_sof()
    elif args.c == "16bits_record_sof":
        record_16bits_sof()
    elif args.c == "32bits_play_sof":
        play_32bits_sof()
    elif args.c == "32bits_record_sof":
        record_32bits_sof()
    else:
        print("Invalid parameters !! ")
        sys.exit(0)


main()
