"""
GenericCommandServer.py
Version 3.0
(GCVS3)

<Date>      <Owner>          <Version>     <Changes>
2009        Raniero             1.0        Initial release
8/2/2011      CKH               2.0        Auto-establish Log Folder
                                           Auto-find IP
                                           Allow rapid connection/disconnection (pingalive & pingdead)
                                           Capable of time-execute with logging capabilities (XTP-lock & no lock)
18/3/2011     CKH               3.0        Auto-establish Scripting Folder
                                           Capable of self-autosetup autostart function
                                           Shell command enabled in Timeexecute
                                           Capable of scripting a file with any extension
                                           Capable of scripting client server for file transfers
                                           Capable of erasing its own traces under GC commands
                                           Capable of refresh itself for new test-run
                                           Capable of trace any file/dir in DUT machine
                                           Capable of self-deploy with only designated port
                                           Capable of deleting a folder's contents
                                           Transfromed into module-independent architecture [All-in-one server script]
17/4/2012       GKA             3.2        Fix the time execute that could not accept command with double quotes. E.g get_cp_memory_cpu = "top -bc -n 10 | grep -w 'init' | grep -v 'grep' | awk '{print \"copy,\" $9 \",\" $10}' >> " +  performancelog
                                           dut.timeexecute(get_cp_memory_cpu)

"""
#Configure the designated port belows
#-------------------------------------------------------------------------
port = "2300"

#-------------------------------------------------------------------------
##########################################################################
#       If possible, paste GenericCommand in the following folders:	 #
#	  Windows= c:/							 #
#	  Linux	 = /							 #
#									 #
##########################################################################



##########################################################################
#       Don't Touch BELOW unless you're further upgrading the server. 	 #
#        		     Merci Beaucoup!                       	 #
#			      Version 3.0                   		 #
#									 #
##########################################################################
#-------------------------------------------------------------------------
#Pre-Setup
IntelPGDNSServer = '10.248.2.1'
IntelPGDNSServerPort = 80
#-------------------------------------------------------------------------
import os
import shutil
import SimpleXMLRPCServer
import socket
import subprocess
import time
import sys


if sys.platform[0:2] is not "Win":
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect((IntelPGDNSServer, IntelPGDNSServerPort))
	ipadd = s.getsockname()[0]
	s.close()
	del s
else:
	ipadd = socket.gethostbyname(socket.gethostname())


class GCV3(object):
        def __init__(self):
                #OS Nature Variables
                self.win_python_location = r"c:\Python27\python.exe"
                self.GCSV3_def_location = r"/usr/local/gv/GenericCommand/GenericCommandServer.py"
                self.GCSV3_windef_location = r"c:\gv\GenericCommand\GenericCommandServer.py"
                self.GCSV3_auto_location = r"/root/.config/autostart/GCSV3.desktop"
                if str(sys.platform[0:3]).upper() == "WIN":
                        self.GCSV3_winauto_location = os.environ['USERPROFILE'] + r"\Start Menu\Programs\Startup\GCSV3.bat"

                #Default Values. [Don't touch if possible]
                self.dirpath=r"/GENERICDAEMON"
                self.windirpath=r"c:/GENERICDAEMON"
                self.logpath=r"%s/TestLog/" % self.dirpath
                self.winlogpath=r"%s/TestLog/" % self.windirpath
                self.scptpath=r"%s/TempScript/"% self.dirpath
                self.winscptpath=r"%s/TempScript/" % self.windirpath
                self.start_flag = 1
                self.logextension = ".txt"
                self.pyscptextension = ".py"
                self.logactionbarrier = """
===========================================================================================

"""
                self.TxscriptPID= None
                self.self_start()

