from requests import post
from ctypes import windll
from string import ascii_uppercase
from time import sleep, time
from shutil import disk_usage
from platform import node, system

WAIT_TIME = 10 # seconds
BLACKLIST = ["N", "S"]

# Okay, this one is from StackOverflow too... but can you really blame me?
def get_drives():
    if system() == "Windows":
        drives = []
        bitmask = windll.kernel32.GetLogicalDrives()
        for letter in ascii_uppercase:
            if bitmask & 1 and letter not in BLACKLIST:
                drives.append(letter)
            bitmask >>= 1
        return drives
    else:
        return ["/"]

while True:
    try:
        dat = {"hostname": node(), "disks": []}
        for disk in get_drives():
            try:
                usage = disk_usage(disk + ":")
                dat["disks"].append([disk, usage.free, usage.total, time()])
            except:
                pass
        post("http://10.13.10.39:8000/submit", json=dat)
    except:
        pass
    sleep(WAIT_TIME)