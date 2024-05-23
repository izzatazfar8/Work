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

def driver_checker():
    print("----- IPU driver Checking -----")
    os.system("dmesg | grep ipu > /home/root/ipu.log")

    #verdict = false
    with open('/home/root/ipu.log') as f:
        if 'intel-ipu6 intel-ipu: enabling device' and 'intel-ipu6 intel-ipu: FW version' and 'intel-ipu6 intel-ipu: IPU driver' in f.read():
          print ("IPU Driver PASS")
        else:
          print ("IPU Driver FAILED")

def modules_checker():
    print("----- IPU Modules Checking -----")
    os.system("lsmod | grep ipu > /home/root/ipu_modules.log")

    #verdict = false
    with open('/home/root/ipu_modules.log') as f:
        if 'intel_ipu6_psys' and 'intel_ipu6_isys' and 'videobuf2_dma_contig' and 'videobuf2_v4l2' and 'videobuf2_common' and 'intel_ipu6' and 'ar0234' in f.read():
          print ("IPU Modules PASS")
        else:
          print ("IPU Modules FAILED")  
	 		 
def exposure():
    print("----- Exposure Checking -----")
    os.system("v4l2-ctl --all -d /dev/v4l-subdev5 > /home/root/exposure_check.log")

    #verdict = false
    with open('/home/root/exposure_check.log') as f:
        if 'exposure 0x00980911 (int)    : min=0 max=2355 step=2 default=2355 value=2355' in f.read():
          print ("Exposure PASS")
        else:
          print ("Exposure FAILED")	
def exposure_min_0():
    print("----- Exposure Checking -----")
    os.system("v4l2-ctl --all -d /dev/v4l-subdev5 > /home/root/exposure_check.log")

    #verdict = false
    with open('/home/root/exposure_check.log') as f:
        if 'exposure 0x00980911 (int)    : min=0' in f.read():
          print ("Exposure PASS")
        else:
          print ("Exposure FAILED")
def exposure_max_2355():
    print("----- Exposure Checking -----")
    os.system("v4l2-ctl --all -d /dev/v4l-subdev5 > /home/root/exposure_check.log")

    #verdict = false
    with open('/home/root/exposure_check.log') as f:
        if 'exposure 0x00980911 (int)    : min=0 max=2355' in f.read():
          print ("Exposure PASS")
        else:
          print ("Exposure FAILED")	

def exposure_def_2355():
    print("----- Exposure Checking -----")
    os.system("v4l2-ctl --all -d /dev/v4l-subdev5 > /home/root/exposure_check.log")

    #verdict = false
    with open('/home/root/exposure_check.log') as f:
        if 'exposure 0x00980911 (int)    : min=0 max=2355 step=2 default=2355' in f.read():
          print ("Exposure PASS")
        else:
          print ("Exposure FAILED")	
          
def exposure_val_2355():
    print("----- Exposure Checking -----")
    os.system("v4l2-ctl --all -d /dev/v4l-subdev5 > /home/root/exposure_check.log")

    #verdict = false
    with open('/home/root/exposure_check.log') as f:
        if 'exposure 0x00980911 (int)    : min=0 max=2355 step=2 default=2355 value=2355' in f.read():
          print ("Exposure PASS")
        else:
          print ("Exposure FAILED")	
def digital_gain():
    print("----- Digital Value Gain Checking -----")
    os.system("v4l2-ctl --all -d /dev/v4l-subdev5 > /home/root/digitalgain_check.log")

    #verdict = false
    with open('/home/root/digitalgain_check.log') as f:
        if 'digital_gain 0x009f0905 (int)    : min=0 max=2047 step=2 default=128 value=128' in f.read():
          print ("Digital Gain PASS")
        else:
          print ("Digital Gain FAILED")
def digital_gain_min_0():
    print("----- Digital Value Gain Checking -----")
    os.system("v4l2-ctl --all -d /dev/v4l-subdev5 > /home/root/digitalgain_check.log")

    #verdict = false
    with open('/home/root/digitalgain_check.log') as f:
        if 'digital_gain 0x009f0905 (int)    : min=0' in f.read():
          print ("Digital Gain PASS")
        else:
          print ("Digital Gain FAILED") 
          
