#!/bin/bash
while true
do
  hour=`date +%H`
  if [ $hour -gt 7 -a $hour -lt 24 ];then
      file_data=$(cat signal.txt)
      if [ "$file_data" = "over" ];then
         killall -9 python
         sleep 3000
         python start.py
      elif [ "$file_data" = "start" ];then
         sleep 20
      fi
  fi
done