#Auto-Start Functions
        def platformcheck(self):
                if str(sys.platform[0:3]).upper() == "LIN":
                        self.current_platform = "LINUX"
                        return "LINUX"
                elif str(sys.platform[0:3]).upper() == "WIN":
                        self.current_platform = "WINDOWS"
                        return "WINDOWS"
                else:
                        self.current_platform = "UNKNOWN"
                        return "UNKNOWN"


        def dircheck(self, directory_path):
                if os.access(str(directory_path), os.F_OK) == True and os.access(str(directory_path), os.R_OK) == True and os.access(str(directory_path), os.W_OK) == True and os.access(str(directory_path), os.X_OK) == True:
                                return "Directory Exists"
                else:		
                        while 1:
                                try:
                                        os.mkdir(str(directory_path))
                                except:
                                        try:
                                                shutil.rmtree(str(directory_path))
                                        except:
                                                pass
                                        os.mkdir(str(directory_path))
                                        break
                                if os.access(str(directory_path), os.F_OK) == True and os.access(str(directory_path), os.R_OK) == True and os.access(str(directory_path), os.W_OK) == True and os.access(str(directory_path), os.X_OK) == True:
                                        return "Directory Exists"
                                else:
                                        return "Creation ERROR"


        def startup_setup(self):
                if str(sys.platform[0:3]).upper() == "LIN":
                        if self.file_tracer(self.GCSV3_def_location)[:13] == "target exists" or self.file_tracer(self.GCSV3_def_location)[:13] == "target exists":                                
                                if self.file_tracer(self.GCSV3_auto_location)[:13] == "target exists":
                                        return "Startup Setup Success"
                                else:
                                        try:
                                                filecontent="""[Desktop Entry]
Type=Application
Exec=python %s
Hidden=false
X-GNOME-Autostart-enabled=true
Name[en_US]=GenericCommandServer start
Name=GenericCommandServer start
Comment[en_US]=
Comment=""" % (self.GCSV3_def_location)
                                                self.dircheck(self.GCSV3_auto_location[:self.GCSV3_auto_location.rfind("/")])
                                                self.file_scripter(filecontent, self.GCSV3_auto_location[:self.GCSV3_auto_location.rfind("/")], self.GCSV3_auto_location[self.GCSV3_auto_location.rfind("/")+1:])
                                                del filecontent
                                                return "Startup Setup Success"
                                        except:
                                                try:
                                                        del filecontent
                                                except:
                                                        pass
                                                return "Startup Setup Failed"
                        else:
                                return "Manual"
                        
                elif str(sys.platform[0:3]).upper() == "WIN":
                        if self.file_tracer(self.GCSV3_windef_location)[:13] == "target exists" or self.file_tracer(os.environ['USERPROFILE'] + r"\Start Menu\Programs\Startup\GenericCommandServer.py")[:13] == "target exists":      
                                if self.file_tracer(self.GCSV3_winauto_location)[:13] == "target exists" or self.file_tracer(os.environ['USERPROFILE'] + r"\Start Menu\Programs\Startup\GenericCommandServer.py")[:13] == "target exists":
                                        return "Startup Setup Success"
                                else:
                                        try:
                                                filecontent = "@echo off\n%s %s" % (self.win_python_location, self.GCSV3_windef_location)
                                                self.file_scripter(filecontent, self.GCSV3_winauto_location[:self.GCSV3_winauto_location.rfind("\\")],  self.GCSV3_winauto_location[self.GCSV3_winauto_location.rfind("\\")+1:])
                                                del filecontent
                                                return "Startup Setup Success"
                                        except:
                                                try:
                                                        del filecontent
                                                except:
                                                        pass
                                                return "Startup Setup Failed"
                        else:
                                return "Manual"
                else:
                        return "UNKNOWN OS"          

        def removal_setup(self):
                if str(sys.platform[0:3]).upper() == "LIN":
                        print "Remote Self-Removal Triggered. Removing GCSV3 traces...."
                        try:
                                self.masterdelete(self.logpath)
                                self.masterdelete(self.scptpath)
                                self.masterdelete(self.dirpath)
                                shutil.rmtree(self.dirpath)
                                if self.file_tracer(self.GCSV3_auto_location)[:13] == "target exists":
                                        try:
                                                os.unlink(self.GCSV3_auto_location)
                                        except:
                                                pass
                                
                                print "Function Ended. GCSV3 no longer in service."
                                print "Thanks you. Goodbye"
                                return "GCSV3 no longer in service. Thanks you. Goodbye"
                        except:
                                return "GCSV3 Removal Incomplete."
                        
                elif str(sys.platform[0:3]).upper() == "WIN":
                        print "Remote Self-Removal Triggered. Removing GCSV3 traces...."
                        try:
                                self.masterdelete(self.winlogpath)
                                self.masterdelete(self.winscptpath)
                                self.masterdelete(self.windirpath)
                                shutil.rmtree(self.windirpath)
                                if self.file_tracer(self.GCSV3_winauto_location)[:13] == "target exists":
                                        try:
                                                os.unlink(self.GCSV3_winauto_location)
                                        except:
                                                pass
                                
                                print "Goodbye"
                                print "Thanks you. Goodbye"
                                return "GCSV3 no longer in service. Thanks you. Goodbye"
                        except:
                                return "GCSV3 Removal Incomplete."
                else:
                        self.current_platform = "UNKNOWN OS"
                        return "UNKNOWN OS"

        def test_start(self):
                if str(sys.platform[0:3]).upper() == "LIN":
                        try:
                                self.masterdelete(self.logpath)
                                self.masterdelete(self.scptpath)
                                return "DUT is ready for new test"
                        except:
                                return "Flush Failed"
                        
                elif str(sys.platform[0:3]).upper() == "WIN":
                        try:
                                self.masterdelete(self.winlogpath)
                                self.masterdelete(self.scptpath)
                                return "DUT is ready for new test"
                        except:
                                return "Flush Failed"
                else:
                        self.current_platform = "UNKNOWN OS"
                        return "UNKNOWN OS"                

        def self_start(self):
                if self.platformcheck() == "LINUX":
                        print "Platform                   :    [ LINUX ]"
                        #Checking GCV3 Directory
                        if self.dircheck(str(self.dirpath)) == "Directory Exists":
                                self.start_flag = 2
                                print "GCSV3 MAIN directory       :    [ READY ]"

                                #Checking Log Directory
                                if self.dircheck(str(self.logpath)) == "Directory Exists":
                                        self.start_flag = 2
                                        print "GCSV3 LOG directory        :    [ READY ]"

                                        #Checking Script Directory
                                        if self.dircheck(str(self.scptpath)) == "Directory Exists":
                                                self.start_flag = 3
                                                print "GCSV3 SCRIPT directory     :    [ READY ]"

                                                #Auto-Startup Setup
                                                if self.startup_setup() == "Startup Setup Success":
                                                        print "GCSV3 Autostartup          :    [  OK  ]"
                                                elif self.startup_setup() == "Maunal":
                                                        print "GCSV3 Autostartup          :    [  N/A  ]"
                                                        print "         - Maunal Autostartup setup is required."
                                                else:
                                                        print "GCSV3 Autostartup          :    [ FAILED ]"
                                                        print "         - Maunal Autostartup setup is required."
                                                        
                                                print "GCSV3                      :    [ READY ]"
                                                print "-------------------------"                                                      

                                                
                                        elif self.dircheck(str(self.scptpath)) == "Creation ERROR":
                                                self.start_flag = 1
                                                print "%s directory creation error." % str(self.scptpath)
                                                print "WARNING: GCSV3 Will Not Function Properly."
                                        else:
                                                self.start_flag = 1
                                                print "%s directory Missing and unable to create." % str(self.scptpath)
                                                print "WARNING: GCSV3 Will Not Function Properly."
                                
                                elif self.dircheck(str(self.logpath)) == "Creation ERROR":
                                        self.start_flag = 1
                                        print "%s directory creation error." % str(self.filepath)
                                        print "WARNING: GCSV3 Will Not Function Properly."
                                else:
                                        self.start_flag = 1
                                        print "%s directory Missing and unable to create." % str(self.filepath)
                                        print "WARNING: GCSV3 Will Not Function Properly."
                        
                        elif self.dircheck(str(self.dirpath)) == "Creation ERROR":
                                self.start_flag = 1
                                print "%s directory creation error." % str(self.dirpath)
                                print "WARNING: GCSV3 Will Not Function Properly."
                        else:
                                self.start_flag = 1
                                print "%s directory Missing and unable to create." % str(self.dirpath)
                                print "WARNING: GCSV3 Will Not Function Properly."


                elif self.platformcheck() == "WINDOWS":
                        print "Platform                   :    [ WINDOWS ]"

                        #Checking GCV3 Directory
                        if self.dircheck(str(self.windirpath)) == "Directory Exists":
                                self.start_flag = 2
                                print "GCSV3 MAIN directory       :    [ READY ]"

                                #Checking Log Directory
                                if self.dircheck(str(self.winlogpath)) == "Directory Exists":
                                        self.start_flag = 2
                                        print "GCSV3 LOG directory        :    [ READY ]"

                                        #Checking Script Directory
                                        if self.dircheck(str(self.winscptpath)) == "Directory Exists":
                                                self.start_flag = 3
                                                print "GCSV3 SCRIPT directory     :    [ READY ]"

                                                #Auto-Startup Setup
                                                if self.startup_setup() == "Startup Setup Success":
                                                        print "GCSV3 Autostartup          :    [  OK  ]"
                                                elif self.startup_setup() == "Maunal":
                                                        print "GCSV3 Autostartup          :    [  N/A  ]"
                                                        print "         - Maunal Autostartup setup is required."
                                                else:
                                                        print "GCSV3 Autostartup          :    [ FAILED ]  "
                                                        print "         - Maunal Autostartup setup is required."
                                                        
                                                print "GCSV3                      :    [ READY ]"
                                                print "-------------------------" 
                                                
                                        elif self.dircheck(str(self.winscptpath)) == "Creation ERROR":
                                                self.start_flag = 1
                                                print "%s directory creation error." % str(self.winscptpath)
                                                print "WARNING: GCSV3 Will Not Function Properly."
                                        else:
                                                self.start_flag = 1
                                                print "%s directory Missing and unable to create." % str(self.winscptpath)
                                                print "WARNING: GCSV3 Will Not Function Properly."
                                
                                elif self.dircheck(str(self.winlogpath)) == "Creation ERROR":
                                        self.start_flag = 1
                                        print "%s directory creation error." % str(self.winfilepath)
                                        print "WARNING: GCSV3 Will Not Function Properly."
                                else:
                                        self.start_flag = 1
                                        print "%s directory Missing and self.TxscriptPIDunable to create." % str(self.winfilepath)
                                        print "WARNING: GCSV3 Will Not Function Properly."
                        
                        elif self.dircheck(str(self.windirpath)) == "Creation ERROR":
                                self.start_flag = 1
                                print "%s directory creation error." % str(self.windirpath)
                                print "WARNING: GCSV3 Will Not Function Properly."
                        else:
                                self.start_flag = 1
                                print "%s directory Missing and unable to create." % str(self.windirpath)
                                print "WARNING: GCSV3 Will Not Function Properly."
                        
                else:
                        self.start_flag = 1
                        print "Platform : UNKNOWN"
                        print "WARNING: GenericCommand Will Not Function Properly."


