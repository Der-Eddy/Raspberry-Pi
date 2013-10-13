#!/bin/sh
# Backup OS to the USB Hard Disk Drive

# Create a filename with datestamp for our current backup (without .img suffix)
ofile="/mnt/usb/images/raspbian-$(date +%y-%m-%d)"

# Create final filename, with suffix
ofilefinal=$ofile.img

# Begin the backup process, should take about 1 hour from 8Gb SD card to HDD
sudo dd if="/dev/mmcblk0" of=$ofile bs=1M

# Collect result of backup procedure
result=$?

# If command has completed successfully, delete previous backups and exit
#if [ $result=0 ]; then rm -f /mnt/usb/backup_*.img; mv $ofile $ofilefinal; exit 0;fi
if [ $result=0 ]; then mv $ofile $ofilefinal; tar cfvj $ofile.tar.bz2 $ofilefinal; rm -f $ofile.img;

MASKE='raspbian-*'
declare -i MAXKEEP=20
IFS='
'
declare -i cnt=0

for x in $(find . -name "$MASKE" -type f -printf '%T@ %p\n'|sort -n -r); do
    fname=$(echo $x|awk '{print $2}')
    if [ $((++cnt)) -gt $MAXKEEP ]; then
        # echo "removing no. $cnt : $fname"
        [ -f "$fname" ] && rm -i $fname
    fi
done

exit 0;fi

#If command has failed, then delete partial backup file
if [ $result=1 ]; then rm -f $ofile; exit 1;fi