def digital_gain_max_2047():
    print("----- Digital Value Gain Checking -----")
    os.system("v4l2-ctl --all -d /dev/v4l-subdev5 > /home/root/digitalgain_check.log")

    #verdict = false
    with open('/home/root/digitalgain_check.log') as f:
        if 'digital_gain 0x009f0905 (int)    : min=0 max=2047' in f.read():
          print ("Digital Gain PASS")
        else:
          print ("Digital Gain FAILED")
          
def digital_gain_def_128():
    print("----- Digital Value Gain Checking -----")
    os.system("v4l2-ctl --all -d /dev/v4l-subdev5 > /home/root/digitalgain_check.log")

    #verdict = false
    with open('/home/root/digitalgain_check.log') as f:
        if 'digital_gain 0x009f0905 (int)    : min=0 max=2047 step=2 default=128' in f.read():
          print ("Digital Gain PASS")
        else:
          print ("Digital Gain FAILED")
          
def digital_gain_val_128():
    print("----- Digital Value Gain Checking -----")
    os.system("v4l2-ctl --all -d /dev/v4l-subdev5 > /home/root/digitalgain_check.log")

    #verdict = false
    with open('/home/root/digitalgain_check.log') as f:
        if 'digital_gain 0x009f0905 (int)    : min=0 max=2047 step=2 default=128 value=128' in f.read():
          print ("Digital Gain PASS")
        else:
          print ("Digital Gain FAILED")
def analog_gain():
    print("----- Analog Gain Value Checking -----")
    os.system("v4l2-ctl --all -d /dev/v4l-subdev5 > /home/root/analoggain_check.log")

    #verdict = false
    with open('/home/root/analoggain_check.log') as f:
        if 'analogue_gain 0x009e0903 (int)    : min=0 max=127 step=2 default=14 value=14' in f.read():
          print ("Analog Gain PASS")
        else:
          print ("Analog Gain FAILED")
          
def analog_gain_min_0():
    print("----- Analog Gain Value Checking -----")
    os.system("v4l2-ctl --all -d /dev/v4l-subdev5 > /home/root/analoggain_check.log")

    #verdict = false
    with open('/home/root/analoggain_check.log') as f:
        if 'analogue_gain 0x009e0903 (int)    : min=0' in f.read():
          print ("Analog Gain PASS")
        else:
          print ("Analog Gain FAILED")
          
def analog_gain_max_127():
    print("----- Analog Gain Value Checking -----")
    os.system("v4l2-ctl --all -d /dev/v4l-subdev5 > /home/root/analoggain_check.log")

    #verdict = false
    with open('/home/root/analoggain_check.log') as f:
        if 'analogue_gain 0x009e0903 (int)    : min=0 max=127' in f.read():
          print ("Analog Gain PASS")
        else:
          print ("Analog Gain FAILED")
          
def analog_gain_def_14():
    print("----- Analog Gain Value Checking -----")
    os.system("v4l2-ctl --all -d /dev/v4l-subdev5 > /home/root/analoggain_check.log")

    #verdict = false
    with open('/home/root/analoggain_check.log') as f:
        if 'analogue_gain 0x009e0903 (int)    : min=0 max=127 step=2 default=14' in f.read():
          print ("Analog Gain PASS")
        else:
          print ("Analog Gain FAILED")
          
def analog_gain_val_14():
    print("----- Analog Gain Value Checking -----")
    os.system("v4l2-ctl --all -d /dev/v4l-subdev5 > /home/root/analoggain_check.log")

    #verdict = false
    with open('/home/root/analoggain_check.log') as f:
        if 'analogue_gain 0x009e0903 (int)    : min=0 max=127 step=2 default=14 value=14' in f.read():
          print ("Analog Gain PASS")
        else:
          print ("Analog Gain FAILED")
          
def check_binary():
    print("----- Binary loaded Checking -----")
    os.system("dmesg | grep ipu > /home/root/check_binary.log")

    #verdict = false
    with open('/home/root/check_binary.log') as f:
        if 'cpd file name: intel/ipu6ep_fw.bin' in f.read():
          print ("Binary Loaded PASS")
        else:
          print ("Binary Loaded FAILED")
          
def kernel_conf():
    print("----- Kernel Configuration Checking -----")
    os.system("zcat /proc/config.gz | grep CONFIG_VIDEO_INTEL_IPU_PDATA_DYNAMIC_LOADING > /home/root/kernel_conf.log")

    #verdict = false
    with open('/home/root/kernel_conf.log') as f:
        if '# CONFIG_VIDEO_INTEL_IPU_PDATA_DYNAMIC_LOADING is not set' in f.read():
          print ("Kernel Configuration PASS")
        else:
          print ("Kernel Configuration FAILED")
          
