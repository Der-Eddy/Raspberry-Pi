#!/bin/sh
#/etc/rc.local - boot
#/bin/mount /dev/sda1 /mnt/usb

#savedir=/home/pi/cam
savedir=/mnt/usb/cam
while :
do
	filename=$(date -u +"%d%m%Y_%H%M-%S").jpg
	#/opt/vc/bin/raspistill -o $savedir/$filename
	/opt/vc/bin/raspistill -o $savedir/$filename -exposure night
	#sleep 4s
	sleep 30s
done
