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

# Setup serial interface
serial.port = serial.Serial("/dev/ttyUSB0", 115200, timeout=0.5)

# Send initialization command
#serial.port.write("<Command><Name>initialize</Name><Refresh>N</Refresh></Command>")
serial.port.write("<Command><Name>initialize</Name></Command>")

#serial.port.write("<Command><Name>get_device_info</Name></Command>")

# Get Schedule information
# Possible events: time, price, demand, summation, message
getScheduleInfo = '''<Command>
                       <Name>get_schedule</Name>
                       <MeterMacId>0xd8d5b900000020ba</MeterMacId>
                       <Event>price</Event>
				   </Command>'''
serial.port.write(getScheduleInfo)


def cmdSerialWrite(cmd):
	results = '<data>'
	cmdTemplate = '''<Command>
	                       <Name>%s</Name>
					 </Command>''' % (cmd)
	serial.port.write(cmdTemplate)
	for line in serial.port.readlines():
		line = line.strip('\n')
		line = line.strip('\r')
		results += line
	results += '</data>'
	return results

def cmdSerialWriteRefresh(cmd, refresh):
	results = '<data>'
	cmdTemplate = '''<Command>
	                       <Name>%s</Name>
	                       <Refresh>%s</Refresh>
					 </Command>''' % (cmd, refresh)
	serial.port.write(cmdTemplate)
	for line in serial.port.readlines():
		line = line.strip('\n')
		line = line.strip('\r')
		results += line
	results += '</data>'
	return results

# Build big string of XML.
data = cmdSerialWrite('get_current_price')

data = cmdSerialWriteRefresh('get_current_summation_delivered', 'Y')

# Create Element object, parsing XML.
root = ET.fromstring(data)

# Enumerate Element and get the 'demand' and timestamps
lastTime = 0
for child in root:
	print '> %s' % child.tag
	for item in child:
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
			dright = int(val, 0)
		elif key == 'DigitsLeft':
			dleft = int(val, 0)
	print 'Demand: %s \nTime since last poll: %s' % (demand, diff)
	print 'digits right of decimal: %s' % dright
	print 'digits leftt of decimal: %s' % dleft



def cmdSerialWrite(cmd, mac):
	cmdEventTemplate = '''<Command>
	                       <Name>%s</Name>
	                       <MeterMacId></MeterMacId>
	                       <Event></Event>
					   </Command>''' % (cmd, mac)
	serial.port.write(cmdTemplate)

get_current_price = '''<Command>
  <Name>get_current_price</Name>
  <Refresh>Y</Refresh>
</Command>'''
serial.port.write(get_current_price)


# Read command results
for line in serial.port.readlines():
	if line.startswith('<Demand>'):