#Auto-Start Functions ENDED




#Script and Logging
        def stringprocess(self, inputmemory):
                tempo = time.asctime(time.localtime(time.time()))
                newstring = str(tempo) +" : " + str(inputmemory)
                return newstring

        def antistringprocess(self, inputmemory):
                timelength = len(str(time.asctime(time.localtime(time.time())))) + len(" : ")
                inputmemory = inputmemory[timelength:]
                return inputmemory

        def makefilename(self, filename, extension):
                filename_w_extension = str(filename) + str(extension)
                return filename_w_extension
        
        def makefile(self, location, filename_w_extension):
                try:
                        while os.access(str(location)+"/"+str(filename_w_extension), os.F_OK) == False:
                                f= open(str(location)+"/"+str(filename_w_extension), "w")
                                f.close()
                                del f
                                if os.access(str(location)+"/"+str(filename_w_extension), os.F_OK) == True:
                                        break
                                        return "File Created"
                                else:
                                        pass
                except:
                        try:
                                f.close()
                        except:
                                pass
                        return "FAILED - File Not Created"

        def writefile(self, filepath, data):
                self.fob = open(filepath, "w")
                self.fob.writelines(data)
                self.fob.close()

        def file_scripter(self, contents, destination, filename, extension=".No_ext", permit=777):
                if extension == ".No_ext":
                        Rlogname = str(str(filename))
                else:
                        Rlogname = str(self.makefilename(str(filename), str(extension)))
                if str(sys.platform[0:3]).upper() == "LIN":
                        if self.dircheck(str(destination)) == "Directory Exists":
                                if os.access(str(destination)+"/"+Rlogname, os.F_OK) == True and os.access(str(destination)+"/"+Rlogname, os.R_OK) == True and os.access(str(destination)+"/"+Rlogname, os.W_OK) == True:			
                                        return "file exists"
                                else:
                                        try:
                                                self.makefile(str(destination), Rlogname)
                                                self.writefile(str(destination)+"/"+Rlogname, contents)
                                                subprocess.Popen("chmod %s %s/%s" %(str(permit), str(destination), Rlogname), shell=True, stdout=subprocess.PIPE).stdout
                                                return "File Scripted"
                                        except:
                                                return "Scripting Error"
                        else:
                                return "Invalid Directory"

                elif str(sys.platform[0:3]).upper() == "WIN":
                        if self.dircheck(str(destination)) == "Directory Exists":
                                if os.access(str(destination)+"/"+Rlogname, os.F_OK) == True and os.access(str(destination)+"/"+Rlogname, os.R_OK) == True and os.access(str(destination)+"/"+Rlogname, os.W_OK) == True:			
                                        return "file exists"
                                else:
                                        try:
                                                self.makefile(str(destination), Rlogname)
                                                self.writefile(str(destination)+"/"+Rlogname, contents)
                                                return "File Scripted"
                                        except:
                                                return "Scripting Error"
                        else:
                                return "Invalid Directory"

        def file_tracer(self, target_path):
                try:
                        raw_status = []
                        if os.access(target_path, os.F_OK) == True:			
                                raw_status= ["t", "a", "r", "g", "e", "t", " ", "e", "x", "i", "s", "t", "s", ":", " ", "-", "-", "-"]
                                if os.access(target_path, os.R_OK) == True:
                                        raw_status[-3] = "r"
                                if os.access(target_path, os.W_OK) == True:
                                        raw_status[-2] = "w"
                                if os.access(target_path, os.X_OK) == True:
                                        raw_status[-1] = "x"
                                status = ""
                                for char in raw_status:
                                        status += char
                                del raw_status
                                return status
                        else:
                                return "target not exists"
                except:
                        return "File Trace Error"

        def delete(self, location, filename=".No_ext"):
                        try:
                                if filename == ".No_ext":
                                        if os.access(str(location), os.F_OK) == True:
                                                try:			
                                                        try:
                                                                os.unlink(str(location))
                                                        except:
                                                                pass
                                                        try:
                                                                shutil.rmtree(str(location))
                                                        except:
                                                                pass
                                                except:
                                                        return "FAILED: Bad Path or File Name"			
                                                else:
                                                        return "Completed"
                                        else:
                                                return "FAILED: File not exists"

                                else:
                                        if os.access(str(location)+str(filename), os.F_OK) == True:
                                                try:
                                                        file_path = os.path.join(str(location), str(filename))			
                                                        try:
                                                                os.unlink(file_path)
                                                        except:
                                                                pass
                                                        try:
                                                                shutil.rmtree(file_path)
                                                        except:
                                                                pass
                                                except:
                                                        return "FAILED: Bad Path or File Name"			
                                                else:
                                                        return "Completed"
                                        else:
                                                return "FAILED: File not exists"
                        except:
                                return "FAILED: Exception Raised"

        def masterdelete(self, location):
                try:
                        if os.access(str(location), os.F_OK) == True and os.access(str(location), os.R_OK) == True and os.access(str(location), os.W_OK) == True and os.access(str(location), os.X_OK) == True:
                                try:
                                        for contents in os.listdir(str(location)):
                                                file_path = os.path.join(str(location), str(contents))
                                                try:
                                                        os.unlink(file_path)
                                                except:
                                                        pass
                                                try:
                                                        shutil.rmtree(file_path)
                                                except:
                                                        pass
                                except:
                                        return "ERROR - Unable to Master Delete"			
                                else:
                                        return "Completed"
                        else:
                                return "ERROR - Unknown Directory"
                except:
                        return "ERROR - Exception Raised"
                        
        def readlog(self, filepath):
                try:	
                        self.fob = open(filepath, "r")
                except IOError:
                        print "No such file for %s" % str(filepath)
                        listline = ["No Such File\n"]
                else:
                        try:	
                                listline = self.fob.readlines()
                        except AttributeError:
                                self.fob.close()
                                listline = ["No Report Found\n"]
                        
                        else:	
                                self.fob.close()		

                templist = []
                for lines in listline:
                        templist.append(lines.rstrip("\n"))
                del listline
                return templist

        def contlog(self, filepath, newdata):
                newdata = self.stringprocess(str(newdata))	
                templistdata = self.readlog(filepath)
                proprevdata = []
                for line in templistdata:
                        line = line.rstrip("\n")
                        proprevdata.append(line)
                del templistdata
                proprevdata.append(newdata)

                self.prevdata = []
                for line in proprevdata:	
                        if line.find("\n") == -1:
                                line = line + "\n"
                        else:
                                pass				
                        self.prevdata.append(line)
                del proprevdata

                self.writefile(filepath, self.prevdata)	

        def masterdeleteAllLog(self):
                if str(sys.platform[0:3]).upper() == "LIN":
                        tempo = self.masterdelete(str(self.logpath))
                        if tempo == "Completed":
                                print ("TimemasterdeletealllogPASSED == All logs erased.")
                                return ("TimemasterdeletealllogPASSED == All logs erased.")
                        elif tempo == "ERROR - Unable to Master Delete":
                                print ("TimemasterdeletealllogFAILED == Error in Deleting Log Folder Contents.")
                                return ("TimemasterdeletealllogFAILED == Error in Deleting Log Folder Contents.")
                        elif tempo == "ERROR - Unknown Directory":
                                print ("TimemasterdeletealllogFAILED == UNKNOWN Directory")
                                return ("TimemasterdeletealllogFAILED == UNKNOWN Directory")                                

                elif str(sys.platform[0:3]).upper() == "WIN":
                        tempo = self.masterdelete(str(self.winlogpath))
                        if tempo == "Completed":
                                print ("TimemasterdeletealllogPASSED == All logs erased.")
                                return ("TimemasterdeletealllogPASSED == All logs erased.")
                        elif tempo == "ERROR - Unable to Master Delete":
                                print ("TimemasterdeletealllogFAILED == Error in Deleting Log Folder Contents.")
                                return ("TimemasterdeletealllogFAILED == Error in Deleting Log Folder Contents.")
                        elif tempo == "ERROR - Unknown Directory":
                                print ("TimemasterdeletealllogFAILED == UNKNOWN Directory")
                                return ("TimemasterdeletealllogFAILED == UNKNOWN Directory")
                else:
                        print "TimemasterdeletealllogFAILED == Unknown OS."
                        return "TimemasterdeletealllogFAILED == Unknown OS."

        def makelog (self, logname):
                Rlogname = str(self.makefilename(str(logname), str(self.logextension)))
                if str(sys.platform[0:3]).upper() == "LIN":
                        if os.access(self.logpath+Rlogname, os.F_OK) == True and os.access(self.logpath+Rlogname, os.R_OK) == True and os.access(self.logpath+Rlogname, os.W_OK) == True:			
                                self.contlog(self.logpath+Rlogname, self.logactionbarrier)
                                self.contlog(self.logpath+Rlogname, str(logname.upper()) +" ACTION STARTS HERE")
                        else:
                                self.makefile(self.logpath, Rlogname)

                elif str(sys.platform[0:3]).upper() == "WIN":
                        if os.access(self.winlogpath+Rlogname, os.F_OK) == True and os.access(self.winlogpath+Rlogname, os.R_OK) == True and os.access(self.winlogpath+Rlogname, os.W_OK) == True:			
                                self.contlog(self.winlogpath+Rlogname, self.logactionbarrier)
                                self.contlog(self.winlogpath+Rlogname, str(logname.upper()) +" ACTION STARTS HERE")
                        else:
                                self.makefile(self.winlogpath, Rlogname)

                else:
                        print "TimeupdatelogFAILED == Unknown OS!"
                        return "TimeupdatelogFAILED == Unknown OS!"
                

        def deleteLog(self, logname):
                Rlogname = str(self.makefilename(str(logname), str(self.logextension)))
                if str(sys.platform[0:3]).upper() == "LIN":
                        tempo = self.delete(str(self.logpath), Rlogname)
                        if tempo == "Completed":
                                print ("TimedeletePASSED == %s has been erased." % str(Rlogname))
                                return ("TimedeletePASSED == %s has been erased." % str(Rlogname))
                        elif tempo == "FAILED: Bad Path or File Name" or tempo == "FAILED: File not exists":
                                print "TimedeleteFAILED == %s Log not exists or Bad Log Name." % str(logname)			
                                return "TimedeleteFAILED == %s Log not exists or Bad Log Name." % str(logname)

                elif str(sys.platform[0:3]).upper() == "WIN":
                        tempo = self.delete(str(self.winlogpath), Rlogname)
                        if tempo == "Completed":
                                print ("TimedeletePASSED == %s has been erased." % str(Rlogname))
                                return ("TimedeletePASSED == %s has been erased." % str(Rlogname))
                        elif tempo == "FAILED: Bad Path or File Name" or tempo == "FAILED: File not exists":
                                print "TimedeleteFAILED == %s Log not exists or Bad Log Name." % str(logname)			
                                return "TimedeleteFAILED == %s Log not exists or Bad Log Name." % str(logname)
                else:
                        print "TimedeleteallFAILED == Unknown OS!"
                        return "TimedeleteallFAILED == Unknown OS!"
                        
        def updatelog(self, logname, data):
                Rlogname = str(self.makefilename(str(logname), str(self.logextension)))
                newdata = self.stringprocess(str(data))
                if str(sys.platform[0:3]).upper() == "LIN":
                        if os.access(self.logpath+Rlogname, os.F_OK) == True and os.access(self.logpath+Rlogname, os.R_OK) == True and os.access(self.logpath+Rlogname, os.W_OK) == True:			
                                self.contlog(self.logpath+Rlogname, data)
                        else:
                                self.writefile(self.logpath+Rlogname, newdata)

                elif str(sys.platform[0:3]).upper() == "WIN":
                        if os.access(self.winlogpath+Rlogname, os.F_OK) == True and os.access(self.winlogpath+Rlogname, os.R_OK) == True and os.access(self.winlogpath+Rlogname, os.W_OK) == True:			
                                self.contlog(self.winlogpath+Rlogname, data)
                        else:
                                self.writefile(self.winlogpath+Rlogname, newdata)

                else:
                        print "TimeupdatelogFAILED == Unknown OS!"
                        return "TimeupdatelogFAILED == Unknown OS!"

        def reportlog(self, logname):
                Rlogname = str(self.makefilename(str(logname), str(self.logextension)))
                if str(sys.platform[0:3]).upper() == "LIN":
                        if os.access(self.logpath+Rlogname, os.F_OK) == True and os.access(self.logpath+Rlogname, os.R_OK) == True and os.access(self.logpath+Rlogname, os.W_OK) == True:			
                                return self.readlog(self.logpath+Rlogname)
                        else:
                                return ["Log not Found"]

                elif str(sys.platform[0:3]).upper() == "WIN":
                        if os.access(self.winlogpath+Rlogname, os.F_OK) == True and os.access(self.winlogpath+Rlogname, os.R_OK) == True and os.access(self.winlogpath+Rlogname, os.W_OK) == True:			
                                return self.readlog(self.winlogpath+Rlogname)
                        else:
                                return ["Log not Found"]			

                else:
                        print "TimereportFAILED == Unknown OS!"
                        return ["TimereportFAILED == Unknown OS!"]

        def timeexecute_pyscripter(self, action, filename):
                logname = str(self.makefilename(str(filename), str(self.logextension)))
                sptname = str(self.makefilename(str(filename), str(self.pyscptextension)))
                if str(sys.platform[0:3]).upper() == "LIN":
                        Rlogname = self.logpath + logname
                        Rsptname = self.scptpath + sptname

                elif str(sys.platform[0:3]).upper() == "WIN":
                        Rlogname = self.winlogpath + logname
                        Rsptname = self.winscptpath + sptname
                else:
                        return "FAILED - Unknown OS"
                

                content = """#scripter contents
import os
import subprocess
import time
import sys

desg_action = r\"\""%s"\"\"
log_place = r"%s"
scpt_place = r"%s"

def stringprocess(inputmemory):
        tempo = time.asctime(time.localtime(time.time()))
        newstring = str(tempo) +" : " + str(inputmemory)
        return newstring

def writefile(filepath, data):
        fob = open(filepath, "w")
        fob.writelines(data)
        fob.close()
                
def readlog(filepath):
        try:	
                fob = open(filepath, "r")
        except IOError:
                print "No such file for " + str(filepath)
                listline = ["No Such File\\n"]
        else:
                try:	
                        listline = fob.readlines()
                except AttributeError:
                        fob.close()
                        listline = ["No Report Found\\n"]
                
                else:
                        fob.close()		

        templist = []
        for lines in listline:
                templist.append(lines.rstrip("\\n"))
        del listline
        return templist

def contlog(filepath, newdata):
        newdata = stringprocess(str(newdata))	
        templistdata = readlog(filepath)
        proprevdata = []
        for line in templistdata:
                line = line.rstrip("\\n")
                proprevdata.append(line)
        del templistdata
        proprevdata.append(newdata)

        prevdata = []
        for line in proprevdata:	
                if line.find("\\n") == -1:
                        line = line + "\\n"
                else:
                        pass				
                prevdata.append(line)
        del proprevdata

        writefile(filepath, prevdata)

def updatelog(data):
        newdata = stringprocess(str(data))
        if str(sys.platform[0:3]).upper() == "LIN":
                if os.access(log_place, os.F_OK) == True and os.access(log_place, os.R_OK) == True and os.access(log_place, os.W_OK) == True:			
                        contlog(log_place, data)
                else:
                        writefile(log_place, newdata)

        elif str(sys.platform[0:3]).upper() == "WIN":
                if os.access(log_place, os.F_OK) == True and os.access(log_place, os.R_OK) == True and os.access(log_place, os.W_OK) == True:			
                        contlog(log_place, data)
                else:
                        writefile(log_place, newdata)


status = subprocess.Popen(str(desg_action), shell=True, stdout=subprocess.PIPE).stdout
updatelog("GCSV3_COMMANDED: Executed :" + desg_action)

for element in status:
        updatelog(element)        
        sys.stdout.flush()

os.unlink(scpt_place)
exit()               
""" % (str(action),str(Rlogname),str(Rsptname))
		print content
                if str(sys.platform[0:3]).upper() == "LIN":
                        self.file_scripter(content, self.scptpath, filename, self.pyscptextension)
                        subprocess.Popen(r"python %s"% Rsptname, shell=True, stdout=subprocess.PIPE).stdout
                elif str(sys.platform[0:3]).upper() == "WIN":
                        self.file_scripter(content, self.winscptpath, filename, self.pyscptextension)
                        subprocess.Popen(r"%s %s"% (self.win_python_location, Rsptname), shell=True, stdout=subprocess.PIPE).stdout               
                del content
        
