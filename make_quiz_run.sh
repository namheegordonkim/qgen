#!/usr/bin/bash
read -e -p "Specify the file you want to use: " filename
read -p "Specify the number of questions: " numq
filename=${filename/#\~/$HOME}
filename_noext=${filename%%.*}
echo $filename $numq
python ~/workspace/qgen/qgen.py \
-f $filename \
-n $numq \
-q $filename_noext-qgen.txt \
-a $filename_noext-ans.txt \
-A $filename_noext-allq.txt
gedit $filename_noext-qgen.txt
