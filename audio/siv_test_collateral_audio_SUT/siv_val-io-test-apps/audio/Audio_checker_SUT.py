# Load Audio Built In driver 
# Created: 17 FEB 2020
# Updated: 15 JUL 2020


import os
import argparse
import sys
import subprocess
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
    print("----- SOF Checker -----")
   
    os.system("dmesg | grep sof > /home/user/sof_checker.log")

    #verdict = false
    
    with open('/home/user/sof_checker.log') as f:
        if 'SoundWire enabled' in f.read():
          print ("SOF Checker PASS")
        else:
          print ("SOF Checker FAILED. No SOF is loaded from dmesg. Please ensure SOF .ri and .tplg are placed in correct path and SOF BIOS settings configured")




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

    if os.path.isfile("/home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/check_onboard_module.log") == 0:
        print("Check Module file is missing !!! Exiting ...")
        sys.exit(0)
    # need to edit with new kernel release
    os.system("lsmod | grep -i snd > /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/sut_check_lsmod.log")
    modules_filter()
    os.system(
        "grep -Ff /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/f_sut_check_lsmod.log /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/check_onboard_module.log > /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/module_compare.log")
    os.system(
        "diff /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/module_compare.log /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/check_onboard_module.log > /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/module_compare1.log")
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
   
    os.system("lsmod > /home/user/alsa_checker.log")

    #verdict = false
    
    with open('/home/user/alsa_checker.log') as f:
        if 'snd_hda' in f.read():
          print ("Alsa Checker PASS")
        else:
          print ("Alsa Checker FAILED. No audio found in 'lsmod' command.")
    
	
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
    os.system("lsmod > /home/user/snd_hda.log")

    #verdict = false
    with open('/home/user/snd_hda.log') as f:
        if 'snd_hda' in f.read():
          print ("snd_hda PASS")
        else:
          print ("snd_hda FAILED. No audio found in 'lsmod' command. Kindly check if Audio has merged into this BKC.")
def hdaudioC0D0():
    print("----- hdaudioC0D0 Checking -----")
    os.system("lsmod > /home/user/hdaudioC0D0.log")

    #verdict = false
    with open('/home/user/hdaudioC0D0.log') as f:
        if 'hda' in f.read():
          print ("snd_hda_intel PASS")
        else:
          print ("snd_hda_intel FAILED. No audio found in 'lsmod; command. Kindly check if Audio has merged into this BKC")
def mic_jack():
    print("----- mic_jack Checking -----")
    os.system("amixer -c0 contents > /home/user/mic_jack.log")

    #verdict = false
    with open('/home/user/mic_jack.log') as f:
        if 'Jack' in f.read():
          print ("mic_jack PASS")
        else:
          print ("mic_jack FAILED. No onboard jack found in 'amixer -c0 contents'. Kindly run 'aplay -l' to confirm if audio is loaded.")

def playback_switch():
    print("----- playback_switch Checking -----")
    os.system("amixer -c0 contents > /home/user/playback_switch.log")

    #verdict = false
    with open('/home/user/playback_switch.log') as f:
        if 'Playback' in f.read():
          print ("playback_switch PASS")
        else:
          print ("playback_switch FAILED. No PLAYBACK found in 'amixer -c0 contents'. Kindly run 'aplay -l' to confirm if audio is loaded.")
def capture_switch():
    print("----- capture_switch Checking -----")
    os.system("amixer -c0 contents > /home/user/capture_switch.log")

    #verdict = false
    with open('/home/user/capture_switch.log') as f:
        if 'Playback' in f.read():
          print ("capture_switch PASS")
        else:
          print ("capture_switch FAILED. No PLAYBACK found in 'amixer -c0 contents'. Kindly run 'aplay -l' to confirm if audio is loaded")

def aplay():
    print("----- aplay Checking -----")
    os.system("aplay -l > /home/user/aplay.log")

    #verdict = false
    with open('/home/user/aplay.log') as f:
        if 'HDA Intel PCH' or 'sof' in f.read():
          print ("aplay PASS")
        else:
          print ("aplay FAILED. Audio fail to load. Please ensure you are using correct BIOS settings for HDA, and for SOF using correct .ri and .tplg which are placed in correct path and SOF BIOS settings configured ")