def dynamic_conf():
    print("----- Dynamic Configuration Checking -----")
    os.system("zcat /proc/config.gz | grep CONFIG_VIDEO_INTEL_IPU_PDATA_DYNAMIC_LOADING > /home/root/dynamic_conf.log")

    #verdict = false
    with open('/home/root/dynamic_conf.log') as f:
        if 'CONFIG_VIDEO_INTEL_IPU_PDATA_DYNAMIC_LOADING=y' in f.read():
          print ("Dynamic Configuration PASS")
        else:
          print ("Dynamic Configuration FAILED")

def single_fps():
    print("----- Single Camera FPS Checking -----")
    os.system("gst-launch-1.0 icamerasrc device-name=ar0234 num-buffers=500 printfps=true ! video/x-raw,format=NV12,width=1280,height=960 ! videoconvert ! glimagesink > /home/root/single_fps.log")

    #verdict = false
    with open('/home/root/single_fps.log') as f:
        if 'Average fps is:29' in f.read():
          print ("Single FPS PASS")
        else:
          print ("Single FPS FAILED")
def dual_fps():
    print("----- Single Camera FPS Checking -----")
    os.system("gst-launch-1.0 icamerasrc device-name=ar0234 num-buffers=500 printfps=true ! video/x-raw,format=NV12,width=1280,height=960 ! videoconvert ! glimagesink icamerasrc device-name=ar0234-2 num-buffers=500 printfps=true ! video/x-raw,format=NV12,width=1280,height=960 ! videoconvert ! glimagesink > /home/root/dual_fps.log")

    #verdict = false
    with open('/home/root/dual_fps.log') as f:
        if 'Average fps is:29' in f.read():
          print ("Dual FPS PASS")
        else:
          print ("Dual FPS FAILED")
def Pdata_dynamic_doc():
    print("----- Pdata dynamic doc Checking -----")
    #os.system("gst-launch-1.0 icamerasrc device-name=ar0234 num-buffers=500 printfps=true ! video/x-raw,format=NV12,width=1280,height=960 ! videoconvert ! glimagesink > /home/root/single_fps.log")

    #verdict = false
    with open('/home/root/ADL-P IPU6 SDK User Guide.docx') as f:
        if 'User also can get sensor platform data binary' in f.read():
          print ("Pdata dynamic doc Checking PASS")
        else:
          print ("Pdata dynamic doc Checking FAILED")
def Pdata_kernel_doc():
    print("----- Pdata Kernel Documentation Checking -----")
    #os.system("gst-launch-1.0 icamerasrc device-name=ar0234 num-buffers=500 printfps=true ! video/x-raw,format=NV12,width=1280,height=960 ! videoconvert ! glimagesink > /home/root/single_fps.log")

    #verdict = false
    with open('/home/root/ADL-P IPU6 SDK User Guide.docx') as f:
        if '2.4	Dynamic change sensor platform data' in f.read():
          print ("Pdata Kernel Documentation PASS")
        else:
          print ("Pdata Kernel Documentation FAILED")
def sensor_conf_doc():
    print("----- Sensor Configuration Document Checking -----")
    #os.system("gst-launch-1.0 icamerasrc device-name=ar0234 num-buffers=500 printfps=true ! video/x-raw,format=NV12,width=1280,height=960 ! videoconvert ! glimagesink icamerasrc device-name=ar0234-2 num-buffers=500 printfps=true ! video/x-raw,format=NV12,width=1280,height=960 ! videoconvert ! glimagesink > /home/root/dual_fps.log")

    #verdict = false
    #with open('/home/root/ADL-P IPU6 SDK User Guide.docx') as f:
    if os.path.isfile("/home/root/ADL-P IPU6 SDK User Guide.docx") == 0:
            print ("Sensor Configuration Document PASS")
    else :
        print ("Sensor Configuration Document FAILED")
        sys.exit(0)
