
import urllib
import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb

NO_DEVICE_NAMED = 'no_device_name'

def device_key(device_name = NO_DEVICE_NAMED):
	"""constructs Datastore key for SensorRecord entity with device_name """
	return ndb.Key('DeviceGroup', device_name)


class SensorRecord(ndb.Model) :
	"""Models a single PinRead from an Arduino with record creation time,  sensor min/max, and Device name"""
	sensormin = ndb.IntegerProperty()
	sensormax = ndb.IntegerProperty()
	sensorreading = ndb.IntegerProperty()
	recordentrytime = ndb.DateTimeProperty(auto_now_add=True)

	#note: all class methods pass the instance of the class as it's first argument 
	@classmethod
	def query_readings_by_device(cls,device_name):
			device_readings_list = []
			device_records_query = cls.query(
			ancestor = device_key(device_name)).order(-SensorRecord.recordentrytime)
			# device_records is a list object only returns sensor reading and time for parsing. 
			device_records = device_records_query.fetch( projection=[cls.sensorreading, cls.recordentrytime])

		#create methods for pulling different streams of data out for processing. 
			for device_record in device_records:
				device_readings_list.append(device_record.sensorreading)
			return device_readings_list

	@classmethod
	def query_readings_by_device_with_timestamp(cls,device_name):
			device_readings_dict = {}
			device_records_query = cls.query(
			ancestor = device_key(device_name)).order(-SensorRecord.recordentrytime)
			
			device_records = device_records_query.fetch( projection=[cls.sensorreading, cls.recordentrytime])

			for device_record in device_records:
				if not cls.sensorreading in device_readings_dict:
					device_readings_dict[device_record.recordentrytime] = device_record.sensorreading
				else:
					device_readings_dict[device_record.recordentrytime].append(device_record.sensorreading)	
			return device_readings_dict

	@classmethod
	def query_latest_reading(cls,device_name):
		
		device_records_query = cls.query(
			ancestor = device_key(device_name)).order(-SensorRecord.recordentrytime)
			# device_records is a list object only returns sensor reading and time for parsing. 
		device_record = device_records_query.fetch(1, projection=[cls.sensorreading, cls.recordentrytime])
		return device_record[0].sensorreading

class MainHandler(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write('hello world')

class CreateRecordHandler(webapp2.RequestHandler):
    
    def get(self):
    	# populates datastore Model Objects with GET Params and creates Datastore Entity
        self.response.headers['Content-Type'] = 'text/plain'

        device_name = self.request.GET['devicename']


        r = SensorRecord(parent = device_key(device_name),
        				sensorreading = int(self.request.GET['sensorreading']),
        				sensormin = int(self.request.GET['sensormin']),
        				sensormax = int(self.request.GET['sensormax']))
        r_key= r.put()



class ReadRecordsHandler(webapp2.RequestHandler):

	def get(self): 
		this = self
		this.response.headers['Content-Type'] = 'text/plain'
		
		try:
			device_name= self.request.GET['devicename']

		except KeyError: #bail if there is no argument for 'devicename' submitted
			self.response.write ('NO DEVICE PARAMETER SUBMITTED')
		else:
			self.response.write(
			SensorRecord.query_readings_by_device(device_name))

class ReadRecordsHandlerWithTime(webapp2.RequestHandler):

	def get(self): 
		this = self
		this.response.headers['Content-Type'] = 'text/plain'
		
		try:
			device_name= self.request.GET['devicename']

		except KeyError: #bail if there is no argument for 'devicename' submitted
			self.response.write ('NO DEVICE PARAMETER SUBMITTED')
		else:
			self.response.write(
			SensorRecord.query_readings_by_device_with_timestamp(device_name))

class ReadLatestRecordHandler(webapp2.RequestHandler):

	def get(self): 
		this = self
		this.response.headers['Content-Type'] = 'text/plain'
		
		try:
			device_name= self.request.GET['devicename']

		except KeyError: #bail if there is no argument for 'devicename' submitted
			self.response.write ('NO DEVICE PARAMETER SUBMITTED')
		else:
			self.response.write(
			SensorRecord.query_latest_reading(device_name))



app = webapp2.WSGIApplication([
	webapp2.Route('/', handler = MainHandler, name = 'home'),
	webapp2.Route('/write', handler =  CreateRecordHandler, name = 'create-record'),
	webapp2.Route('/read', handler = ReadRecordsHandler, name = 'read-values'),
	webapp2.Route('/read-time', handler = ReadRecordsHandlerWithTime, name = 'read-values-with-time'),
	webapp2.Route('/read-latest', handler = ReadLatestRecordHandler, name = 'read-latest-value')

], debug=True)


 