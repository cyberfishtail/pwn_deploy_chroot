# pwn_deploy_chroot

> A project for deploying ctf pwn challenge use chroot

中文请点击：

[README_CN.md](https://github.com/giantbranch/pwn_deploy_chroot/blob/master/README_CN.md)

常见问题：

[FAQ.md](https://github.com/giantbranch/pwn_deploy_chroot/blob/master/FAQ.md)

详细部署示例：

[如何安全快速地部署多道ctf pwn比赛题目 - How to deploy many ctf pwn game safely and quickly](http://www.giantbranch.cn/2018/09/24/%E5%A6%82%E4%BD%95%E5%AE%89%E5%85%A8%E5%BF%AB%E9%80%9F%E5%9C%B0%E9%83%A8%E7%BD%B2%E5%A4%9A%E9%81%93ctf%20pwn%E6%AF%94%E8%B5%9B%E9%A2%98%E7%9B%AE/)

## Before

```
# Install the latest version docker
curl -s https://get.docker.com/ | sh
# Install docker compose
apt install docker-compose
```

## How to Use

### 1. Git clone

```
git clone https://github.com/cyberfishtail/pwn_deploy_chroot
```

### 2. Add pwn executable files into ./bin directory

```
cd pwn_deploy_chroot
rm bin/*
mv yourfile bin/
```

You can edit config.py to decide whether to replace /bin/sh with catflag
```
# Whether to replace /bin/sh

## replace
REPLACE_BINSH = True
## not replace(default)
REPLACE_BINSH = False
```

### 3. Run step1.py

```
python3 step1.py
```

### 4. Edit flag.txt

### 5. Run step2.py

```
python3 step2.py
```

### 6. Docker run

```
docker-compose up --build -d
```



## Attention

The flag will be generated by the step1.py and it store in flags.txt

The port information of the pwn program is also inside the flags.txt.


## Reference

https://github.com/Eadom/ctf_xinetd
