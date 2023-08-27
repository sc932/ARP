# ARP Project
**Scott Clark and Kyle Emich Project**

## Summary

This code allows you to compute team scores
using radial basis functions. This is an
incredibly effective way to predict team
performance (see citation).

## Web Usage

### Using Google Collab (free, but Google account required)

1. 

## Local Installation

### Windows 10/11

**Install pre-reqs**

1. Install windows linux subsystem (WSL). Instructions: https://learn.microsoft.com/en-us/windows/wsl/install (this will install a Ubuntu VM within Windows)
2. Install python (https://medium.com/@rhdzmota/python-development-on-the-windows-subsystem-for-linux-wsl-17a0fa1839d)

**Install ARP**

1. Open the WSL terminal
2. Run the following commands
```
git clone ...
cd ...
pip3 --upgrade
pip3 install requirements.txt
```

### Mac OSX 10.4+

**Install pre-reqs**

1. Install python (https://www.python.org/downloads/macos/)
2. Install a proper terminal (https://iterm2.com/downloads.html)

**Install ARP**

1. Open iTerm2
2. Run the following commands
```
git clone ...
cd ...
pip3 --upgrade
pip3 install requirements.txt
```

### Ubuntu

**Install pre-reqs**

1. Congratulations. You're done.

**Install ARP**

1. Open a terminal
2. Run the following commands
```
git clone ...
cd ...
pip3 --upgrade
pip3 install requirements.txt
```

## Running ARP

### Writing your YAML configuration file

1. Open a text editor of your choice (suggestions below)

### In a terminal

1. Open the terminal (from above)
2. Navigate (`cd <directory>`) to the directory `git` cloned the repo into (from above)
3. Run the following command
```
python3 runner.py --help
```
4. You will see the following output
```
$ python3 runner.py --help
usage: runner.py [-h] [-p P_THRESHOLD] yml

This will run through the code described in [paper X]. For more information see [website Y].

positional arguments:
  yml                   .yml file with config values

options:
  -h, --help            show this help message and exit
  -p P_THRESHOLD, --p-threshold P_THRESHOLD
                        p-val threshold for when to print output
```
5. Follow the instructions (example below)
```
python3 runner.py Fall2013Fordham_Scott.yml -p 0.05
```