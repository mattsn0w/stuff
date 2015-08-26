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
import os
#import pdb


def epochtodate(seconds):
	'''Convert an int() epoc value to a tuple, then to human readable timestamp.'''


def datetoepoch(dateStamp):
	''' Make a tuple. convert tuple to epoch seconds. Account for 30y offset.'''
	tupleresult = time.strptime(dateStamp, '%Y-%m-%d %H:%M:%S')
	results = int(time.mktime(tupleresult)) + 985500000
	return results

def hextodec(val):
	'''Convert the hex values returned by the Rainforest automation's device to
	int() or float() values.'''
	result = None
	if val is str():
		result = int(val, 16)
	elif val is not str():
		result = int(val)
	return result


def serialwrite(cmd, refresh=None):
	'''First command should always be: initialize
	commands: 
			get_current_price, get_current_summation_delivered, get_current_period_usage.
			get_schedule, set_schedule.
	        get_device_info, get_meter_info, set_meter_info.
	        get_connection_status, get_network_info, get_time,
	        get_message, confirm_message
	        get_current_price, set_current_price, get_instantaneous_demand.
	        get_current_period_usage, get_last_period_usage.
	        set_fast_poll.
	'''
	devices = ['/dev/ttyUSB0', '/dev/ttyUSB1', '/dev/ttyUSB2']
	for device in devices:
		if os.path.exists(device):
			try:
				ser = serial.Serial(device, 115200, timeout=1)
				ser.flushInput()
				ser.flushOutput()
			except:
				raise
	results = '<data>'
	if refresh:
		cmd = '''<Command><Name>%s</Name><Refresh>Y</Refresh></Command>''' % (cmd)
	else:
		cmd = '''<Command><Name>%s</Name><Refresh>N</Refresh></Command>''' % (cmd)
	# Send new command.
	ser.write(cmd)
	while True:
		print 'True and reading...'
		# While readline and readlines are supported, reading the buffer sequentially ensures
		# a valid XML element structure.
		# Remove the \r\ns since we don't need linefeeds.
		buf = ser.read(1000)
		buf = buf.replace('\r', '')
		buf = buf.replace('\n', '')
		if len(buf) > 0:
			results += buf
			#print buf
			break
	results += '</data>'
	if ser.isOpen():
		ser.close()
	return results


def xmltodicts(xet):
	'''Convert string to XML Element Tree to a dictionary with elements as keys.'''
	results = {}
	try:
		root = ET.fromstring(xet)
		if ET.iselement(root):
			for e in root:
				for i in e:
					print 'key: %s, val: %s' % (i.tag, i.text)
					if i.text.startswith('0x'):
						i.text = hextodec(i.text)
					results[i.tag] = i.text
	finally:
		return results


# data = cmdSerialWrite('get_current_summation_delivered', True)

# Initialize
serialwrite('initialize')
# Build big string of XML.
data = serialwrite('get_current_price')
# Create Element object, parsing XML.



for c in root:
	print '<%s>' % c.tag
	for i in c:
		if i.tag == 'TimeStamp' or i.tag == 'UTCTime':
			'''Sometimes this value is a datestamp, sometimes it is a hex value.'''
			if i.text.startswith('1985'):
				print 'format is YYYY-MM-DD'
				now = dateToEpoch(i.text) + epoch30yOffset
			elif i.text.startswith('0x'):
				print 'format is hex val'
				print 'type is %s' % type(i.text)
				if type(i.text) is str:
					i.text = int(i.text, 0)
				now = i.text + epoch30yOffset
			timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(now)))
			print 'timestamp create: %s' % timestamp
		elif i.tag == 'Demand':
			demand = int(i.text)
		elif i.tag == 'DigitsRight':
			print 'i.text in DigitsRight is: %s' % i.text
			odx = i.text
			watts = str(int(lastDemand))[:-odx] + '.' + str(int(lastDemand))[-odx:]
		elif i.tag == 'Price':
			price = i.text
		print '\t<%s>\n\t\t%s\n\t</%s>' % (i.tag, i.text, i.tag)
	print '</%s>' % c.tag



