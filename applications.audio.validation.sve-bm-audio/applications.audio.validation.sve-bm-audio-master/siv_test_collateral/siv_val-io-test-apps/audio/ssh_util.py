import os, sys, subprocess, time, socket, re

class ssh_com(object):
	def __init__(self, ip, user='root'):
		self.ret_ip = ip
		self.user = user
		self.reset_known_host()
	
	def setpub(self,sshpass="",verbose=False):
		if self.user == "root":
			key_dir = "/root/"
		else:
			key_dir = "/home/" + self.user + "/"
			
		if not os.path.exists(key_dir + ".ssh/id_rsa"):
			self.local_exec("ssh-keygen -f " + key_dir + ".ssh/id_rsa -q -N ''")
		if sshpass:
			self.ssh_exec("mkdir ~/.ssh",sshpass=sshpass,verbose=False)
			self.local_exec("sshpass -p " + sshpass + " scp -o StrictHostKeyChecking=no -C  ~/.ssh/id_rsa.pub "+ self.user +"@" + self.ret_ip + ":~/.ssh/authorized_keys")
		else:
			self.ssh_exec("mkdir ~/.ssh", verbose=False)
			self.local_exec("scp -o StrictHostKeyChecking=no -C ~/.ssh/id_rsa.pub "+ self.user +"@" + self.ret_ip + ":~/.ssh/authorized_keys",status_code=True)
	
	def ssh_exec(self,cmd,timer=0,log=False,backgrd=False,verbose=True,sshpass=None,non_blk=False,status_code=None):
	# Execute command at remote machine with SSH protocol
		ret_ip = self.ret_ip
		time.sleep(float(timer))
		if backgrd:
			if verbose:
				sys.stdout.write("ssh_exec(bckgrd): " + cmd + " (" + str(ret_ip) + ")\n")
				if sshpass:
					ssh = subprocess.Popen("sshpass -p " + sshpass + " ssh -o StrictHostKeyChecking=no -f "+ self.user +"@" + str(ret_ip) + " '" + cmd + "' 2>&1",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
					sys.stdout.write("sshpass -p " + sshpass + " ssh -o StrictHostKeyChecking=no -f "+ self.user +"@" + str(ret_ip) + " '" + cmd + "' 2>&1")
					ssh = subprocess.Popen("sshpass -p " + sshpass + " ssh -o StrictHostKeyChecking=no -f "+ self.user +"@" + str(ret_ip) + " '" + cmd + "' 2>&1",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
				else:
					sys.stdout.write("ssh -o StrictHostKeyChecking=no -f "+ self.user +"@" + str(ret_ip) + " '" + cmd + "' 2>&1")
					ssh = subprocess.Popen("ssh -o StrictHostKeyChecking=no -f "+ self.user +"@" + str(ret_ip) + " '" + cmd + "' 2>&1",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
				return
		else:
			if verbose:
				sys.stdout.write("ssh_exec: " + cmd + " (" + str(ret_ip) + ")\n")
			if sshpass:
				ssh = subprocess.Popen("sshpass -p " + sshpass + " ssh -o StrictHostKeyChecking=no "+ self.user +"@" + str(ret_ip) + " '" + cmd + "' 2>&1",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
			else:
				ssh = subprocess.Popen('ssh ' + self.user + '@' + str(ret_ip) + ' "' + cmd + '" 2>&1', shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		if non_blk:
			fd = ssh.stdout.fileno()
			fl = fcntl.fcntl(fd, fcntl.F_GETFL)
			fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
		try:
			output = ssh.stdout.readlines()
		except IOError:
			output = ""
		
		output = [i.strip() for i in output]
		output = "".join(output)
		return output
	def local_exec(self,cmd,timer=0,log=False,backgrd=False,verbose=False,status_code=None):
		# Execute command locally
		time.sleep(float(timer))
		if backgrd:
			if verbose:
				sys.stdout.write("local_exec(bckgrd): " + cmd + "\n")
				local = subprocess.Popen(cmd + " & 2>&1",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
			return
		else:
			if verbose:
				sys.stdout.write("local_exec: " + cmd + " \n")
			local = subprocess.Popen(cmd + " 2>&1",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		
		output = local.stdout.readlines()
		output = [i.strip() for i in output]
		output = ",".join(output)
		if log:
			with open("/local_exec.log","a+") as f:
				f.write(str(datetime.datetime.now()) + "\n")
				f.write("Executed Command >>> " + cmd + "\n")
				f.write("Output Logged >>> " + output + "\n")
		if status_code:
			 return local.wait()
		return output
	
	def reset_known_host(self):
		# Reset the known_hosts value of the system
		if self.user == "root":
			key_dir = "/root/"
		else:
			key_dir = "/home/" + self.user + "/"
		self.local_exec("ssh-keygen -q -f '" + key_dir + ".ssh/known_hosts' -R " + self.ret_ip)
		# print "ssh-keygen -f '" + key_dir + ".ssh/known_hosts' -R " + self.ret_ip
		# status = os.system("ssh-keygen -q -f '" + key_dir + ".ssh/known_hosts' -R " + self.ret_ip)
		# status = os.system("ssh-keygen -R " + self.ret_ip)
		# if int(status) > 0:
		# 	print "Failed to reset known_hosts value of the system"
	
	def chk_con(self,exit=False,timeout=1000):
		# Check ssh connectivity to remote machine
		print "\n================================ Check IP Status =========================================="
		print "Ping ALIVE now : " + self.ret_ip
		pingresult = 5
		i = 0
		while 1:
			con = socket.socket()
			con.settimeout(0.25)
			try:
				con.connect((self.ret_ip,int(22)))
				# con.close()
			except socket.error:
				i += 1
				time.sleep(1)
			else:
				con.close()
				pingresult = 1
				break
			if i == int(timeout):
				pingresult = 0
				break
		if pingresult == 1:
			print "Connection for " + self.ret_ip + " is alive"
			print "===========================================================================================\n"
			return True
		elif pingresult == 0:
			print "Connection for " + self.ret_ip + " timeout"
			print "===========================================================================================\n"
			return False
	
	def get_disk_id(self, disk_id):
		multiple_splitter = re.compile("->|../|-|.hddimg")
		get_id_command = "ls -l /dev/disk/by-id | grep -i " + str(disk_id) + " | grep -v part"
		device_label_wo_dev = str(multiple_splitter.split(self.ssh_exec(get_id_command, verbose=False))[-1])
		device_label = "/dev/" + device_label_wo_dev
		
		if device_label_wo_dev == "":
			print "Device not found. Proceed to exit."
			sys.exit(1)
		
		return device_label
