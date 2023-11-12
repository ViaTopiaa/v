#!/bin/python3
# Growtopia save.dat decoder

from struct import unpack
import sys
import platform

def HELP():
    HELP_TEXT = """
Growotopia save.dat decoder
by Zoxorer

usage: savedat.py <file>

parameter:
    file                                Growotopia save.dat file

example:
    savedat.py save.dat
    """
    print(HELP_TEXT)




def deviceInfo():
    funcs = ["python_version","system", "machine","architecture","win32_ver"]
    print("System Information")
    for func in funcs:
        print("\t"+str(func)+":",str(getattr(platform,func)()))
    if(hasattr(sys,"getandroidapilevel")):
        print("\tPython Android: YES (%s)" % (sys.getandroidapilevel()))
    print("\n")


def decryptTankidPassword(data):
    print("[warn] Password decryption is Experimental, may not work properly")
    res = ""
    for n,char in enumerate(data):
        res += chr(char-(100+n))
    return res
def dump(stream):
    stream.seek(4)
    while True:
        TYPE = unpack("<I", stream.read(4))[0]
        if(TYPE in [1,2,5,9]):
            LENGTH = unpack("<I", stream.read(4))[0]
            KEY = stream.read(LENGTH)
            VALUE = stream.read(4)
            if(TYPE == 5):
                VALUE = unpack("?", VALUE[0].to_bytes(1,"little"))[0]
            elif(TYPE == 1):
                VALUE = unpack("f", VALUE)[0]
            elif(TYPE == 2):
                VALUE_LENGTH = unpack("<i", VALUE)[0]
                VALUE = stream.read(VALUE_LENGTH)
                if(KEY == b"tankid_password"):
                    try:
                        VALUE = decryptTankidPassword(VALUE)
                    except Exception as e:
                        print("[error] Unable to decrypt tankid_password: ",e,"(continuing)");
            elif(TYPE == 9):
                VALUE = unpack("<i",VALUE)[0]
            else:
                print("ERROR! Can't parse type: %s (continuing)" % (TYPE))
            print("[result] %s : %s" % (KEY.decode(), VALUE))
        elif(TYPE == 0):
            break
        else:
            print("[error] Can't parse type: %s (continuing)" % (TYPE))

if __name__ == "__main__":
    ARGS = sys.argv
    if(len(ARGS) < 2):
        HELP()
        exit()
    deviceInfo()
    try:
        FILE = open(ARGS[1], "rb")
        print("\t\t---------- dump ----------")
        dump(FILE)
    except Exception as e:
        print("[error]",e)
