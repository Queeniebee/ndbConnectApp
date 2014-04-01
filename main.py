
import urllib
import webapp2

try: import simplejson as json
except ImportError: import  json

from google.appengine.api import users
from google.appengine.ext import ndb
from urlparse import urlparse, parse_qs

<<<<<<< HEAD
NO_DEVICE_NAMED = 'no_device_name'

def device_key(device_name = NO_DEVICE_NAMED):
=======
from datetime import datetime # This is being used to reformat the dateTime record
import StringIO # This module is for writing strings into memory.  

import ast



default_device_val = 'no_device_name'

def device_key(device_name = default_device_val):
>>>>>>> 99c82602099b569a8f70d35b6a3a3183587c6395
	"""constructs Datastore key for SensorRecord entity with device_name """
	return ndb.Key('DeviceGroup', device_name)


class SensorRecord(ndb.Model) :
<<<<<<< HEAD
	"""Models a single PinRead from an Arduino with record creation time,  sensor min/max, and Device name"""
	sensorreading= ndb.JsonProperty()
	recordentrytime = ndb.DateTimeProperty(auto_now_add=True)

	#note: all class methods pass the instance of the class as it's first argument 
	@classmethod
	def query_readings_by_device(cls,device_name):
			device_readings_list = []
			device_records_query = cls.query(
			ancestor = device_key(device_name)).order(-SensorRecord.recordentrytime)
			# device_records is a list object only returns sensor reading and time for parsing. 
			device_records = device_records_query.fetch()

		#create methods for pulling different streams of data out for processing. 
			for device_record in device_records:
				device_readings_list.append(device_record.sensorreading)
			return device_readings_list

	@classmethod
	def query_readings_by_device_with_timestamp(cls,device_name):
			device_readings_dict = {}
			device_records_query = cls.query(
			ancestor = device_key(device_name)).order(-SensorRecord.recordentrytime)
			
			device_records = device_records_query.fetch()

			
			return device_records

	@classmethod
	def query_latest_reading(cls,device_name):
		
		device_records_query = cls.query(
			ancestor = device_key(device_name)).order(-SensorRecord.recordentrytime)
			# device_records is a list object only returns sensor reading and time for parsing. 
		device_record = device_records_query.fetch(1)
		return device_record[0].sensorreading
