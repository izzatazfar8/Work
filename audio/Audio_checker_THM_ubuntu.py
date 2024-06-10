import os
import sys
import time
import argparse
import paramiko

destPath = "/home/test/siv_test_collateral/siv_val-io-test-apps/audio"
file_to_check = "/home/Audio_checker.py"
script_name = str(sys.argv[0])
usage = "# python /home/THM/automation_script/Audio_checker_THM.py <IP> <option>"
pvtkey = '/home/adlp3/.ssh/id_rsa'

parser = argparse.ArgumentParser(prog=script_name, description=usage)
parser.add_argument('-sut_ip', help='SUT IP')
parser.add_argument('-sut_user', help='SUT User')
parser.add_argument('-sut_pass', help='SUT Password')
parser.add_argument('-os', help='OS')
parser.add_argument('-thm_ip', help='THM IP')
parser.add_argument('-op', help='Option = [playback, driver_check]')
parser.add_argument('-drv', help='Driver = [HDA, SOF]')
parser.add_argument('-bitdepth', help='bitdepth = [8bits, 16bits, 24bits, 32bits]')
parser.add_argument('-khz', help='rate = [8, 16, 48]')
parser.add_argument('-ch', help='channel = [2, 4, 8]')
parser.add_argument('-codec', help='codec = [hda, sof, snd]')
parser.add_argument('-pvt', help='Pvt-key at your THM: ex: /home/adlp3/rsa_pvt')
args = parser.parse_args()

def scp_files(username, password, ip_address):
    command = f"cd /home/applications.audio.validation.sve-bm-audio/ && sudo sshpass -p '{password}' scp -o StrictHostKeyChecking=no -rv siv_test_collateral/siv_val-io-test-apps/audio/siv_test_collateral_audio_SUT/ {username}@{ip_address}:/home/user"
    return os.system(command)

if args.sut_user and args.sut_pass and args.sut_ip:
    result = scp_files(args.sut_user, args.sut_pass, args.sut_ip)
    print(result)
else:
    print("Please provide username (-sut_user), password (-sut_pass), and IP address (-sut_ip).")
    sys.exit(1)

if not args.sut_ip:
    print("-sut_ip missing")
    sys.exit(1)

if not args.op:
    print("-op missing")
    sys.exit(1)

sut = paramiko.SSHClient()
sut.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    if args.pvt:
        pvtkey = args.pvt
        sut.connect(hostname=args.sut_ip, username=args.sut_user, key_filename=pvtkey)
        print("SSH key-authentication established successfully.")
    else:
        sut.connect(hostname=args.sut_ip, port=22, username=args.sut_user, password=args.sut_pass, allow_agent=False, look_for_keys=False)
        print("SSH password authentication established successfully.")
except paramiko.SSHException as e:
    print(f"SSH connection error: {e}")
    sys.exit(1)

def get_product_name(sut):
    command = "sudo dmidecode"
    stdin, stdout, stderr = sut.exec_command(command)
    
    output = stdout.read().decode()
    error = stderr.read().decode()
    
    if stderr.channel.recv_exit_status() != 0:
        print(f"Error: {error.strip()}")
        return None
    
    for line in output.splitlines():
        if "Product Name" in line:
            return line.split(":")[1].strip()
    
    return None

def check_codec_loaded(sut, codec):
    command = "aplay -l"
    stdin, stdout, stderr = sut.exec_command(command)
    output = stdout.read().decode()
    
    if codec in output:
        if codec == "SOF":
            print("SOF is loaded")
        elif codec == "SND":
            print("Soundwire/SND is loaded")
        return True
    return False

