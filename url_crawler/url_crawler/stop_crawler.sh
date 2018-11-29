ps -ef|grep start_crawler | grep -v grep |awk '{print $2}'|xargs -n1 kill -9
echo 'over' > signal.txt