=======
	""" 'sensorreading' accepts an arbitrary number of key/value pairs """
	# Setting compression to 'False' ensures that the retured property when queried is not a binary
	sensorreading= ndb.JsonProperty(
		indexed = True, 
		compressed = False) 
	recordentrytime = ndb.DateTimeProperty(
		auto_now_add=True)

	#note: all class methods pass the instance of the class as it's first argument 
	@classmethod
	def query_readings_by_device(cls,device_name,number_of_entries_to_fetch=0):
		#StringIO creates the String object buffer to store the output. It is 'print()' but to memory instead of the console via the response handler. 
		json_output = StringIO.StringIO() 
		device_records_query = cls.query(
		ancestor = device_key(device_name),
		projection = [SensorRecord.recordentrytime, SensorRecord.sensorreading]).order(-SensorRecord.recordentrytime)
		#If the default value is still '0' then the fetch() method is receives no arguement and should return al records
		if number_of_entries_to_fetch == 0:
			device_records = device_records_query.fetch()
		else:
			device_records = device_records_query.fetch(number_of_entries_to_fetch)
		json_output.write('{ "collection":{ "device_group":"%s", "items":['%(device_name)) 
		j = 0 # this counter is used to test if the for loop has reached the end of the entries
		# The following outer for loop iterates through all returned entries
		for device_record in device_records:
			entry_time = device_record.recordentrytime #.strftime("%a,%b,%d,%H,%M,%S")
			json_output.write('{"datetime" :"%s",'%entry_time)
			# 'ast.literal_eval' converts the returned sensor readings into a list from a unicode string
			#sensor_vals = ast.literal_eval(device_record.sensorreading)
			sensor_vals = json.loads(device_record.sensorreading)
			#self.response.write('"list":"%s",'%j) # a counter for debugging so I can check the index
			#This inner for loop iterates through the key/value pair tuples with the key always at the '[0]' index and the value at '[1]'
	 		for i in range(1, len(sensor_vals)):
				json_output.write('"%s":'%(sensor_vals[i][0]))
				json_output.write('"%s"'%(sensor_vals[i][1]))
				# all the key / value pairs in the list are seperated by a comma. The following if statement prevents a ',' from being output after the last item in the list
				if i < (len(sensor_vals)-1):
					json_output.write(',')
				# Once the end of the list has been reached however, a closing bracket is needed. The following if statement does this
				if i ==(len(sensor_vals)-1):
					json_output.write('}')
				# Same 'no comma at end of list' check as the first one. This one being for seperating the sets of readings. 
			if j <(len(device_records)-1):
					json_output.write(',')
			j+=1
		json_output.write(']}}')

			
			
		return json_output.getvalue()
		#After the output is returned to the function it is discarded from memory when the .close() method is called. 
		json_output.close() 

	@classmethod
	def parse_out_latest_device_timestamp(cls,device_name):
		#get the latest device record
		device_record = SensorRecord.query_readings_by_device(device_name,1)
		#json.load(device_record)
		# return only the datetime value
		json_output = json.loads(device_record)
		# Traversing the JSON:
		# json_output['readings'] returns a list, which is denoted by '[]'
		# [{u'datetime': u'2014-03-29 23:18:31.484465', u'a1': u'332', u'a0': u'221', u'a3': u'554', u'a2': u'443', u'a5': u'776', u'a4': u'665'}] (ignore the 'u' it is noting that the string is 'unicode')
		# json_output['readings'][0] <--- this second index of [0] traverses past the list and into the JSON object '{}' that are wrapping the node being targeted
		
		# now the node value can be accessed via key name ['datetime']. It will be returned as a unicode string. 
		# Next datetime's '.strptime()' method is called, passing the record's datetime value as the first arguement. The second arguement passes the syntax for parsing.  
		# more information about datetime can be found here: http://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
		
		return datetime.strptime(json_output['collection']['items'][0]['datetime'],'%Y-%m-%d %H:%M:%S.%f').strftime("%a,%b,%d,%H,%M,%S")
		

>>>>>>> 99c82602099b569a8f70d35b6a3a3183587c6395

class MainHandler(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write('hello world')

class CreateRecordHandler(webapp2.RequestHandler):
    
    def get(self):

<<<<<<< HEAD
    	
=======
    	self.response.headers['Access-Control-Allow-Origin'] = '*'
>>>>>>> 99c82602099b569a8f70d35b6a3a3183587c6395
    	# populates datastore Model Objects with GET Params and creates Datastore Entity
        self.response.headers['Content-Type'] = 'text/plain'
        #the following request objects are used to collect the arguments from the Query string (everything after the '?')
        device_name = self.request.GET['devicename']
        
        r = SensorRecord(parent = device_key(device_name),
<<<<<<< HEAD
        				sensorreading = json.dumps(self.request.GET.items(), separators=(',', ':'), indent = 2 ))
=======
        				sensorreading = json.dumps(self.request.GET.items(), separators=(',', ':')))
>>>>>>> 99c82602099b569a8f70d35b6a3a3183587c6395
        				
        r_key = r.put()



<<<<<<< HEAD
class ReadRecordsHandler(webapp2.RequestHandler):

	def get(self): 
		this = self
		this.response.headers['Content-Type'] = 'text/plain'
=======
class ReadSensorRecordsHandler(webapp2.RequestHandler):

	#This handler returns all of the records for the device name submitted via the GET query parameter 'devicename'
	#The nested for loops in this handler format the returned datastore entities into a JSON object. 

	def get(self): 
		this = self
		this.response.headers['Content-Type'] = 'application/json'
		self.response.headers['Access-Control-Allow-Origin'] = '*'
>>>>>>> 99c82602099b569a8f70d35b6a3a3183587c6395
		
		try:
			device_name= self.request.GET['devicename']

		except KeyError: #bail if there is no argument for 'devicename' submitted
<<<<<<< HEAD
			self.response.write ('NO DEVICE PARAMETER SUBMITTED')
		else:
			self.response.write(
			SensorRecord.query_readings_by_device(device_name))

class ReadRecordsHandlerWithTime(webapp2.RequestHandler):

	def get(self): 
		this = self
		this.response.headers['Content-Type'] = 'text/plain'