def arecord():
    print("----- arecord Checking -----")
    os.system("arecord -l > /home/user/arecord.log")

    #verdict = false
    with open('/home/user/arecord.log') as f:
        if 'CAPTURE Hardware Devices' in f.read():
          print ("arecord PASS")
        else:
          print ("arecord FAILED. Audio fail to load. Please ensure you are using correct BIOS settings for HDA, and for SOF using correct .ri and .tplg which are placed in correct path and SOF BIOS settings configured")
def aplay_snd():
    print("----- aplay_snd Checking -----")
    os.system("aplay -l > /home/user/aplay_snd.log")

    #verdict = false
    with open('/home/user/aplay_snd.log') as f:
        if 'sof-soundwire' in f.read():
          print ("aplay PASS")
        else:
          print ("aplay FAILED. Soundwire Audio fail to load. Please ensure .ri and .tplg  are placed in correct path and Soundwire BIOS settings configured")
def arecord_snd():
    print("----- arecord Checking -----")
    os.system("arecord -l > /home/user/arecord_snd.log")

    #verdict = false
    with open('/home/user/arecord_snd.log') as f:
        if 'sof-soundwire' in f.read():
          print ("arecord PASS")
        else:
          print ("arecord FAILED. Soundwire Audio fail to load. Please ensure .ri and .tplg  are placed in correct path and Soundwire BIOS settings configured")
def snd():
    print("----- snd Checking -----")
    os.system("dmesg | grep audio > /home/user/snd.log")

    #verdict = false
    with open('/home/user/snd.log') as f:
        if 'snd_intel' in f.read():
          print ("snd PASS")
        else:
          print ("snd FAILED. Soundwire Audio fail to load. Please ensure .ri and .tplg  are placed in correct path and Soundwire BIOS settings configured")
def lspci():
    print("----- lspci Checking -----")
    os.system("lspci > /home/user/lspci.log")

    #verdict = false
    with open('/home/user/lspci.log') as f:
        if 'Multimedia audio controller' in f.read():
          print ("lspci PASS")
        else:
          print ("lspci FAILED, No Audio found in 'lspci command.")
def audio_lib():
    print("----- audio_lib Checking -----")
    os.system("lsmod > /home/user/audio_lib.log")

    #verdict = false
    with open('/home/user/audio_lib.log') as f:
        if 'snd_hda_codec' in f.read():
          print ("audio_lib PASS")
        else:
          print ("audio_lib FAILED. No 'snd_hda_codec' found in 'lsmod' command, please ensure audio is loaded in 'aplay -l' command.")
def rt5660_codec():
    print("----- rt5660_codec Checking -----")
    os.system("aplay -l > /home/user/rt5660_codec.log")

    #verdict = false
    with open('/home/user/rt5660_codec.log') as f:
        if 'card 0: sofehlrt5660 [sof-ehl-rt5660], device 0: Headset' in f.read():
          print ("rt5660_codec PASS")
        else:
          print ("rt5660_codec FAILED. No 'sofehlrt5660' found in 'aplay -l' command, please ensure you are using right rt5660 AIC .")
def rt5660_modules():
    print("----- rt5660_modules Checking -----")
    os.system("lsmod | grep -i snd > /home/user/rt5660_modules.log")

    #verdict = false
    with open('/home/user/rt5660_modules.log') as f:
        if 'snd_soc_ehl_rt5660' in f.read():
          print ("rt5660_modules PASS")
        else:
          print ("rt5660_modules FAILED. No 'sofehlrt5660' found in 'aplay -l' command, please ensure you are using right rt5660 AIC")
