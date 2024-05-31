#!/bin/bash

iteration="20"
command="python Audio_loopback.py -f 48 -b 16 -s 1 -m I2S -i 10.221.120.134 -e 10.221.120.15"

if [ "$1" != "" ]; then
	    command=$1
	        if [ "$2" != "" ]; then
			        iteration=$2
				    fi
			    fi

			    flag=0
			    while [ $flag -lt $iteration ]; do
				        $command
					    flag=$((flag+1))
					        echo -e "=============Iteration "$flag" done================"
					done

