#!/bin/bash

is_python_installed=0
if  [[ $(which python) ]] ; then
       echo "Python is installed"
        python --version
        is_python_installed=1
fi
if [[ $(which python3) ]] ; then
	echo "Python is installed"
	python3 --version
	is_python_installed=1
fi
if [[ $is_python_installed == 0 ]] ; then
	echo "Python installation not found"
	echo "installing python"
	export DEBIAN_FRONTEND=noninteractive
	apt-get update
	apt-get install -y software-properties-common
	add-apt-repository ppa:deadsnakes/ppa
	apt-get install -y python3.8
fi
