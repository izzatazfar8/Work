import os, re, sys, time, argparse, subprocess, time
from invoke import UnexpectedExit
import paramiko

script_name = str(sys.argv[0])
usage = "# python /home/THM/automation_script/IPU_checker_THM.py <IP> <option>"
parser = argparse.ArgumentParser(prog=script_name, description=usage)
parser.add_argument('-sut_ip', help='SUT IP')
parser.add_argument('-thm_ip', help='THM IP')
parser.add_argument('-op', help='Option = [streaming, driver_check]')

args = parser.parse_args()

target_user = 'root'
target_pass = ''

if args.sut_ip is not None:
    sut_ip = args.sut_ip
else:
    print ("-sut_ip missing")
    sys.exit(1)

if args.op is not None:
     option = args.op
else:
     print ("-op missing")
     sys.exit(1)

sut = paramiko.SSHClient()
sut.set_missing_host_key_policy(paramiko.AutoAddPolicy())
sut.connect(hostname=sut_ip,port=22,username=target_user,password=target_pass,allow_agent=False,look_for_keys=False)
# proc = subprocess.Popen(["prog", "arg"], stdout=subprocess.PIPE)
host,port = sut_ip,22
# transport = paramiko.Transport((host,port))
# username,password = "root",""
# transport.connect(None,username,password)
# sftp = paramiko.SFTPClient.from_transport(transport)

def main():

    if option == "ipu_driver_checker":
        stdin, stdout, stderr = sut.exec_command("python3 /home/root/ipu_checker.py -c ipu_driver_checker")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)

    elif option == "ipu_modules_checker":
        stdin, stdout, stderr = sut.exec_command("python3 /home/root/ipu_checker.py -c ipu_modules_checker")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
    
    elif option == "exposure":
        stdin, stdout, stderr = sut.exec_command("python3 /home/root/ipu_checker.py -c exposure")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
		
    elif option == "digital_gain":
        stdin, stdout, stderr = sut.exec_command("python3 /home/root/ipu_checker.py -c digital_gain")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
        
    elif option == "analog_gain":
        stdin, stdout, stderr = sut.exec_command("python3 /home/root/ipu_checker.py -c analog_gain")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
    
    elif option == "check_binary":
        stdin, stdout, stderr = sut.exec_command("python3 /home/root/ipu_checker.py -c check_binary")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)    
    elif option == "kernel_conf":
        stdin, stdout, stderr = sut.exec_command("python3 /home/root/ipu_checker.py -c kernel_conf")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
        
    elif option == "dynamic_conf":
        stdin, stdout, stderr = sut.exec_command("python3 /home/root/ipu_checker.py -c dynamic_conf")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
        
    elif option == "single_fps":
        stdin, stdout, stderr = sut.exec_command("python3 /home/root/ipu_checker.py -c single_fps")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)    
        
    elif option == "dual_fps":
        stdin, stdout, stderr = sut.exec_command("python3 /home/root/ipu_checker.py -c dual_fps")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)  
    elif option == "Pdata_dynamic_doc":
        stdin, stdout, stderr = sut.exec_command("python3 /home/root/ipu_checker.py -c Pdata_dynamic_doc")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
    elif option == "Pdata_kernel_doc":
        stdin, stdout, stderr = sut.exec_command("python3 /home/root/ipu_checker.py -c Pdata_kernel_doc")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
    elif option == "sensor_conf_doc":
        stdin, stdout, stderr = sut.exec_command("python3 /home/root/ipu_checker.py -c sensor_conf_doc")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)
    elif option == "ipu_modules_fw_checker":
        stdin, stdout, stderr = sut.exec_command("python3 /home/root/ipu_checker.py -c ipu_modules_fw_checker")
        print ("\nSUT executing " + option + " command...\n")
        time.sleep(3)
        output = stdout.readlines()
        sut.close()
        print ("\nSUT output:\n")
        print (output)
        sys.exit(0)

main()
