import subprocess

def list_interface():
    command = "nmcli device status | grep 'wifi' | awk '{print $1}'"
    res = subprocess.run(command, shell=True, capture_output=True, check=True, text=True)
    interface=res.stdout.strip().split('\n')
    return interface

def start_monitor_mode(mon_if):
    subprocess.run(["sudo","ip","link","set",mon_if,"down"])
    subprocess.run(["sudo","iw",mon_if,"set","type","monitor"])
    subprocess.run(["sudo","ip","link","set",mon_if,"up"])

def list_monitor_interface():
    cmd="iwconfig 2>/dev/null | awk '/Mode:Monitor/ {print $1}'"
    inf=subprocess.run(cmd,shell=True,capture_output=True,text=True,check=True)
    mon_if=inf.stdout.strip()
    return mon_if

def stop_monitor_mode(mon_if):
    # cmd="sudo airmon-ng stop"
    subprocess.run(["sudo","ip","link","set",mon_if,"down"])
    subprocess.run(["sudo","iw",mon_if,"set","type","managed"])
    subprocess.run(["sudo","ip","link","set",mon_if,"up"])
    # subprocess.run(["sudo", "airmon-ng", "stop", mon_if], check=True, text=True)

def ls_active_wifi(mon_if):
    ls_Wifi=subprocess.run(["sudo","airodump-ng",mon_if],check=True,text=True)

    
if __name__ == "__main__":
    # ifname=list_interface()
    mon_if=list_monitor_interface()
    print(mon_if)
