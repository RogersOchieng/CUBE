import sys
import subprocess
 
#Checking IP reachability
def ip_reach(list):
 
    for ip in list:
        ip = ip.rstrip()
        
        ping_reply = subprocess.call('ping %s /n 2' % (ip), stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
               
        if ping_reply == 0:
            print("\n* {} is reachable :)\n".format(ip))
            continue
        
        else:
            print('\n* {} not reachable :( Check connectivity and try again.'.format(ip))
            sys.exit()
            
            

def ip_reach(list):
    for ip in list:
        ip = ip.rstrip()
        ping_reply = subprocess.call('ping %s /n 2' % (ip), stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
        if ping_reply == 0:
            print ("\* IP {} is recheable :)".format(ip))
            print(ping_reply)
            continue
        else:
            print ("\* IP {} is not recheable. Please verify connectivity and try again".format(ip))
            sys.exit()