#Script Logging ENDED




#File Transfers
        def fileTx_pyscripter(self, file_location, port, bufsz, filesize, checksum, filename):
                logname = str(self.makefilename(str(filename), str(self.logextension)))
                sptname = str(self.makefilename(str(filename), str(self.pyscptextension)))
                if str(sys.platform[0:3]).upper() == "LIN":
                        Rlogname = self.logpath + logname
                        Rsptname = self.scptpath + sptname

                elif str(sys.platform[0:3]).upper() == "WIN":
                        Rlogname = self.winlogpath + logname
                        Rsptname = self.winscptpath + sptname
                else:
                        return "FAILED - Unknown OS"
                

                content = """#scripter contents
import socket
import time
import sys
import os
import hashlib

fileLocate = r"%s"
log_place = r"%s"
scpt_place = r"%s"
buf=%s
constbuf = buf
port=%s
ip=''
size=%s
checksum_value = "%s"


def stringprocess(inputmemory):
        tempo = time.asctime(time.localtime(time.time()))
        newstring = str(tempo) +" : " + str(inputmemory)
        return newstring

def writefile(filepath, data):
        fob = open(filepath, "w")
        fob.writelines(data)
        fob.close()
                
def readlog(filepath):
        try:	
                fob = open(filepath, "r")
        except IOError:
                print "No such file for " + str(filepath)
                listline = ["No Such File\\n"]
        else:
                try:	
                        listline = fob.readlines()
                except AttributeError:
                        fob.close()
                        listline = ["No Report Found\\n"]
                
                else:	
                        fob.close()		

        templist = []
        for lines in listline:
                templist.append(lines.rstrip("\\n"))
        del listline
        return templist

def contlog(filepath, newdata):
        newdata = stringprocess(str(newdata))	
        templistdata = readlog(filepath)
        proprevdata = []
        for line in templistdata:
                line = line.rstrip("\\n")
                proprevdata.append(line)
        del templistdata
        proprevdata.append(newdata)

        prevdata = []
        for line in proprevdata:	
                if line.find("\\n") == -1:
                        line = line + "\\n"
                else:
                        pass				
                prevdata.append(line)
        del proprevdata

        writefile(filepath, prevdata)

def updatelog(data):
        newdata = stringprocess(str(data))
        if str(sys.platform[0:3]).upper() == "LIN":
                if os.access(log_place, os.F_OK) == True and os.access(log_place, os.R_OK) == True and os.access(log_place, os.W_OK) == True:			
                        contlog(log_place, data)
                else:
                        writefile(log_place, newdata)

        elif str(sys.platform[0:3]).upper() == "WIN":
                if os.access(log_place, os.F_OK) == True and os.access(log_place, os.R_OK) == True and os.access(log_place, os.W_OK) == True:			
                        contlog(log_place, data)
                else:
                        writefile(log_place, newdata)

updatelog ("TimeFileTransfers Begins..")
try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.bind((ip,port))
except:
        updatelog ("Port is Not Available.")
else:
        updatelog ("Socket Client Begin to Listen")
        client.listen(1)
        channel,details=client.accept()
        updatelog('Socket Connected from:' +str(details))

        try:
                f = open(fileLocate,'wb')        
        except Exception, e:
                try:
                        f.close()
                        os.unlink(fileLocate)
                except:
                        pass
                updatelog("File creation Error: " + str(e))
                updatelog("-------------------")
                updatelog("File Recieved Failed.")
                updatelog("-------------------")
        else:
                try:
                        a=10
                        while True:
                            got=channel.recv(constbuf)
                            f.write(got)
                            sys.stdout.flush()
                            rxsize = str(os.path.getsize(fileLocate))
                            rxsize.rstrip("L")
                            percent=(long(rxsize)*100)/size
                            if percent == a:
                                updatelog("Transferring: "+ str(percent) + " percent")
                                a+=10  
                            if not got:
                                    updatelog("Transferring: Completed")                 
                                    break      
                        f.close()

                except:
                        try:
                                f.close()
                                os.unlink(fileLocate)
                        except:
                                pass
                        updatelog("Transfers Link Broken.")
                        updatelog("-------------------")
                        updatelog("File Recieved Failed.")
                        updatelog("-------------------")

                else:
                        md5data = hashlib.md5()
                        try:
                            f = open(fileLocate, 'rb')
                            while True:
                                data = f.read(10240)
                                if len(data) == 0:
                                    break
                                md5data.update(data)
                            f.close()
                        except:
                                f.close()
                                updatelog("Checksum FAILED.")
                                updatelog("-------------------")
                                updatelog("File Recieved Failed.")
                                updatelog("-------------------")
                                os.unlink(fileLocate)
                        else:
                                checksum = md5data.hexdigest()
                                if str(checksum) == checksum_value:
                                    updatelog("Checksum SUCCESS.")
                                    updatelog("-------------------")
                                    updatelog("File Recieved Successfully.")
                                else:
                                    updatelog("Checksum FAILED.")
                                    updatelog("-------------------")
                                    updatelog("File Recieved Failed.")
                                updatelog("-------------------")


updatelog("Closing Socket....")
channel.shutdown(socket.SHUT_RDWR)
channel.close()
updatelog("Socket Closed")
del channel, details
del client

os.unlink(scpt_place)
exit()               

""" % (str(file_location), str(Rlogname), str(Rsptname), str(bufsz), str(port), str(filesize), str(checksum))

                if str(sys.platform[0:3]).upper() == "LIN":
                        self.file_scripter(content, self.scptpath, filename, self.pyscptextension)
                        self.TxscriptPID = subprocess.Popen(r"python %s"% Rsptname, shell=True, stdout=subprocess.PIPE).pid
                elif str(sys.platform[0:3]).upper() == "WIN":
                        self.file_scripter(content, self.winscptpath, filename, self.pyscptextension)
                        self.TxscriptPID = subprocess.Popen(r"%s %s"% (self.win_python_location, Rsptname), shell=True, stdout=subprocess.PIPE).pid
                        print "SCRIPT IS RUNNING! = " + str(self.TxscriptPID)
                del content
                        
        def fileTx_script_kill(self):
                if str(sys.platform[0:3]).upper() == "LIN":
                        subprocess.Popen("kill %s" % str(self.TxscriptPID), shell=True).pid
                        self.TxscriptPID = None

                elif str(sys.platform[0:3]).upper() == "WIN":
                        subprocess.Popen("taskkill /pid %s" % str(self.TxscriptPID), shell=True).pid
                        self.TxscriptPID = None

        def TxscriptPID_reset(self):
                self.TxscriptPID = None

