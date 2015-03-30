#!/usr/bin/env python
# cosm.py Copyrigth 2012 Itxaka Serrano Garcia <itxakaserrano@gmail.com>  
# licensed under the GPL2  
# see the full license at http://www.gnu.org/licenses/gpl-2.0.txt  
# edited by Der-Eddy from elitepvpers

import json, subprocess, os, time, re

#add your privat stuff here
feed = "YOUR_FEED"
apikey = "YOUR_KEY"

hdd = subprocess.check_output(["df | grep rootfs | awk '{print $2,$4,$5}'"], shell=True)
hdd = hdd.split()
hdd = int(hdd[1]) / 1024

cpu = subprocess.check_output(["vmstat | awk '{print $13}'"], shell=True)
cpu = cpu.split()[1]

cpu_temp = subprocess.check_output(["sudo /opt/vc/bin/vcgencmd measure_temp | cut -c6-9"], shell=True)

mem = subprocess.check_output(["cat /proc/meminfo | grep Mem | awk '{print $2}'"], shell=True)
mem = mem.split()
mem_total = int(mem[0]) / 1024
mem_free = int(mem[1]) / 1024
mem_used = mem_total - mem_free

mhz = subprocess.check_output(["vcgencmd measure_clock arm | cut -d'=' -f2-"], shell=True)
mhz = int(mhz) / 1000000
mhz = int(round(mhz, -2))

volts = subprocess.check_output(["vcgencmd measure_volts | cut -c6-9"], shell=True)

up = float(subprocess.check_output(["cat /proc/uptime | cut -d'.' -f1-1"], shell=True))
up = round(up / 60 / 60, 3)

ps = subprocess.check_output(["ps -A | awk '{print $1}'"], shell=True)
ps = len(ps) - 1

net = subprocess.check_output(["ifconfig eth0 | grep RX\ bytes"], shell=True)
rx_bytes = re.findall('RX bytes:([0-9]*) ', net)[0]
tx_bytes = re.findall('TX bytes:([0-9]*) ', net)[0]
rx_bytes = round(float(rx_bytes) / 1024 / 1024, 2)
tx_bytes = round(float(tx_bytes) / 1024 / 1024, 2)
total_bytes = rx_bytes + tx_bytes
connections = subprocess.check_output(["netstat -nta --inet | wc -l"], shell=True)

data = json.dumps({"version":"1.0.0", "datastreams":[{"id":"hdd","current_value":hdd },{"id":"cpu","current_value":cpu},{"id":"free_mem","current_value":mem_free},{"id":"used_mem","current_value":mem_used},{"id":"cpu_temp","current_value":cpu_temp},{"id":"cpu_frequency","current_value":mhz},{"id":"uptime","current_value":up},{"id":"processes","current_value":ps},{"id":"volts_core","current_value":volts},{"id":"network_receive","current_value":rx_bytes},{"id":"network_send","current_value":tx_bytes},{"id":"network_total","current_value":total_bytes},{"id":"network_connections","current_value":connections},]})
with open("temp.json", "w") as f:
	f.write(data)
subprocess.call(['curl --request PUT --data-binary @temp.json --header "X-ApiKey: {0}" --verbose http://api.cosm.com/v2/feeds/{1}'.format(apikey, feed)], shell=True)

os.remove("temp.json")