def psys_conf_doc():
    print("----- Psys USB Document Checking -----")
    #os.system("gst-launch-1.0 icamerasrc device-name=ar0234 num-buffers=500 printfps=true ! video/x-raw,format=NV12,width=1280,height=960 ! videoconvert ! glimagesink icamerasrc device-name=ar0234-2 num-buffers=500 printfps=true ! video/x-raw,format=NV12,width=1280,height=960 ! videoconvert ! glimagesink > /home/root/dual_fps.log")

    #verdict = false
    #with open('/home/root/ADL-P IPU6 SDK User Guide.docx') as f:
    if os.path.isfile("/home/root/ADL-P IPU6 SDK User Guide.docx") == 0:
        print ("Psys USB Document PASS")
    else:
        print ("Psys USB Document FAILED")
        sys.exit(0)
def aptina1():
    print("----- aptina1 Checking -----")
    os.system("lsusb > /home/root/aptina1.log")

    #verdict = false
    with open('/home/root/aptina1.log') as f:
        if 'Bus 004 Device 006: ID 20fb:100e APTINA DEMO3' in f.read():
          print ("aptina1 PASS")
        else:
          print ("aptina1 FAILED")
def aptina2():
    print("----- aptina2 Checking -----")
    os.system("lsusb > /home/root/aptina2.log")

    #verdict = false
    with open('/home/root/aptina2.log') as f:
        if 'Bus 004 Device 005: ID 20fb:100e APTINA DEMO3' in f.read():
          print ("aptina2 PASS")
        else:
          print ("aptina2 FAILED")
def usb_app_exec():
    print("----- usb_app_exec Checking -----")
    os.system("./usb_camera_test -p 3 -f 5 -c 12  > /home/root/usb_app_exec.log")

    #verdict = false
    with open('/home/root/usb_app_exec.log') as f:
        if '[DBG]: Camera#2: Output frames#4 buffer dequeued.' in f.read():
          print ("usb_app_exec PASS")
        else:
          print ("usb_app_exec FAILED")  
def cam1_nv12():
    print("----- cam1_nv12 Checking -----")
    os.system("./usb_camera_test -p 3 -f 5 -c 1  > /home/root/cam1_nv12.log")

    #verdict = false
    with open('/home/root/cam1_nv12.log') as f:
        if '[DBG]: fileName ./cam1_stream0_frame0000_1280x960.NV12' in f.read():
          print ("cam1_nv12 PASS")
        else:
          print ("cam1_nv12 FAILED")
def cam2_nv12():
    print("----- cam2_nv12 Checking -----")
    os.system("./usb_camera_test -p 3 -f 5 -c 2  > /home/root/cam2_nv12.log")

    #verdict = false
    with open('/home/root/cam2_nv12.log') as f:
        if '[DBG]: fileName ./cam2_stream0_frame0000_1280x960.NV12' in f.read():
          print ("cam2_nv12 PASS")
        else:
          print ("cam2_nv12 FAILED")
def dual_nv12():
    print("----- dual_nv12 Checking -----")
    os.system("./usb_camera_test -p 3 -f 5 -c 12  > /home/root/dual_nv12.log")

    #verdict = false
    with open('/home/root/dual_nv12.log') as f:
        if '[DBG]: fileName ./cam1_stream0_frame0000_1280x960.NV12 [DBG]: fileName ./cam2_stream0_frame0000_1280x960.NV12' in f.read():
          print ("dual_nv12 PASS")
        else:
          print ("dual_nv12 FAILED")  
def usb1_active():
    print("----- usb1_active Checking -----")
    os.system("./usb_camera_test -p 3 -f 5 -c 1  > /home/root/usb1_active.log")

    #verdict = false
    with open('/home/root/usb1_active.log') as f:
        if '[INFO]: Camera#1: USB sensor input mode activated' in f.read():
          print ("usb1_active PASS")
        else:
          print ("usb1_active FAILED")
def usb2_active():
    print("----- usb2_active Checking -----")
    os.system("./usb_camera_test -p 3 -f 5 -c 2  > /home/root/usb2_active.log")

    #verdict = false
    with open('/home/root/usb2_active.log') as f:
        if '[INFO]: Camera#2: USB sensor input mode activated' in f.read():
          print ("usb2_active PASS")
        else:
          print ("usb2_active FAILED")  
def lib_check():
    print("----- lib_check Checking -----")
    if os.path.isfile("/home/root/usb_camera_test_tool/lib") == 0:
          print ("lib_check PASS")
    else:
          print ("lib_check FAILED")
def inc_check():
    print("----- inc_check Checking -----")
    if os.path.isfile("/home/root/usb_camera_test_tool/include") == 0:
          print ("inc_check PASS")
    else:
          print ("inc_check FAILED")  
