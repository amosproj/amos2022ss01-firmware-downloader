#!/bin/bash

for py_file in $(find ../unit_test -name *.py);
do
	python $py_file;
done