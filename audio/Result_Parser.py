import os

class Result_Parser(object):
    # Auto-initialization
    def __init__(self):
        self.inheritance = object
        self.winlocation = "c:"
        self.winresultlocation = "%s\Test_Results" % self.winlocation
        #Folder Check
        #######################################################################################
        if os.access(str(self.winresultlocation), os.F_OK) == False:		
            while 1:
                    try:
                            os.mkdir(str(self.winresultlocation))
                    except:
                            try:
                                    shutil.rmtree(str(self.winresultlocation))
                            except:
                                    pass
                            os.mkdir(str(self.winresultlocation))
                    if os.access(str(self.winresultlocation), os.F_OK) == True:
                        break 
                        pass
        else:
            pass
        #######################################################################################



    ##############################################################################################
    # Meta Functions
    ##############################################################################################
    def makefilename(self, filename, extension=".txt"):
        name = str(filename) + str(extension)
        return name
    
    def parse(self, filename, keyword, ref_symbol="="):
        #To check file existance
        if os.access(filename, os.F_OK) == False:
            return "FAILED - Invalid Filename"
        else:
            pass

        #To read the file
        try:
            f = open(filename, 'r')
            lineread = f.readlines()
            f.close()
        except:
            try:
                f.close()
            except:
                pass
            return "FAILED - Unable to read file"
        try:
            #To process actual data lines
            realline = []
            for i in lineread:
                if i.find(ref_symbol)>0:
                    i = i.rstrip()
                    i = i.rstrip("\n")
                    i = i.rstrip()
                    realline.append(i)
            del lineread

            #To find actual data based on keywords
            for line in realline:
                if line[:len(str(keyword))] == str(keyword) and len(line[:line.find(str(ref_symbol))].rstrip()) == len(str(keyword)):
                    data = line[line.find(str(ref_symbol))+1:]
                    data = data.lstrip()
                    data = data.rstrip()
                    return data
                else:
                    pass
            return "FAILED - No Such Keyword"

        except Exception, e:
            print str(e)
            return "FAILED - Unable to Prase Data Lines"

    def parsewrite(self, filename, keyword, new_data, ref_symbol="="):
        #To check file existance
        if os.access(filename, os.F_OK) == False:
            return "FAILED - Invalid Filename"
        else:
            pass

        #To read the file
        try:
            f = open(str(filename), 'r')
            lineread = f.readlines()
            f.close()
        except:
            try:
                f.close()
            except:
                pass
            return "FAILED - Unable to read file"
        
        try:
            #To process actual data lines
            realline = []
            for i in lineread:
                if i.find(ref_symbol)>0:
                    i = i.rstrip()
                    i = i.rstrip("\n")
                    i = i.rstrip()
                    realline.append(i)
            lineread = []
            
            #To find actual data and do database modifications based on keywords
            for line in realline:
                if line[:len(str(keyword))] == str(keyword) and len(line[:line.find(str(ref_symbol))].rstrip()) == len(str(keyword)):
                    ref = line[:line.find(str(ref_symbol))]
                    ref = ref.lstrip()
                    ref = ref.rstrip()
                    newdataline = ref + " " + str(ref_symbol) + " " + str(new_data)                    
                    lineread.append(newdataline)
                else:
                    lineread.append(line)
            
            realline = []        
            for line in lineread:
                line = line + "\n"
                realline.append(line)

            #To write the new list
            try:
                f = open(str(filename), 'w')
                f.writelines(realline)
                f.close()
                return "PASSED - Data has been parsed"
            except:
                try:
                    f.close()
                except:
                    pass
                try:
                    f.open(str(filename)+"_BACKUP.txt", 'w')
                    f.writelines(lineread)
                    f.close()
                except:
                    pass
                return "FAILED - Unable to Update Database File. Backup File written."
                

        except Exception, e:
            print "Error: " + e
            return "FAILED - Unable to Prase Data Lines"

    def parse_newwrite(self, filename, keyword, data, ref_symbol="="):
        #To check file existance
        if os.access(filename, os.F_OK) == False:
            return "FAILED - Invalid Filename"
        else:
            pass

        #To read the file
        try:
            f = open(str(filename), 'r')
            lineread = f.readlines()
            f.close()
        except:
            try:
                f.close()
            except:
                pass
            return "FAILED - Unable to read file"
        
        try:           
            #To add new keywords and data
            lineread.append(str(keyword) + " " + str(ref_symbol) + " " + str(data)+ "\n")
            
            #To write the new list
            try:
                f = open(str(filename), 'w')
                f.writelines(lineread)
                f.close()
                return "PASSED - Data has been parsed"
            except:
                try:
                    f.close()
                except:
                    pass
                try:
                    f.open(str(filename)+"_BACKUP.txt", 'w')
                    f.writelines(lineread)
                    f.close()
                except:
                    pass
                return "FAILED - Unable to Update Database File. Backup File written."
                
        except Exception, e:
            print "Error: " + e
            return "FAILED - Unable to Prase Data Lines"
        
    ##############################################################################################
    #Main Class Functions
    ##############################################################################################
    def verdict_write(self, filename="NULL", testID="NULL", Condition="NULL", ref_symbol="="):
        #Parameter Check
        if testID == "NULL" or Condition == "NULL" or filename=="NULL":
            return "FAILED - Missing TestID, Condition or filename"
        else:
            pass

        #Folder Access Check
        if os.access(self.winresultlocation, os.F_OK) == False:
            return "FAILED - 'c:\\Test_Results' Folder Invalid. Restart class declaration or create manually."
        else:
            pass

        #File Access Logics
        filename_w_extension = self.makefilename(str(filename))
        if os.access(self.winresultlocation+"\\"+filename_w_extension, os.F_OK) == True and os.access(self.winresultlocation+"\\"+filename_w_extension, os.W_OK) == True and os.access(self.winresultlocation+"\\"+filename_w_extension, os.R_OK) == True:
            "Do Prase and Extract"
            #Prase Check Keywords Existance
            ret = self.parse(str(self.winresultlocation+"\\"+filename_w_extension), str(testID))
            if ret == "FAILED - No Such Keyword":
                #Register new TestID
                self.parse_newwrite(str(self.winresultlocation+"\\"+filename_w_extension), testID, str(Condition).upper(), ref_symbol)
            elif ret == "FAILED - Invalid Filename" or ret == "FAILED - Unable to read file" or ret == "FAILED - Unable to Prase Data Lines":
                #Return Error Status
                return ret
            else:
                #Updating TestID Verdict
                self.parsewrite(str(self.winresultlocation+"\\"+filename_w_extension), testID, str(Condition).upper(), ref_symbol)

            
        else:
            
            "Make File and Extract"
            #Make File
            try:
                f = open(str(self.winresultlocation+"\\"+filename_w_extension), 'w')
                f.close()
            except:
                f.close()
                return "ERROR - Make File Error"
            try:
                #Write New Keyword with Data
                f = open(str(self.winresultlocation+"\\"+filename_w_extension), 'w')
                f.write(str(testID) + " " + str(ref_symbol) + " " + str(Condition.upper())+"\n")
                f.close()                
                return "PASSED - Data has been parsed"
            except:
                try:
                    f.close()
                except:
                    pass
                return "FAILED - Unable to Update Data into File"

    def verdict_read(self, filename="NULL", testID="NULL", ref_symbol="="):
        #Parameter Check
        if testID == "NULL" or filename=="NULL":
            return "FAILED - Missing TestID, Condition or filename"
        else:
            pass

        #Folder Access Check
        if os.access(self.winresultlocation, os.F_OK) == False:
            return "FAILED - 'c:\\Test_Results' Folder Invalid. Restart class declaration or create manually."
        else:
            pass

        #File Access Logics
        filename_w_extension = self.makefilename(str(filename))
        if os.access(self.winresultlocation+"\\"+filename_w_extension, os.R_OK) == True:
            ret = self.parse(self.winresultlocation+"\\"+filename_w_extension, str(testID), ref_symbol)
            return ret
        else:
            return "FAILED - Invalid Filename"
        