def rt5660_arecord():
    print("----- rt5660_arecord Checking -----")
    os.system("arecord -l > /home/user/rt5660_arecord.log")

    #verdict = false
    with open('/home/user/rt5660_arecord.log') as f:
        if 'card 0: sofehlrt5660 [sof-ehl-rt5660], device 0: Headset' in f.read():
          print ("rt5660_arecord PASS")
        else:
          print ("rt5660_arecord FAILED. No 'sofehlrt5660' found in 'aplay -l' command, please ensure you are using right rt5660 AIC")
def usb_32bits():
    print("----- 32bits_usb Checking. Please ensure USB headset is connected -----")
    os.system("aplay -l >> /home/user/play_32bits.log")

    with open('/home/user/play_32bits.log') as f:
        if 'USB' in f.read():
          print ("32bits_usb PASS")
        else:
          print ("32bits_usb FAILED. Please connect any USB headset/speaker to USB Port and remove 'blacklist_hda.conf in system at path /etc/modprobe/")
def usb_16bits():
    print("----- usb_16bits Checking -----")
    os.system("aplay -Dhw:1,0 -r48000 -fs16_le -c2 -vvv 16bits.wav >> /home/user/play_16bits.log")

    with open('/home/user/play_16bits.log') as f:
        if 'stream:PLAYBACK' in f.read():
          print ("usb_16bits PASS")
        else:
          print ("usb_16bits FAILED. Please connect any USB headset/speaker to USB Port and remove 'blacklist_hda.conf in system at path /etc/modprobe/")
def dp_16bits():
    print("----- dp_16bits Checking -----")
    os.system("aplay -l > /home/user/dp_16bits.log")

    with open('/home/user/dp_16bits.log') as f:
        if 'HDMI 0' in f.read():
          print ("dp_16bits PASS")
        else:
          print ("dp_16bits FAILED. Please connect SUT to Monitor via DP, then audio jack speaker/headset to audio jack from monitor")
def dp_32bits():
    print("----- dp_32bits Checking -----")
    os.system("aplay -l  > /home/user/dp_32bits.log")

    with open('/home/user/dp_32bits.log') as f:
        if 'HDMI 0' in f.read():
          print ("dp_32bits PASS")
        else:
          print ("dp_32bits FAILED. Please connect SUT to Monitor via DP, then audio jack speaker/headset to audio jack from monitor")	

def play_16bits():
    print("----- play_16bits Checking -----")
    # Run aplay first
    output = os.popen("aplay -l | grep -E 'HDA|sof|SND'").read()

    if 'HDA' in output or 'sof' in output:
        # If output "HDA" or "sof"
        command = "sudo aplay -Dhw:0,0 -r48000 -fs16_le -c2 -d1 -vvv /home/user/16bits.wav"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

    elif 'sof-soundwire' in output:
        # If output "SND"
        command = "sudo aplay -Dhw:0,1 -r48000 -fs16_le -c2 -d1 -vvv /home/user/16bits.wav"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
    else:
        # If none of the expected outputs are found
        print("Audio HDA/SOF/SND is not loaded, for HDA/SOF, please check on AIC connection and ensure BIOS settings is configured, for SND, please ensure .ri and .tplg is placed correctly and BIOS settings is configured properly.")

    # Check if "stream:PLAYBACK" is present in the log file
    log_file = "/home/user/play_16bits.log"
    with open(log_file, "a") as f:
        f.write(stdout.decode("utf-8"))
        f.write(stderr.decode("utf-8"))
    with open('/home/user/play_16bits.log') as f:
        if 'PLAYBACK' in f.read():
            print("TEST PASS")
        else:
            print("TEST FAIL. Playback is failing might be due to 1) Change of -Dhw:x,x 2) Other playback process is still running. 3) Missing audio playback file in /home/user ")

