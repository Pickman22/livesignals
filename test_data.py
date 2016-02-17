#! /usr/bin/python

import message, sys, time, random, pylab, influxdb, logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

def generate_data(days, dt_minutes):
	dt = dt_minutes * 60 # Data every 10 minutes.
	days_minutes = days * 24 * 60 # Ten days worth of data.
	base_temp = 30.0 # degrees
	base_pressure = 1.01 # atmospheres.
	base_humidity = 83.2 # relative.
	total_seconds = days_minutes * 60
	now = time.time()
	data = {'temperature': 0., 'pressure': 0., 'humidity': 0.}
	#secs = range(0, total_seconds, dt)
	for t in xrange(0, total_seconds, dt):
		_time = now - t
		data['temperature'] = base_temp + random.random()\
			+ 7.0 * pylab.sin(2 * pylab.pi  * _time / (24.0 * 60 * 60))
		data['pressure'] = base_pressure + random.random() * 0.1 - 0.5 
		data['humidity'] = base_humidity + random.random() * 13.0 - 5.0
		yield data, time.asctime(time.localtime(_time))


def main():
	days_data = 10 # 10 days of data.
	minutes_data = 10 # Generate data every 10 minutes.
	db_name = 'test'
	try:
		db_name = sys.argv[1]
		logger.debug('Database name {} provided')
	except:
		logger.debug('No database name provided. Using "test"')
	tags = {'region': 'Ensenada', 'host': 'localhost'}
	db = influxdb.InfluxDBClient('localhost', 8086, 'root', 'root')
	all_dbs_list = db.get_list_database()
	if db_name not in [str(x['name']) for x in all_dbs_list]:
		logger.warn('Database does not exist. Creating database {0}'.format(db_name))
		db.create_database(db_name)
	else:
		logger.info('Reusing database {0}'.format(db_name))
	db.switch_database(db_name)
	print('Generating {} days worth of data. Data is commited every {} minutes.'.format(days_data, minutes_data))
	print('Updating database with data. This could take a while. Please wait...')
	for fields, t in generate_data(10, 10):
		data = [message.get_message(fields, 'weather', t, tags)]
		if db.write_points(data):
			logger.debug('Writing {}'.format(data))
		else:
			logger.debug('Operation failed.')
	print('Update is done.')
	print('Check results in database {} with the following query: '.format(db_name))
	print('SELECT * FROM "weather"')

if __name__ == '__main__':
	main()