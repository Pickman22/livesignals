#!/usr/bin/python

import logging, copy, time

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

_BASE_BODY = {
	'measurement': ' ',
	'tags': {},
	'time': ' ',
	'fields': {}
}

def get_message(fields, name, dtime, tags = None):
	'''Returns a dict to upload data to InfluxDB.
	fields data to be logged.
	@name name of the measurement.
	@dtime date of measurement.
	@tags extra info such as host or region.
	'''
	body  = copy.deepcopy(_BASE_BODY)
	body['time'] = dtime#time.asctime(time.localtime(dtime))
	body['measurement'] = name
	for k, v in fields.iteritems():
		if k != 'time': # time is already set at this point.
			body['fields'][k] = v
	if tags is not None:
		for k, v in tags.iteritems():
			if k != 'time': # same as before.
				body['tags'][k] = v
	logger.debug('Setting message: {}'.format(body))
	return body

if __name__ == '__main__':
	fields = {'temperature': 33.2, 'pressure': 1.02, 'humidity': 80.2}
	tags = {'location': 'Ensenada', 'host': 'local'}
	now = time.asctime(time.localtime(time.time()))
	print('{}'.format('*' * 80))
	print('This is an example message to update an InfluxDB: {}'.format(get_message(fields, 'weather', now, tags)))
	print('{}'.format('*' * 80))