#!/bin/bash

dir=$(cd $(dirname $0); pwd)
procname=$(grep '"ProcessName":' ${dir}/team_api/pub/config.py | awk '{print $2}' | awk -F \" '{print $2}')
pidfile=/tmp/${procname}.pid

case $1 in
start)
    [ -d ${dir}/team_api/logs/ ] || mkdir -p ${dir}/team_api/logs/
    if [ -f $pidfile ]; then
        if [[ $(ps aux | grep $(cat $pidfile) | grep -v grep | wc -l) -lt 1 ]]; then
            $(which python) -O ${dir}/team_api/Product.py &> /dev/null &
            pid=$!
        fi
    else
        $(which python) -O ${dir}/team_api/Product.py &> /dev/null &
        pid=$!
    fi
    if [[ $(ps aux | grep $procname | grep -v grep | wc -l) = "1" ]]; then
        echo $pid > $pidfile
    else
        echo "Start error, please check ${dir}/team_api/logs/sys.log"
        exit 1
    fi
    ;;

stop)
    killall $procname
    retval=$?
    if [ $retval -eq 0 ]; then
        rm -f $pidfile
    else
        kill -9 `cat $pidfile`
        retval=$?
        rm -f $pidfile
        echo "$procname stop over"
    fi
    ;;

restart)
    ./$0 stop
    ./$0 start
    ;;

status)
    pid=$(ps aux | grep $procname | grep -v grep | awk '{print $2}')
    if [ ! -f $pidfile ]; then
        echo -e "\033[39;31m${procname} has stopped.\033[0m"
        exit
    fi
    if [[ $pid != $(cat $pidfile) ]]; then
        echo -e "\033[39;31m异常，pid文件与系统pid值不相等。\033[0m"
        echo -e "\033[39;34m  系统pid：${pid}\033[0m"
        echo -e "\033[39;34m  pid文件：$(cat ${pidfile})($(echo $pidfile))\033[0m"
    else
        echo -e "\033[39;33m${procname}\033[0m":
        echo "  pid: $pid"
	echo -e "  state:" "\033[39;32mrunning\033[0m"
        echo -e "  process run time:" "\033[39;32m$(ps -eO lstart | grep $procname | grep -v grep | awk '{print $6"-"$3"-"$4,$5}')\033[0m"
    fi
    ;;

*)
    ./$0 start
    ;;
esac
