#!/bin/bash

dir=$(cd $(dirname $0);pwd)
pidfile=/tmp/team_api.pid

case $1 in
start)
    [ -d ${dir}/team_api/logs/ ] || mkdir -p ${dir}/team_api/logs/
    if [ -f $pidfile ]; then
        if [[ $(ps aux | grep $(cat $pidfile) | grep -v grep | wc -l) -lt 1 ]]; then
            $(which python) -O ${dir}/Product.py &> /dev/null &
            pid=$!
            echo $pid > $pidfile
        else
            :
        fi
    else
        $(which python) -O ${dir}/Product.py &> /dev/null &
        pid=$!
        echo $pid > $pidfile
    fi
    ;;

stop)
    killall Team.Api
    retval=$?
    if [ $retval -eq 0 ]; then
        rm -f $pidfile
    else
        kill -9 `cat $pidfile`
        retval=$?
        sleep 1
        [ "$retval" = "0" ] && rm -f $pidfile || echo "Stop Error"
    fi
    ;;

restart)
    $0 stop
    $0 start
    ;;

*)
    $0 start
    ;;
esac
