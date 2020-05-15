import paramiko
import os.path
import time
import sys
import re
 
#Checking username/password file 
#Prompting user for input - USER FILE
user_file = input("\n# Enter user file path and name (e.g. D:\MyApps\myusers.txt): ")

#Verifying the validity of the USERNAME/PASSWORD file
if os.path.isfile(user_file) == True:
    print("\n* Username/password file is valid :)\n")
 
else:
    print("\n* File {} does not exist :( Please check and try again.\n".format(user_file))
    sys.exit()
        
#Checking Call Rates file
#Prompting user for input - CALLING RATES FILE
rate_file = input("\n# Please enter rate file name and path. (e.g g:\callrates.csv): ") 
 
#Verifying the validity of the COMMANDS FILE

if os.path.isfile(rate_file) == True:
    print("n\* Rate file is valid :)\n")
        
else:
    print("\n* Rate File {} does not exist :( Please check and try again.\n".format(rate_file))
    sys.exit()
    
#Open SSHv2 connection to the device
def ssh_connection(ip):
    
    global user_file
    global rate_file
    
    #Creating SSH CONNECTION
    try:
        #Define SSH parameters
        selected_user_file = open(user_file, 'r')
        
        #Starting from the beginning of the file
        selected_user_file.seek(0)
        
        #Reading the username from the file
        username = selected_user_file.readlines()[0].split(',')[0].rstrip()
        
        #Starting from the beginning of the file
        selected_user_file.seek(0)
        
        #Reading the password from the file
        password = selected_user_file.readlines()[0].split(',')[1].rstrip()
        
        #Logging into device
        session = paramiko.SSHClient()
        
        #For testing purposes, this allows auto-accepting unknown host keys
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        #Connect to the device using username and password          
        session.connect(ip.rstrip(), username = username, password = password)
        
        #Start an interactive shell session on the router
        connection = session.invoke_shell()    
        
        #Setting terminal length for entire output - disable pagination
        connection.send("enable\n")
        connection.send("terminal length 0\n")
        time.sleep(1)
        
        #Entering global config mode
        connection.send("\n")
        connection.send("configure terminal\n")
        time.sleep(1)
        
        selected_rate_file = open(rate_file, 'r')
        
        
        selected_rate_file.seek(0)

        call_rate_table =selected_rate_file.readlines()

        call_rate_table.pop(0)

        for each_destination in call_rate_table:
            destination_table = each_destination.split(',')
    
            specific_tariff = {destination_table[0] + destination_table[1]:{"ITSP1":destination_table[2],"ITSP2":destination_table[3],"ITSP3":destination_table[4].rstrip()}}
    
            country_code = list(specific_tariff)[0]

            call_rate = list(specific_tariff.values())[0]

            sorted_call_rate = sorted(call_rate.items(), key=lambda x: x[1])

            x = 0
            for each_itsp in sorted_call_rate:
                if each_itsp[0] == "ITSP1":
                    connection.send ("dial-peer voice 1" + country_code + "1 voip\n")
                    time.sleep(2)
                    connection.send ("preference {} ".format(x) + "\n")
                    time.sleep(2)
                elif each_itsp[0] == "ITSP2":
                    connection.send ("dial-peer voice 1" + country_code + "2 voip\n")
                    time.sleep(2)
                    connection.send ("preference {} ".format(x) + "\n")
                    time.sleep(2)
                elif each_itsp[0] == "ITSP3":
                    connection.send ("dial-peer voice 1" + country_code + "3 voip\n")
                    time.sleep(2)
                    connection.send ("preference {} ".format(x) + "\n")
                    time.sleep(2)
                x = 1 + x
            
        connection.send("end\n")
        time.sleep(2)
        connection.send("write memory\n")
        time.sleep(6)
        #Closing the user file
        selected_user_file.close()
        
        #Closing the rate file
        selected_rate_file.close()
        
        #Checking command output for IOS syntax errors
        router_output = connection.recv(65535)
        
        if re.search(b"% Invalid input", router_output):
            print("* There was at least one IOS syntax error on device {} :(".format(ip))
            
        else:
            print("\nDONE for device {} :)\n".format(ip))
            
        #Test for reading command output
        print(str(router_output) + "\n")
        
        #Closing the connection
        session.close()
     
    except paramiko.AuthenticationException:
        print("* Invalid username or password :( \n* Please check the username/password file or the device configuration.")
        print("* Closing program... Bye!")