def suffix_a():
    print("----- suffix_a Checking -----")
    os.system("cd /home/root/suffix_a_neg/")
    os.system("python3 sensor_pdata.py adl  > /home/root/suffix_a.log")

    #verdict = false
    with open('/home/root/suffix_a.log') as f:
        if 'Error: char format requires a bytes object of length 1' in f.read():
          print ("suffix_a PASS")
        else:
          print ("suffix_a FAILED")
def suffix_b():
    print("----- suffix_b Checking -----")
    os.system("cd /home/root/suffix_b_neg/")
    os.system("python3 sensor_pdata.py adl  > /home/root/suffix_b.log")

    #verdict = false
    with open('/home/root/suffix_b.log') as f:
        if 'Error: char format requires a bytes object of length 1' in f.read():
          print ("suffix_b PASS")
        else:
          print ("suffix_b FAILED") 
def slave_a():
    print("----- slave_a Checking -----")
    os.system("cd /home/root/slave_add_a_neg/")
    os.system("python3 sensor_pdata.py adl  > /home/root/slave_a.log")

    #verdict = false
    with open('/home/root/slave_a.log') as f:
        if 'Error' in f.read():
          print ("slave_a PASS")
        else:
          print ("slave_a FAILED") 
def slave_b():
    print("----- slave_b Checking -----")
    os.system("cd /home/root/slave_add_b_neg/")
    os.system("python3 sensor_pdata.py adl  > /home/root/slave_b.log")

    #verdict = false
    with open('/home/root/slave_b.log') as f:
        if 'Error' in f.read():
          print ("slave_b PASS")
        else:
          print ("slave_b FAILED")
def lane_a():
    print("----- lane_a Checking -----")
    os.system("cd /home/root/lane_a/")
    os.system("python3 sensor_pdata.py adl  > /home/root/lane_a.log")

    #verdict = false
    with open('/home/root/lane_a.log') as f:
        if 'Error' in f.read():
          print ("lane_a PASS")
        else:
          print ("lane_a FAILED")
def lane_b():
    print("----- lane_b Checking -----")
    os.system("cd /home/root/lane_b/")
    os.system("python3 sensor_pdata.py adl  > /home/root/lane_b.log")

    #verdict = false
    with open('/home/root/lane_b.log') as f:
        if 'Error' in f.read():
          print ("lane_b PASS")
        else:
          print ("lane_b FAILED")
def port_a():
    print("----- port_a Checking -----")
    os.system("cd /home/root/port_a/")
    os.system("python3 sensor_pdata.py adl  > /home/root/port_a.log")

    #verdict = false
    with open('/home/root/port_a.log') as f:
        if 'Error' in f.read():
          print ("port_a PASS")
        else:
          print ("port_a FAILED")
def port_b():
    print("----- port_b Checking -----")
    os.system("cd /home/root/port_b/")
    os.system("python3 sensor_pdata.py adl  > /home/root/port_b.log")

    #verdict = false
    with open('/home/root/port_b.log') as f:
        if 'Error' in f.read():
          print ("port_b PASS")
        else:
          print ("port_b FAILED")
def build2_kernel():
    print("----- build2_kernel Checking -----")
    os.system("dmesg | grep ipu  > /home/root/build2_kernel.log")

    #verdict = false
    with open('/home/root/build2_kernel.log') as f:
        if 'cpd file name: intel/ipu6ep_fw.bin' in f.read():
          print ("build2_kernel PASS")
        else:
          print ("build2_kernel FAILED")
def  build2_fw_bin():
    print("-----  build2_fw_bin Checking -----")
    os.system("dmesg | grep ipu  > /home/root/ build2_fw_bin.log")

    #verdict = false
    with open('/home/root/build2_fw_bin.log') as f:
        if 'cpd file name: intel/ipu6ep_fw.bin' in f.read():
          print (" build2_fw_bin PASS")
        else:
          print (" build2_fw_bin FAILED")
def build2_config():
    print("----- build2_config Checking -----")
    os.system("zcat /proc/config.gz | grep CONFIG_VIDEO_INTEL_IPU_PDATA_DYNAMIC_LOADING  > /home/root/build2_config.log")

    #verdict = false
    with open('/home/root/build2_config.log') as f:
        if 'CONFIG_VIDEO_INTEL_IPU_PDATA_DYNAMIC_LOADING=y' in f.read():
          print ("build2_config PASS")
        else:
          print ("build2_config FAILED")
