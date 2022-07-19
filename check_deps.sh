#!/bin/bash

is_python_installed=0

which python;
if [ $? = 0 ] ; then
       echo "Python is installed"
	echo $(python --version)
	is_python_installed=1
fi	
if [ $is_python_installed = 0 ] ; then
    echo "Python installation not found"
    echo "installing python"
    apt-get update
    apt-get install software-properties-common
    add-apt-repository ppa:deadsnakes/ppa
    apt-get install python3.8
fi
