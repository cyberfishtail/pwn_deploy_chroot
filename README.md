# pwn_deploy_chroot

## Forked from

https://github.com/giantbranch/pwn_deploy_chroot

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

### 4. Edit flags.json as necessary

```
[
    {
        "port":10000,
        "filename":"rip",
        "flag":"flag{bddc24eb-61f0-4095-8d66-74cf2f1222a2}"
    }
]
```

### 5. Run step2.py

```
python3 step2.py
```

### 6. Docker compose run

```
docker-compose up --build -d
```
