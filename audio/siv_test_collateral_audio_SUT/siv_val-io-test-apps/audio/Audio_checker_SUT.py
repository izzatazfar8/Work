import os
import sys
import subprocess
import argparse
import time

LOG_DIR = "/home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log"

def execute_command(command, log_file=None):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if log_file:
        with open(log_file, "w") as f:
            f.write(result.stdout)
            f.write(result.stderr)
    return result.stdout, result.stderr

def sof_checker():
    print("----- SOF Checker -----")
    execute_command("dmesg | grep sof > /home/user/sof_checker.log")
    with open('/home/user/sof_checker.log') as f:
        if 'SoundWire enabled' in f.read():
            print("SOF Checker PASS")
        else:
            print("SOF Checker FAILED. Ensure SOF .ri and .tplg are in the correct path and SOF BIOS settings are configured")

def modules_filter():
    print("----- Second Step -----")
    with open("/home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/sut_check_lsmod.log", "r") as fil:
        data = fil.readlines()

    with open("/home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/f_sut_check_lsmod.log", "a") as fil2:
        for line in data:
            fil2.write(line.split()[0] + "\n")

def modules_checker():
    print("----- Modules Checking -----")
    os.system(f"rm -rf {LOG_DIR}/sut_check_lsmod.log; rm -rf {LOG_DIR}/f_sut_check_lsmod.log")
    if not os.path.isfile("/home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/check_onboard_module.log"):
        print("Check Module file is missing! Exiting ...")
        sys.exit(0)

    execute_command("lsmod | grep -i snd > /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/sut_check_lsmod.log")
    modules_filter()
    execute_command("grep -Ff /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/f_sut_check_lsmod.log /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/check_onboard_module.log > /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/module_compare.log")
    execute_command("diff /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/module_compare.log /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/check_onboard_module.log > /home/user/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/module_compare1.log")
    
    if os.stat(f"{LOG_DIR}/module_compare1.log").st_size == 0:
        print("Modules checker: PASS")
    else:
        print("Modules checker: FAIL")

def alsa_checker():
    print("----- ALSA Checker -----")
    execute_command("lsmod > /home/user/alsa_checker.log")
    with open('/home/user/alsa_checker.log') as f:
        if 'snd_hda' in f.read():
            print("ALSA Checker PASS")
        else:
            print("ALSA Checker FAILED. No audio found in 'lsmod' command.")

def onboard_hdmi_checker():
    print("----- ALSA HDMI Checking -----")
    if not os.path.isfile("/home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/check_onboard_hdmi_alsa.log"):
        print("Check HDMI ALSA file is missing! Exiting ...")
        sys.exit(0)

    execute_command("aplay -l > /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/sut_check_hdmi_alsa.log")
    execute_command("diff /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/sut_check_hdmi_alsa.log /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/check_onboard_hdmi_alsa.log > /home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_log/hdmi_alsa_compare1.log")

    if os.stat(f"{LOG_DIR}/hdmi_alsa_compare1.log").st_size == 0:
        print("ALSA HDMI checker: PASS")
    else:
        print("ALSA HDMI checker: FAIL")

def bitdepth_checker(bit_depth, sample_rate, file_suffix):
    print(f"----- {bit_depth}bits {sample_rate}kHz Bitdepth Checking -----")
    check_file = f"/home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/check_f_{bit_depth}bit_{sample_rate}k.log"
    if not os.path.isfile(check_file):
        print(f"Check bit depth file {check_file} is missing! Exiting ...")
        sys.exit(0)

    audio_file_dir = f"/home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/Audio_wav_files/2ch_{sample_rate}k_s{bit_depth}_le.wav"
    cmd_playback = f"aplay -vD hw:0,0 {audio_file_dir} 2> {LOG_DIR}/sut_check_f_{bit_depth}bit_{sample_rate}k.log"
    execute_command(cmd_playback)
    time.sleep(5)

    execute_command(f"diff {LOG_DIR}/sut_check_f_{bit_depth}bit_{sample_rate}k.log {check_file} > {LOG_DIR}/f_{bit_depth}bit_{sample_rate}k_compare1.log")

    if os.stat(f"{LOG_DIR}/f_{bit_depth}bit_{sample_rate}k_compare1.log").st_size == 0:
        print(f"Bitdepth checker: PASS for {bit_depth}bits {sample_rate}kHz")
    else:
        print(f"Bitdepth checker: FAIL for {bit_depth}bits {sample_rate}kHz")

def sof_16b():
    print("----- 16bits Bitdepth SOF Checking -----")
    check_file = "/home/siv_test_collateral_audio_SUT/siv_val-io-test-apps/audio/sof_debug_check_16b.log"
    if not os.path.isfile(check_file):
        print("Check bit depth file is missing! Exiting ...")
        sys.exit(0)

    audio_file_dir = "/home/AIC_HDA_HDMI_DP/16bits.wav"
    cmd_playback = f"aplay -d10 -vD hw:0,0 {audio_file_dir} 2> {LOG_DIR}/sut_check_sof_16b.log"
    execute_command(cmd_playback)
    time.sleep(5)

    execute_command(f"diff {LOG_DIR}/sut_check_sof_16b.log {check_file} > {LOG_DIR}/sof_16b_compare1.log")

    if os.stat(f"{LOG_DIR}/sof_16b_compare1.log").st_size == 0:
        print("Bitdepth checker: PASS for SOF 16bits")
    else:
        print("Bitdepth checker: FAIL for SOF 16bits")

def snd_hda():
    print("----- snd_hda Checking -----")
    execute_command("lsmod > /home/user/snd_hda.log")
    with open('/home/user/snd_hda.log') as f:
        if 'snd_hda' in f.read():
            print("snd_hda PASS")
        else:
            print("snd_hda FAILED. No audio found in 'lsmod' command.")

def ensure_audio_log_directory():
    if not os.path.isdir(LOG_DIR):
        try:
            os.makedirs(LOG_DIR)
            print(f"Created directory: {LOG_DIR}")
        except OSError as e:
            print(f"Error: {e.strerror}. Cannot create directory: {LOG_DIR}")
            sys.exit(0)
    else:
        print("Audio_log directory exists... Execution continues...")

def main():
    print("----- Audio Built In driver testing -----")
    script_name = str(sys.argv[0])
    usage = f"python {script_name} -c modules\npython {script_name} -b 16 -s 48"

    parser = argparse.ArgumentParser(prog=script_name, formatter_class=argparse.RawTextHelpFormatter, description=usage)
    parser.add_argument('-c', metavar='--checker', help='modules')
    parser.add_argument('-b', metavar='--checker', help='bit_depth')
    parser.add_argument('-s', metavar='--checker', help='sampling_rate')

    args = parser.parse_args()

    ensure_audio_log_directory()

    if args.c == "modules":
        modules_checker()
    elif args.c == "alsa":
        alsa_checker()
    elif args.c == "alsa_hdmi":
        onboard_hdmi_checker()
    elif args.c == "sof_16b":
        sof_16b()
    elif args.c == "snd_hda":
        snd_hda()
    elif args.b and args.s:
        bitdepth_checker(args.b, args.s, f"{args.b}bit_{args.s}k")
    else:
        print("Invalid parameters! Exiting ...")
        sys.exit(0)

if __name__ == "__main__":
    main()