def record_16bits():
    print("----- record_16bits Checking -----")
    # Run arecord first
    output = os.popen("arecord -l | grep -E 'HDA|sof|SND'").read()

    if 'HDA' in output or 'sof' in output:
        # If output "HDA" or "sof"
        command = "sudo arecord -Dhw:0,0 -r48000 -fs16_le -c2 -d1 -vvv"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

    elif 'sof-soundwire' in output:
        # If output "SND"
        command = "sudo arecord -Dhw:0,1 -r48000 -fs16_le -c2 -d1 -vvv"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
    else:
        # If none of the expected outputs are found
        print("Audio HDA/SOF/SND is not loaded, for HDA/SOF, please check on AIC connection and ensure BIOS settings is configured, for SND, please ensure .ri and .tplg is placed correctly and BIOS settings is configured properly.")

    # Check if "stream:CAPTURE" is present in the log file
    log_file = "/home/user/record_16bits.log"
    with open(log_file, "a") as f:
        f.write(stdout.decode("utf-8", errors="ignore"))
        f.write(stderr.decode("utf-8", errors="ignore"))
    with open('/home/user/record_16bits.log') as f:
        if 'CAPTURE' in f.read():
            print("TEST PASS")
        else:
            print("TEST FAIL. Recording is failing might be due to 1) Change of -Dhw:x,x 2) Other playback process is still running. 3) Missing audio playback file in /home/user ")

def play_32bits():
    print("----- play_32bits Checking -----")
    # Run aplay first
    output = os.popen("aplay -l | grep -E 'HDA|sof|SND'").read()

    if 'HDA' in output or 'sof' in output:
        # If output "HDA" or "sof"
        command = "sudo aplay -D plughw:0,0 -r48000 -fs32_le -c2 -d1 -vvv /home/user/32bits.wav"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

    elif 'sof-soundwire' in output:
        # If output "SND"
        command = "sudo aplay -D plughw:0,1 -r48000 -fs32_le -c2 -d1 -vvv /home/user/32bits.wav"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
    else:
        # If none of the expected outputs are found
        print("Audio HDA/SOF/SND is not loaded, for HDA/SOF, please check on AIC connection and ensure BIOS settings is configured, for SND, please ensure .ri and .tplg is placed correctly and BIOS settings is configured properly.")

    # Check if "stream:PLAYBACK" is present in the log file
    log_file = "/home/user/play_32bits.log"
    with open(log_file, "a") as f:
        f.write(stdout.decode("utf-8"))
        f.write(stderr.decode("utf-8"))
    with open('/home/user/play_32bits.log') as f:
        if 'PLAYBACK' in f.read():
            print("TEST PASS")
        else:
            print("TEST FAIL. Playback is failing might be due to 1) Change of -Dhw:x,x 2) Other playback process is still running. 3) Missing audio playback file in /home/user ")
		
def record_32bits():
    print("----- record_32bits Checking -----")
    # Run arecord first
    output = os.popen("arecord -l | grep -E 'HDA|sof|SND'").read()

    if 'HDA' in output or 'sof' in output:
        # If output "HDA" or "sof"
        command = "sudo arecord -D plughw:0,0 -r48000 -fs32_le -c2 -d1 -vvv"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

    elif 'sof-soundwire' in output:
        # If output "SND"
        command = "sudo arecord -D plughw:0,1 -r48000 -fs32_le -c2 -d1 -vvv"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
    else:
        # If none of the expected outputs are found
        print("Audio HDA/SOF/SND is not loaded, for HDA/SOF, please check on AIC connection and ensure BIOS settings is configured, for SND, please ensure .ri and .tplg is placed correctly and BIOS settings is configured properly.")

    # Check if "stream:Capture" is present in the log file
    log_file = "/home/user/record_32bits.log"
    with open(log_file, "a") as f:
        f.write(stdout.decode("utf-8", errors="ignore"))
        f.write(stderr.decode("utf-8", errors="ignore"))
    with open('/home/user/record_32bits.log') as f:
        if 'CAPTURE' in f.read():
            print("TEST PASS")
        else:
            print("TEST FAIL. Recording is failing might be due to 1) Change of -Dhw:x,x 2) Other playback process is still running. 3) Missing audio playback file in /home/user ")