=======
			self.response.write ('NO DEVICE_NAME PARAMETER SUBMITTED')
			
		else:
			device_readings = SensorRecord.query_readings_by_device(device_name)

			self.response.write(device_readings)



class ReadLatestRecordHandler(webapp2.RequestHandler):

	def get(self): 
		this = self
		this.response.headers['Content-Type'] = 'application/json'
		self.response.headers['Access-Control-Allow-Origin'] = '*'
>>>>>>> 99c82602099b569a8f70d35b6a3a3183587c6395
		
		try:
			device_name= self.request.GET['devicename']

<<<<<<< HEAD
		except KeyError: #bail if there is no argument for 'devicename' submitted
			self.response.write ('NO DEVICE PARAMETER SUBMITTED')
		else:
			self.response.write(
			SensorRecord.query_readings_by_device_with_timestamp(device_name))

class ReadLatestRecordHandler(webapp2.RequestHandler):

	def get(self): 
		this = self
		this.response.headers['Content-Type'] = 'text/plain'
=======
		#bail if there is no argument for 'devicename' submitted
		except KeyError: 
			self.response.write ('NO DEVICE PARAMETER SUBMITTED')
		else:
			# pass the number of records to be returned via the second argument.
			device_reading =  SensorRecord.query_readings_by_device(device_name,1)
			self.response.write(device_reading)

		
class ReturnLatestRecordTime(webapp2.RequestHandler):

	def get(self): 
		this = self
		this.response.headers['Content-Type'] = 'application/json'
		self.response.headers['Access-Control-Allow-Origin'] = '*'
>>>>>>> 99c82602099b569a8f70d35b6a3a3183587c6395
		
		try:
			device_name= self.request.GET['devicename']

<<<<<<< HEAD
		except KeyError: #bail if there is no argument for 'devicename' submitted
			self.response.write ('NO DEVICE PARAMETER SUBMITTED')
		else:

			reading = SensorRecord.query_latest_reading(device_name)
			decoded_dict = dict(json.loads(reading))

			#self.response.write(decoded_dict.get('devicename') + '\n')
			#self.response.write(decoded_dict.get('a0'))

			self.response.write(decoded_dict) #outputs key value dictionary of retrieved datastore entity. 
=======
		#bail if there is no argument for 'devicename' submitted
		except KeyError: 
			self.response.write ('NO DEVICE PARAMETER SUBMITTED')
		else:
			device_reading =  SensorRecord.query_readings_by_device(device_name,1)
			self.response.write(
			SensorRecord.parse_out_latest_device_timestamp(device_name))

>>>>>>> 99c82602099b569a8f70d35b6a3a3183587c6395

class PassSensorValueOnly(webapp2.RequestHandler):

	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'

		try:
			device_name= self.request.GET['devicename']

		except KeyError: #bail if there is no argument for 'devicename' submitted
			self.response.write ('NO DEVICE PARAMETER SUBMITTED')
		else:
			reading = SensorRecord.query_latest_reading(device_name)
			decoded_dict = dict(json.loads(reading))
			self.response.write(decoded_dict.get('a0'))


app = webapp2.WSGIApplication([
	webapp2.Route('/', handler = MainHandler, name = 'home'),
	webapp2.Route('/write', handler =  CreateRecordHandler, name = 'create-record'),
<<<<<<< HEAD
	webapp2.Route('/read', handler = ReadRecordsHandler, name = 'read-values'),
	webapp2.Route('/read-time', handler = ReadRecordsHandlerWithTime, name = 'read-values-with-time'),
	webapp2.Route('/read-latest', handler = ReadLatestRecordHandler, name = 'read-latest-value'),
	webapp2.Route('/a0', handler = PassSensorValueOnly, name = 'pass-sensor-value-a0')
=======
	webapp2.Route('/read', handler = ReadSensorRecordsHandler, name = 'read-values'),
	webapp2.Route('/read-latest', handler = ReadLatestRecordHandler, name = 'read-latest-record'),
	webapp2.Route('/read-time', handler = ReturnLatestRecordTime, name = 'read-latest-record-time'),
	webapp2.Route('/read-sensor-value', handler = PassSensorValueOnly, name = 'pass-sensor-value-a0')
>>>>>>> 99c82602099b569a8f70d35b6a3a3183587c6395

], debug=True)


 