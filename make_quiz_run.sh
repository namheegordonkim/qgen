#!/usr/bin/bash

read -e -p "Specify the file you want to use: " file_name
read -p "Specify the number of questions: " numq
export file_name
python qgen.py $file_name $numq
gedit $file_name"-qgen.txt"