def build2_0x10_pipe():
    print("----- build2_0x10_pipe Checking -----")
    os.system("gst-launch-1.0 icamerasrc device-name=ar0234 num-buffers=100 ! video/x-raw,format=NV12,width=1280,height=960 ! videoconvert ! xvimagesink icamerasrc device-name=ar0234-2 num-buffers=100 ! video/x-raw,format=NV12,width=1280,height=960 ! videoconvert ! xvimagesink  > /home/root/build2_0x10_pipe.log")

    #verdict = false
    with open('/home/root/build2_0x10_pipe.log') as f:
        if 'Registering meta implementation' in f.read():
          print ("build2_0x10_pipe PASS")
        else:
          print ("build2_0x10_pipe FAILED")
def sensor_conf_1():
    print("----- sensor_conf_1 Checking -----")
    os.system("dmesg | grep ar0234  > /home/root/sensor_conf_1.log")

    #verdict = false
    with open('/home/root/sensor_conf_1.log') as f:
        if 'stream off ar0234 a' in f.read():
          print ("sensor_conf_1 PASS")
        else:
          print ("sensor_conf_1 FAILED")
def sensor_conf_2():
    print("----- sensor_conf_2 Checking -----")
    os.system("dmesg | grep ar0234  > /home/root/sensor_conf_2.log")

    #verdict = false
    with open('/home/root/sensor_conf_2.log') as f:
        if 'stream off ar0234 b' in f.read():
          print ("sensor_conf_2 PASS")
        else:
          print ("sensor_conf_2 FAILED")
def subdev5():
    print("----- subdev5 Checking -----")
    os.system("v4l2-ctl --all -d /dev/v4l-subdev5  > /home/root/subdev5.log")

    #verdict = false
    with open('/home/root/subdev5.log') as f:
        if 'digital_gain' in f.read():
          print ("subdev5 PASS")
        else:
          print ("subdev5 FAILED")
def subdev5_output():
    print("----- subdev5_output Checking -----")
    os.system("v4l2-ctl --all -d /dev/v4l-subdev5  > /home/root/subdev5_output.log")

    #verdict = false
    with open('/home/root/subdev5_output.log') as f:
        if 'Cannot open device' in f.read():
          print ("subdev5_output FAILED")
        else:
          print ("subdev5_output PASS")
def mipi_1hour():
    print("----- mipi_1hour Checking -----")
    os.system("gst-launch-1.0 icamerasrc device-name=ar0234 num-buffers=6000 ! video/x-raw, format=NV12, width=1280, height=960 ! msdkvpp ! glimagesink icamerasrc device-name=ar0234-2 ! video/x-raw, format=NV12, width=1280, height=960 ! msdkvpp ! glimagesink  > /home/root/mipi_1hour.log")

    #verdict = false
    with open('/home/root/mipi_1hour.log') as f:
        if 'Execution ended after 1' in f.read():
          print ("mipi_1hour PASS")
        else:
          print ("mipi_1hour FAILED")
def usb_1hour():
    print("----- usb_1hour Checking -----")
    os.system("cd /home/root/icg_linux_ipu_sdk/usb_camera_test_tool")
    os.system("./usb_camera_test -p 3 -f 144000 -c 12  > /home/root/usb_1hour.log")

    #verdict = false
    with open('/home/root/usb_1hour.log') as f:
        if 'frames#144000 buffer dequeued' in f.read():
          print ("usb_1hour PASS")
        else:
          print ("usb_1hour FAILED")
def usb_24hour():
    print("----- usb_24hour Checking -----")
    os.system("cd /home/root/icg_linux_ipu_sdk/usb_camera_test_tool")
    os.system("./usb_camera_test -p 3 -f 3456000  -c 12  > /home/root/usb_24hour.log")

    #verdict = false
    with open('/home/root/usb_24hour.log') as f:
        if 'frames#3456000  buffer dequeued' in f.read():
          print ("usb_24hour PASS")
        else:
          print ("usb_24hour FAILED")
def mipi_24hour():
    print("----- mipi_24hour Checking -----")
    os.system("gst-launch-1.0 icamerasrc device-name=ar0234 num-buffers=144000 ! video/x-raw, format=NV12, width=1280, height=960 ! msdkvpp ! glimagesink icamerasrc device-name=ar0234-2 ! video/x-raw, format=NV12, width=1280, height=960 ! msdkvpp ! glimagesink  > /home/root/mipi_24hour.log")

    #verdict = false
    with open('/home/root/mipi_24hour.log') as f:
        if 'Execution ended after 24' in f.read():
          print ("mipi_24hour PASS")
        else:
          print ("mipi_24hour FAILED")
          
