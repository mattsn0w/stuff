#!/bin/env python

import serial
import time
import xml.etree.ElementTree as ET

# Setup serial interface
serial.port = serial.Serial("/dev/ttyUSB0", 115200, timeout=0.5)

# Send initialization command
#serial.port.write("<Command><Name>initialize</Name><Refresh>N</Refresh></Command>")
serial.port.write("<Command><Name>initialize</Name></Command>")

serial.port.write("<Command><Name>get_device_info</Name></Command>")
'''
	'<DeviceInfo>\r\n'
    '  <DeviceMacId>0xd8d5b900000020ba</DeviceMacId>\r\n'
	'  <InstallCode>0x9e542351cbe4c42d</InstallCode>\r\n'
	'  <LinkKey>0x612680b440bdd56677c2d15e76e8d480</LinkKey>\r\n'
	'  <FWVersion>1.4.48 (6952)</FWVersion>\r\n'
	'  <HWVersion>1.3.3</HWVersion>\r\n'
	'  <ImageType>0x0e01</ImageType>\r\n'
	'  <Manufacturer>Rainforest Automation, Inc.</Manufacturer>\r\n'
	'  <ModelId>Z105-2-EMU2-LEDD</ModelId>\r\n'
	'  <DateCode>2013110523320640</DateCode>\r\n'
	'</DeviceInfo>\r\n'
'''
# Get Schedule information
# Possible events: time, price, demand, summation, message
getScheduleInfo = '''<Command>
                       <Name>get_schedule</Name>
                       <MeterMacId>0xd8d5b900000020ba</MeterMacId>
                       <Event>price</Event>
				   </Command>'''
serial.port.write(getScheduleInfo)

def cmdSerialWrite(cmd):
	results = ['<root>']
	cmdTemplate = '''<Command>
	                       <Name>%s</Name>
					 </Command>''' % (cmd)
	serial.port.write(cmdTemplate)
	for line in serial.port.readlines():
		line = line.strip('\n')
		line = line.strip('\r')
		results.append(line)
	results.append('</root>')
	return results

def cmdSerialWrite(cmd):
	results = '<root>'
	cmdTemplate = '''<Command>
	                       <Name>%s</Name>
					 </Command>''' % (cmd)
	serial.port.write(cmdTemplate)
	for line in serial.port.readlines():
		line = line.strip('\n')
		line = line.strip('\r')
		results += line
	results += '</root>'
	return results

# Build big string of XML.
data = cmdSerialWrite('get_current_price')

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
		if key == 'TimeStamp':
			now = val
			diff = now - lastTime
			lastTime = val
	print '%s : %s' % (demand, diff)



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


