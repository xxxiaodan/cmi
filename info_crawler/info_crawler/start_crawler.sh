#!/bin/bash
while true
do
  file_data=$(cat signal.txt)
  if [ "$file_data" = "over" ];then
     killall -9 python
     sleep 5
     python start.py
  elif [ "$file_data" = "start" ];then
     sleep 10
  fi
done
