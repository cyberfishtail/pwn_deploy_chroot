from config import *
import os
import uuid
import json

def getFileList():
    filelist = []
    for filename in os.listdir(PWN_BIN_PATH):
        filelist.append(filename)
    filelist.sort()
    return filelist

def getFlags():
    with open('flags.json', 'r') as f:
        return json.load(f)

def checkFlag(flag_dict):
    if flag_dict == None or flag_dict == {}:
        return False
    if flag_dict["port"] < 0 or flag_dict["port"] > 65535:
        return False
    if not os.path.exists('''bin/{0}'''.format(flag_dict["filename"])):
        print('''bin/{0} not exist'''.format(flag_dict["filename"]))
        return False
    return True


def generateFlags(filelist):
    
    ## if previous flags.json exist
    have_previous_flags = False
    if os.path.exists('flags.json'):
        previous_flags = getFlags()
        have_previous_flags = True
    
    flags_dic_list = []
    port = PORT_LISTEN_START_FROM

    for filename in filelist:
        flag_dict = {}
        if have_previous_flags == True:
            for previous_flag in previous_flags:
                if previous_flag != None:
                    if previous_flag["filename"] == filename:
                        flag_dict = previous_flag 
                        break
        
        if have_previous_flags == False or not checkFlag(flag_dict):
            flag_dict["port"] = port
            port = port + 1
            flag_dict["filename"] = filename
            tmp_flag = "flag{" + str(uuid.uuid4()) + "}"
            flag_dict["flag"] = tmp_flag

        flags_dic_list.append(flag_dict)
        flags_json = json.dumps(flags_dic_list,indent=4, separators=(',', ':'))
    
    ## write json into file 
    with open('flags.json', 'w') as f:
        f.write(flags_json)
        f.close()
    print(flags_json)

generateFlags(getFileList())
