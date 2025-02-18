import subprocess
from pathlib import Path

current_dir = (Path(__file__).resolve().parent)


def setThePasswordText(password):
    with open(f"{str(current_dir)}/enterdPassword.txt","w") as file:
        file.write(password)

def isThePasswordIsCurrect(capFile,password):
    result = subprocess.run(["aircrack-ng","-w","enterdPassword.txt",capFile],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    strResult = str(result)
    return strResult.find(password) != -1

def verifyThePassword(password):
    cap_file = current_dir/"cap/capture-01.cap"

    setThePasswordText(password)
    return isThePasswordIsCurrect(cap_file,password)
    # if isTrue:
    #     print(f"password : {password} is the password of wifi")
    # else:
    #     print("password incorect")
        
