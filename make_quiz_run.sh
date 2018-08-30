#!/usr/bin/bash

read -e -p "Specify the file you want to use: " file_name
read -p "Specify the number of questions: " numq
file_name=${file_name/#\~/$HOME}
filename_noext=${file_name%%.*}
python qgen.py \
-f $file_name \
-n $numq \
-q $filename_noext-qgen.txt \
-a $filename_noext-ans.txt \
-A $filename_noext-allq.txt
gedit $filename_noext-qgen.txt