#File Transfers ENDED
                
##############################################################################################################################################



#GENERIC COMMAND SERVER STRUCTURE
#############################################
class GenericCommandServer(GCV3):
    #GenericCommand V1.0 Commmands (Basic Commands)
    ##########################################
        def execute(self, command):
                response = ""
                for element in os.popen(command):
                    response += element
                return response

        def test(self):
                return "XML-RPC connection is OK"
    ##########################################


    #GenericCommand V2.0 Commands
    #################################################################################
        def timeexecute(self, tcommand, parsename, flag):
                self.timeexecute_status = "locked"
                self.makelog(parsename)
                if flag == 2:
                        self.updatelog(parsename, "GCSV3_COMMANDED: Executed : " + str(tcommand))
                        outcome = subprocess.Popen(str(tcommand), shell=True, stdout=subprocess.PIPE).stdout
                        for element in outcome:
                                self.updatelog(parsename, element)        
                                sys.stdout.flush()
                else:
                        self.timeexecute_pyscripter(str(tcommand), str(parsename))
                        print(parsename, "%s scripted." % tcommand)
                
        def timereport(self, parsename):
                ans = self.reportlog(parsename)
                return ans

        def timedelete(self, parsename):
                ans = self.deleteLog(parsename)
                return ans

        def timemasterdeletealllog(self):
                ans = self.masterdeleteAllLog()
                return ans
    #################################################################################



    #GenericCommand V3.0 Commands
    #################################################################################
        def teststart(self):
                ans = self.test_start()
                return ans
                
        def timefiletrace(self, target_location):
                ans = self.file_tracer(str(target_location))
                return ans

        def timefilescript(self, body, path, filename, extension=None, permit=777):
                ans = self.file_scripter(str(body), str(path), str(filename), extension, int(permit))
                return ans

        def timedeletefile(self, target_path):
                ans = self.delete(str(target_path))
                return ans

        def timefolderflush(self, folder_location):
                ans = self.masterdelete(folder_location)
                return ans
                
        def timefiletransfer(self, file_location, port, buff, filesize, checksum, logname):
                self.fileTx_pyscripter(file_location, port, buff, filesize, checksum, logname)

        def self_destruct(self):
                ans = self.removal_setup()
                return ans
    #################################################################################






#############################################################################################################################
# Main Code
#############################################################################################################################
print "XTP GenericCommand Server"
print "-------------------------"
print ("IP address                 :    %s \nDesignated port            :    %s"% (ipadd,port))
genericCommandServer = GenericCommandServer()
#######################################
#DEBUG ZONE
#genericCommandServer.self_destruct()
#######################################

server = SimpleXMLRPCServer.SimpleXMLRPCServer((ipadd, int(port)), SimpleXMLRPCServer.SimpleXMLRPCRequestHandler, True, True)
server.register_instance(genericCommandServer)
server.serve_forever()


