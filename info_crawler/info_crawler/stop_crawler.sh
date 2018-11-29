ps -ef|grep start_crawler.sh | grep -v grep |awk '{print $2}'|xargs -n1 kill -9
killall -9 python
echo 'over' > signal.txt