def fwtplg(codec):
    product_name = get_product_name(sut)
    if not product_name:
        print("Failed to get product name")
        return

    print(f"Product Name: {product_name}")
    print(f"Codec: {codec}")

    success = False
    commands = []

    if product_name in ["Meteor Lake Client Platform"]:
        if codec == "SOF":
            commands = [
                "sudo cp -r /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/fwtplg/MTL/SOF/sof-mtl.ri /lib/firmware/intel/sof-ipc4/mtl/",
                "sudo cp -r /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/fwtplg/MTL/SOF/sof-hda-generic.tplg /lib/firmware/intel/sof-ace-tplg/"
            ]
        elif codec == "SND":
            commands = [
                "sudo cp -r /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/fwtplg/MTL/SND/sof-mtl.ri /lib/firmware/intel/sof-ipc4/mtl/",
                "sudo cp -r /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/fwtplg/MTL/SND/sof-mtl-rt711.tplg /lib/firmware/intel/sof-ace-tplg/"
            ]
    if product_name in ["Arrow Lake Client Platform"]:
        if codec == "SOF":
            commands = [
                "sudo cp -r /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/fwtplg/ARL/SOF/sof-arl-s.ri /lib/firmware/intel/sof-ipc4/arl-s/",
                "sudo cp -r /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/fwtplg/ARL/SOF/sof-hda-generic.tplg /lib/firmware/intel/sof-ace-tplg/"
            ]
        elif codec == "SND":
            commands = [
                "sudo cp -r /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/fwtplg/ARL/SND/sof-arl-s.ri /lib/firmware/intel/sof-ipc4/arl/",
                "sudo cp -r /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/fwtplg/ARL/SND/sof-arl-rt711-l0-4ch.tplg /lib/firmware/intel/sof-ace-tplg/"
            ]
    if product_name in ["Raptor Lake Client Platform"]:
        if codec == "SOF":
            commands = [
                "sudo cp -r /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/fwtplg/RPL/SOF/sof-arl-s.ri /lib/firmware/intel/sof",
                "sudo cp -r /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/fwtplg/RPL/SOF/sof-hda-generic-1ch.tplg /lib/firmware/intel/sof-tplg/"
            ]
        elif codec == "SND":
            commands = [
                "sudo cp -r /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/fwtplg/RPL/SND/sof-rpl.ri /lib/firmware/intel/sof",
                "sudo cp -r /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/fwtplg/RPL/SND/sof-adl-rt711.tplg /lib/firmware/intel/sof-tplg/"
            ]

    if product_name in ["Alder Lake Client Platform"]:
        if codec == "SOF":
            commands = [
                "sudo cp -r /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/fwtplg/ADL/SOF/sof-adl_n.ri /lib/firmware/intel/sof",
                "sudo cp -r /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/fwtplg/ADL/SOF/sof-hda-generic.tplg /lib/firmware/intel/sof-tplg/"
            ]
        elif codec == "SND":
            commands = [
                "sudo cp -r /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/fwtplg/ADL/SND/sof-adl_n.ri /lib/firmware/intel/sof",
                "sudo cp -r /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/fwtplg/ADL/SND/sof-adl-rt711.tplg /lib/firmware/intel/sof-tplg/"
            ]

    # Add other product name and codec combinations as needed

    if not commands:
        print("Unsupported product name or codec")
    else:
        for command in commands:
            stdin, stdout, stderr = sut.exec_command(command)
        success = True

    if success:
        print("Files copied successfully")
        reboot_system()

def reboot_system():
    stdin, stdout, stderr = sut.exec_command("sudo reboot")
    time.sleep(100)  # Wait for the system to reboot

    while True:
        try:
            sut.connect(hostname=args.sut_ip, port=22, username=args.sut_user, password=args.sut_pass, allow_agent=False, look_for_keys=False)
            print("System is alive")
            break
        except (paramiko.ssh_exception.NoValidConnectionsError, paramiko.ssh_exception.SSHException):
            time.sleep(10)

def main():
    if not check_codec_loaded(sut, args.codec):
        fwtplg(args.codec)  # Call the fwtplg function if codec is not loaded

    commands = {
        "snd_script": "sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c snd_script",
        "modules_checker": "sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c modules",
        "alsa_checker": "sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c alsa",
        "sof_checker": "sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c sof",
        "16bits": "sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -b 16 -s 48",
        "32bits": "sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -b 32 -s 48",
        "32bits_8k": "sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -b 32 -s 8",
        "16bits_sof": "sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c sof_16b",
        "snd_hda": "sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c snd_hda",
        "hdaudioC0D0": "sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c hdaudioC0D0",
        "mic_jack": "sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c mic_jack",
        "playback_switch": "sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c playback_switch",
        "capture_switch": "sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c capture_switch",
        "aplay": "sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c aplay",
        "arecord": "sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c arecord",
        "aplay_snd": "sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c aplay_snd",
        "arecord_snd": "sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c arecord_snd",
        "snd": "sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c snd",
        "lspci": "sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c lspci",
        "audio_lib": "sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c audio_lib",
        "playback": f"sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/new_audio_SUT_checker.py -op {args.op} -drv {args.drv} -b {args.bitdepth} -s {args.khz} -ch {args.ch}",
        "rt5660_codec": "sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c rt5660_codec",
        "rt5660_arecord": "sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c rt5660_arecord",
        "rt5660_modules": "sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c rt5660_modules",
        "usb_16bits": "sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c 16bits_usb",
        "usb_32bits": "sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c 32bits_usb",
        "dp_16bits": "sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c 16bits_dp",
        "dp_32bits": "sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c 32bits_dp",
        "play_16bits": "sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c 16bits_play",
        "record_16bits": "sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c 16bits_record",
        "play_32bits": "sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c 32bits_play",
        "record_32bits": "sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c 32bits_record",
        "play_16bits_sof": "sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c 16bits_play_sof",
        "record_16bits_sof": "sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c 16bits_record_sof",
        "play_32bits_sof": "sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c 32bits_play_sof",
        "record_32bits_sof": "sudo python3 /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_checker_SUT_ubuntu.py -c 32bits_record_sof",
    }

    command = commands.get(args.op)
    if command:
        stdin, stdout, stderr = sut.exec_command(command)
        print(f"\nSUT executing {args.op} command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print("\nSUT output:\n")
        print(output)
    else:
        print(f"Unsupported operation: {args.op}")

main()
