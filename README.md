# ARP Project
**Scott Clark and Kyle Emich Project**

## Summary

This code allows you to compute team scores
using radial basis functions. This is an
incredibly effective way to predict team
performance (see citation).

## Web Usage

### Using Google Collab (free, but Google account required)

1. First, download the git repo (try using the github client: https://desktop.github.com/) and put it in your Google Drive
2. Open the notebook

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

### Using Jupyter Notebook

1. Open the `runner.ipynb` notebook and execute both cells
2. Write your own YAML file for your data as needed (see below)

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
python3 runner.py example.yml -p 0.05
```

6. Write your own YAML file for your data as needed (see below)

## Configuration

### The YAML config file

YAML is a markup language that allows for easy configuration of complex tasks.
For more information check out LINK

### Example YAML file

```
# Example ARP YAML file for more information see README.md
# For help editing a YAML file see link in README.md

### REQUIRED CONFIGS ###
csv_file_name: 'example.csv' # path to csv file with dataset

team_index: 'OvrTeamID' # column name with group id in it

target_vars: ['Perf'] # can be one or more, seperated by commas

big_five: # mapping from csv column name to standard Big 5 names, put # in front of those you wish to ignore
  #Extraverted: 'Extraversion'
  Agreeable: 'Agreeable'
  #Conscientious: 'Conscientiousness'
  Neurotic: 'Neurotic'
  #Open: 'Openness'

### OPTIONAL CONFIGS ###
cog_attrs: [] # cognitive attributes (like GRE, GPA, etc)

pos_attrs: [] # positive NON-Big-5, NON-cognitive attributes (like teamwork, etc)

neg_attrs: [] # negative NON-Big-5, NON-cognitive attributes (like dark triade, etc)

neutral_attrs: [] #'age', 'Sex', 'LANGU', 'NATION', 'ETHNIC', 'COMPANY', 'JOBTITLE', 'JOBDEPT', 'jobcity', 'job_geog', 'JOB_INDUS', 'JOB_FUNC']

### HOW TO DEAL WITH "BAD" DATA ###
missing_values:
  cog_attr_vals: ['0', ] # Teams with members that have these scores for cog_attr with be ignored
  spaces: True # True if teams with members that have whitespace/blanks instead of values should be ignored, otherwise False
  other_vals: ['-9999', ] # Teams with members that have these attribute values will be ignored
```