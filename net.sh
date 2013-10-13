#!/bin/bash
#40:A6:D9:4B:3D:EF is the Mac Address of my iPhone
while :
do
	#net=$(netdiscover -P)
	net=$(netdiscover -r 192.168.178.0/24 -P)
	if [[ $net =~ .*40:a6:d9:4b:3d:ef.* ]]
	then
		echo "True"
	else
		echo "False"
	fi
	sleep 10s
done