def main():
    print("----- IPU Module/Firmware Checking -----")
    script_name = str(sys.argv[0])
    usage = "python ipu_checker.py -c ipu_modules_checker"

    parser = argparse.ArgumentParser(prog=script_name,
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     description=usage)

    parser.add_argument('-c', metavar='--checker', help='driver/modules checker')


    args = parser.parse_args()

    print(sys.argv[0:])

    if args.c == "ipu_driver_checker":
        driver_checker()
    elif args.c == "ipu_modules_checker":
        modules_checker()
    elif args.c == "exposure":
        exposure()
    elif args.c == "digital_gain":
        digital_gain()
    elif args.c == "analog_gain":
        analog_gain()
    elif args.c == "check_binary":
        check_binary()
    elif args.c == "dynamic_conf":
        dynamic_conf()
    elif args.c == "kernel_conf":
        kernel_conf()   
    elif args.c == "single_fps":
        single_fps()
    elif args.c == "dual_fps":
        dual_fps()    
    elif args.c == "Pdata_dynamic_doc":
        Pdata_dynamic_doc()
    elif args.c == "Pdata_kernel_doc":
        Pdata_kernel_doc()
    elif args.c == "sensor_conf_doc":
        sensor_conf_doc()
    elif args.c == "psys_conf_doc":
        psys_conf_doc()    
    elif args.c == "exposure_min_0":
        exposure_min_0()
    elif args.c == "exposure_max_2355":
        exposure_max_2355()    
    elif args.c == "exposure_def_2355":
        exposure_def_2355()
    elif args.c == "exposure_val_2355":
        exposure_val_2355()
    elif args.c == "digital_gain_min_0":
        digital_gain_min_0()
    elif args.c == "digital_gain_max_2047":
        digital_gain_max_2047()    
    elif args.c == "digital_gain_def_128":
        digital_gain_def_128()
    elif args.c == "digital_gain_val_128":
        digital_gain_val_128()
    elif args.c == "analog_gain_min_0":
        analog_gain_min_0()
    elif args.c == "analog_gain_max_127":
        analog_gain_max_127()    
    elif args.c == "analog_gain_def_14":
        analog_gain_def_14()
    elif args.c == "analog_gain_val_14":
        analog_gain_val_14()
    elif args.c == "aptina1":
        aptina1()
    elif args.c == "aptina2":
        aptina2()
    elif args.c == "usb_app_exec":
        usb_app_exec()
    elif args.c == "cam1_nv12":
        cam1_nv12()
    elif args.c == "cam2_nv12":
        cam2_nv12()
    elif args.c == "dual_nv12":
        dual_nv12()
    elif args.c == "usb1_active":
        usb1_active()
    elif args.c == "usb2_active":
        usb2_active()
    elif args.c == "lib_check":
        lib_check()
    elif args.c == "inc_check":
        inc_check()
    elif args.c == "suffix_a":
        suffix_a()
    elif args.c == "suffix_b":
        suffix_b()
    elif args.c == "slave_a":
        slave_a()
    elif args.c == "slave_b":
        slave_b()
    elif args.c == "lane_a":
        lane_a()
    elif args.c == "lane_b":
        lane_b()
    elif args.c == "port_a":
        port_a()
    elif args.c == "port_b":
        port_b()
    elif args.c == "build2_kernel":
        build2_kernel()
    elif args.c == "build2_fw_bin":
        build2_fw_bin()
    elif args.c == "build2_config":
        build2_config()
    elif args.c == "build2_0x10_pipe":
        build2_0x10_pipe()
    elif args.c == "sensor_conf_1":
        sensor_conf_1()
    elif args.c == "sensor_conf_2":
        sensor_conf_2()
    elif args.c == "subdev5":
        subdev5()
    elif args.c == "subdev5_output":
        subdev5_output()
    elif args.c == "mipi_1hour":
        mipi_1hour()
    elif args.c == "usb_1hour":
        usb_1hour()
    elif args.c == "usb_24hour":
        usb_24hour()
    elif args.c == "mipi_24hour":
        mipi_24hour()
    else:
        print("Invalid parameters !! ")
        sys.exit(0)


main()
