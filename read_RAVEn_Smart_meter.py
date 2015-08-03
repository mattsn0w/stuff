#!/bin/env python
# Matt Snow <mattatmattsn0wd0tcom>
#
# Script features:
#     - Conect to the Rainforest Automation EMU-2 via USB.
#     - Poll device using RAVEn XML API and normalize results.
#     - Collect metrics relative to: 
#          * current kW draw.
#          * Sumation of kWh to date.
#          * Rate price.
#          * Tier.

import serial
import time
import xml.etree.ElementTree as ET


epoch30yOffset = 985500000

# Setup serial interface
serial.port = serial.Serial("/dev/ttyUSB0", 115200, timeout=0.5)


def cmdSerialWrite(cmd, refresh=None):
	'''First command should always be: initialize

	commands: 
	       get_device_info, get_connection_status, get_current_summation_delivered,
	       get_schedule, set_schedule, get_meter_info, get_network_info, set_meter_info, get_time,
	       get_message, confirm_message, get_current_price, set_current_price, get_instantaneous_demand,
	       get_current_summation_delivered, get_current_period_usage, get_last_period_usage,
	       set_fast_poll.
	'''
	results = '<data>'
	if refresh:
		cmd = '''<Command><Name>%s</Name><Refresh>Y</Refresh></Command>''' % (cmd)
	else:
		cmd = '''<Command><Name>%s</Name><Refresh>N</Refresh></Command>''' % (cmd)
	serial.port.write(cmd)
	for line in serial.port.readlines():
		line = line.strip('\n')
		line = line.strip('\r')
		results += line
	results += '</data>'
	return results



# Enumerate Element and get the 'demand' and timestamps
def parseVals(xmldata):
	lastTime = 0
	demand = None
	for child in root:
		print '> %s' % child.tag
		for item in child:
			# Assign key,val object names for saner reading.
			key = item.tag
			if item.text.startswith('0x'):
				val = int(item.text, 0)
			else:
				val = item.text
			if key == 'Demand':
				demand = val
			elif key == 'TimeStamp':
				now = val
				diff = now - lastTime
				lastTime = val
			elif key == 'DigitsRight':
				dright = val
			elif key == 'DigitsLeft':
				dleft = val
		if all([demand, now, dright]):
			demandStr = str(demand)
			demandStr = '%s.%s' % (demandStr[:-dright], demandStr[-dright:])
			demand = float(demandStr)
		print 'Demand: %s \nTime : %s' % (demand, now)



data = cmdSerialWrite('get_current_summation_delivered', True)

# Build big string of XML.
data = cmdSerialWrite('get_current_price')

# Create Element object, parsing XML.
root = ET.fromstring(data)


for c in root:
	print '<%s>' % c.tag
	for i in c:
		if i.tag == 'TimeStamp':
			i.text = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(i.text, 0)))
		print '\t<%s>\n\t\t%s\n\t</%s>' % (i.tag, i.text, i.tag)
	print '</%s>' % c.tag

