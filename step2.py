from config import *
import time
import json

def getFlagsAndSave():
    with open('flags.json', 'r') as f:
        flags_json = json.load(f)
    with open('backup/flags_{0}.json'.format(time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())), 'w') as f:
        f.write(json.dumps(flags_json,indent=4, separators=(',', ':')))
    return flags_json

def generateXinetd(flags):
    conf = ""
    uid = 1000
    for flag in flags:
        conf += XINETD % (flag["port"], str(uid) + ":" + str(uid), flag["filename"], flag["filename"])
        uid = uid + 1
    with open(XINETD_CONF_FILENAME, 'w') as f:
            f.write(conf)

def generateDockerfile(flags):
    conf = ""
    # useradd and put flag
    runcmd = "RUN "
    
    for flag in flags:
        runcmd += "useradd -m " + flag["filename"] + " && "
   
    for x in range(0, len(flags)):
        if x == len(flags) - 1:
            runcmd += "echo '" + flags[x]["flag"] + "' > /home/" +  flags[x]["filename"] + "/flag.txt" 
        else:
            runcmd += "echo '" + flags[x]["flag"] + "' > /home/" + flags[x]["filename"] + "/flag.txt" + " && "
    # print runcmd 

    # copy bin
    copybin = ""
    for flag in flags:
        copybin += "COPY " + PWN_BIN_PATH + "/" + flag["filename"]  + " /home/" + flag["filename"] + "/" + flag["filename"] + "\n"
        if REPLACE_BINSH:
            copybin += "COPY ./catflag" + " /home/" + flag["filename"] + "/bin/sh\n"
        else:
            copybin += "COPY ./catflag" + " /home/" + flag["filename"] + "/bin/sh\n"

    # print copybin

    # chown & chmod
    chown_chmod = "RUN "
    for x in range(0, len(flags)):
        chown_chmod += "chown -R root:" + flags[x]["filename"] + " /home/" + flags[x]["filename"] + " && "
        chown_chmod += "chmod -R 750 /home/" + flags[x]["filename"] + " && "
        if x == len(flags) - 1:
            chown_chmod += "chmod 740 /home/" + flags[x]["filename"] + "/flag.txt"
        else:
            chown_chmod += "chmod 740 /home/" + flags[x]["filename"] + "/flag.txt" + " && "
    # print chown_chmod

    # copy lib,/bin 
    # dev = '''mkdir /home/%s/dev && mknod /home/%s/dev/null c 1 3 && mknod /home/%s/dev/zero c 1 5 && mknod /home/%s/dev/random c 1 8 && mknod /home/%s/dev/urandom c 1 9 && chmod 666 /home/%s/dev/* && '''
    dev = '''mkdir /home/%s/dev && mknod /home/%s/dev/null c 1 3 && mknod /home/%s/dev/zero c 1 5 && mknod /home/%s/dev/random c 1 8 && mknod /home/%s/dev/urandom c 1 9 && chmod 666 /home/%s/dev/* '''
    if not REPLACE_BINSH:
        # ness_bin = '''mkdir /home/%s/bin && cp /bin/sh /home/%s/bin && cp /bin/ls /home/%s/bin && cp /bin/cat /home/%s/bin'''
        ness_bin = '''&& cp /bin/sh /home/%s/bin && cp /bin/ls /home/%s/bin && cp /bin/cat /home/%s/bin'''
    copy_lib_bin_dev = "RUN "
    for x in range(0, len(flags)):
        copy_lib_bin_dev += "cp -R /lib* /home/" + flags[x]["filename"]  + " && "
        copy_lib_bin_dev += "cp -R /usr/lib* /home/" + flags[x]["filename"]  + " && "
        copy_lib_bin_dev += dev % (flags[x]["filename"], flags[x]["filename"], flags[x]["filename"], flags[x]["filename"], flags[x]["filename"], flags[x]["filename"])
        if x == len(flags) - 1:
            if not REPLACE_BINSH:
                copy_lib_bin_dev += ness_bin % (flags[x]["filename"], flags[x]["filename"], flags[x]["filename"])
            pass                
        else: 
            if not REPLACE_BINSH:   
                copy_lib_bin_dev += ness_bin % (flags[x]["filename"], flags[x]["filename"], flags[x]["filename"]) + " && "
            else:
                copy_lib_bin_dev += " && "

    # print copy_lib_bin_dev

    conf = DOCKERFILE % (runcmd, copybin, chown_chmod, copy_lib_bin_dev)

    with open("Dockerfile", 'w') as f:
        f.write(conf)

def generateDockerCompose(flags):
    ports = ""
    conf = ""
    for flag in flags:
        ports += "- " + str(flag["port"]) + ":" + str(flag["port"]) + "\n    "
        # port = port + 1

    conf = DOCKERCOMPOSE % ports
    # print conf
    with open("docker-compose.yml", 'w') as f:
        f.write(conf)


flags = getFlagsAndSave()
generateXinetd(flags)
generateDockerfile(flags)
generateDockerCompose(flags)

