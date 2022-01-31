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

def isExistBeforeGetFlagAndPort(filename, contentBefore):
    filename_tmp = ""
    tmp_dict = ""
    ret = False
    for line in contentBefore:
        tmp_dict = json.loads(line)
        filename_tmp = tmp_dict["filename"]
        if filename == filename_tmp:
            ret = [tmp_dict["flag"], tmp_dict["port"]]
    return ret

def generateFlags(filelist):
    tmp_flag = ""
    contentBefore = []
    if not os.path.exists(FLAG_BAK_FILENAME):
        os.popen("touch " + FLAG_BAK_FILENAME)
    with open(FLAG_BAK_FILENAME, 'r') as f:
        while 1:
            line = f.readline()
            if not line:
                break
            contentBefore.append(line)
    # bin's num != flags.txt's linenum, empty the flags.txt
    if len(filelist) != len(contentBefore):
        os.popen("echo '' > " + FLAG_BAK_FILENAME)
        contentBefore = []
    port = PORT_LISTEN_START_FROM + len(contentBefore)
    with open(FLAG_BAK_FILENAME, 'w') as f:
        flag_list = []
        for filename in filelist:
            flag_dict = {}
            ret = isExistBeforeGetFlagAndPort(filename, contentBefore)
            if ret == False:
                tmp_flag = "flag{" + str(uuid.uuid4()) + "}"
                flag_dict["port"] = port
                port = port + 1
            else:
                tmp_flag = ret[0]
                flag_dict["port"] = ret[1]
                
            flag_dict["filename"] = filename
            flag_dict["flag"] = tmp_flag
            
            flag_list.append(flag_dict)
        
        flag_json = json.dumps(flag_list,indent=4, separators=(',', ':'))
        print(flag_json)
        f.write(flag_json)
        f.close()

generateFlags(getFileList())
