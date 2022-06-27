#!/bin/bash
#
# Created By: misraX
# Github: github.com/misrax
# License: MIT
# CopyWrite: 2017
# Bash script to install and generate pip requirements.txt from inside a virtualenv.
# By using pip freeze to creat a list of all the virtualenviroment pip packeges.
# It's just a simple way of creating the pip requirements.txt for a development use.
# usage pip-install package1 package2 package3 .. package(n)... etc 
# 
packages=($1)

echo "Starting to install packages, Hooopa....." 
   #check virtualenv path 
if [[ "$VIRTUAL_ENV" != "" ]]; then 
    echo "You are in a working virtualenv $VIRTUAL_ENV";
   # virtual_env > check if packages is empty .. if [[ ]]; then
    if [[ "$packages" != "" ]]; then
    pip install "${packages[@]}";
    echo "Whre do u wanna save your requirements.txt type the path and click [ENTER]"
    ls "$VIRTUAL_ENV"
    read requirements_path
        # virtual_env > > package > if read is empty ... if [[ ]]; then 
        if [[ "$requirements_path" ==  ""  ]]; then
            echo "Oh pleae, Enter something :D, now to call this script again use prepare"
            exit 1;
        # virtual_env > packages > read > if virtualevn/read is a valid directory.. elif [[ ]]; then 
        elif [[ -d "$VIRTUAL_ENV/$requirements_path"  ]]; then
        #statements
            echo "creating requirements.txt";
            pip freeze > "$VIRTUAL_ENV/$requirements_path/requirements.txt"
        # > virtul_env > package > read > not a valid directory .. else; fi
        else 
        echo "This is not a vail directory under $(ls $VIRTUAL_ENV) path"
    fi
# virtual_env > packages .. else; fi 
  else 
    echo "Please enter at least one package to install";
    exit 1;
  fi 
# virtual_env .. else; fi
else 
    echo "You are not in a working virtualenv"
    echo "Exiting .........."
    exit 1;
fi 

#
#TODO
#adding enviroments variable to set DJANG_PATH and REQUIRMETS_PATH.
#