def snd_script():
    print("----- Copying SND Script -----")
    os.system("cd /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio ; sudo cp -r sof-mtl.ri /lib/firmware/intel/sof-ipc4/mtl/")
    os.system("cd /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio ; sudo cp -r sof-mtl-rt711-2ch.tplg /lib/firmware/intel/sof-ace-tplg/")
    #print ("Sytem will reboot")
    #os.system("sudo reboot")
    #time.sleep(80)
    sys.exit(0)

def get_system_info():
    try:
        # Execute the dmidecode command
        result = subprocess.run(['sudo', 'dmidecode'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout

        # Parse the output for required information
        system_info = {
            "Product Name": None,
            "Serial Number": None,
            "SKU Number": None,
            "Base Board Product Name": None,
        }

        lines = output.split('\n')
        for i, line in enumerate(lines):
            if "System Information" in line:
                for j in range(i, i + 20):
                    if "Product Name:" in lines[j]:
                        system_info["Product Name"] = lines[j].split(":", 1)[1].strip()
                    if "Serial Number:" in lines[j]:
                        system_info["Serial Number"] = lines[j].split(":", 1)[1].strip()
                    if "SKU Number:" in lines[j]:
                        system_info["SKU Number"] = lines[j].split(":", 1)[1].strip()

            if "Base Board Information" in line:
                for j in range(i, i + 20):
                    if "Product Name:" in lines[j]:
                        system_info["Base Board Product Name"] = lines[j].split(":", 1)[1].strip()

        # Print the information
        print("System Information")
        print(f"\tProduct Name: {system_info['Product Name']}")
        print(f"\tSerial Number: {system_info['Serial Number']}")
        print(f"\tSKU Number: {system_info['SKU Number']}")
        print("\nBase Board Information")
        print(f"\tProduct Name: {system_info['Base Board Product Name']}")

    except Exception as e:
        print(f"An error occurred: {e}")

def ensure_audio_log_directory():
    log_dir = "/home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log"
    
    if not os.path.isdir(log_dir):
        try:
            os.makedirs(log_dir)
            print(f"Created directory: {log_dir}")
        except OSError as e:
            print(f"Error: {e.strerror}. Cannot create directory: {log_dir}")
            sys.exit(0)
    else:
        print("Audio_log directory exists... Execution continues...")

	
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

# Execute the function
    get_system_info()
    ensure_audio_log_directory()

    if args.c == "modules":
        audio_lib()
    elif args.c == "alsa":
        alsa_checker()
    elif args.c == "alsa_hdmi":
        onboard_hdmi_checker()
    elif args.b == "16" and args.s == "48":
        aplay()
    elif args.b == "32" and args.s == "48":
        aplay()
	
    elif args.b == "16" and args.s == "8":
        f_16bit_8k()
    elif args.b == "32" and args.s == "8":
        f_32bit_8k()
    elif args.b == "16" and args.s == "16":
        f_16bit_16k()
    elif args.b == "32" and args.s == "16":
        arecord()
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
    elif args.c == "arecord":
        arecord()
    elif args.c == "aplay_snd":
        aplay_snd()
    elif args.c == "arecord_snd":
        arecord_snd()
    elif args.c == "snd":
        snd()
    elif args.c == "lspci":
        lspci()
    elif args.c == "audio_lib":
        audio_lib()
    elif args.c == "rt5660_codec":
        rt5660_codec()
    elif args.c == "rt5660_modules":
        rt5660_modules()
    elif args.c == "rt5660_arecord":
        rt5660_arecord()
    elif args.c == "32bits_usb":
        snd_hda()
    elif args.c == "16bits_usb":
        snd_hda()
    elif args.c == "16bits_dp":
        audio_lib()
    elif args.c == "32bits_dp":
        snd_hda()
    elif args.c == "16bits_play":
        play_16bits()
    elif args.c == "16bits_record":
        record_16bits()
    elif args.c == "32bits_play":
        play_32bits()
    elif args.c == "32bits_record":
        record_32bits()	
    elif args.c == "snd_script":
        snd_script()
    else:
        print("Invalid parameters !! ")
        sys.exit(0)


main()
