import sys, json


def set_Setting(elsetting, elvalue ='', filename='', verbose = 0):
	config = {'': ''}
	try:
		with open(filename, 'r+') as f:
			config = json.load(f)       
		#print("The current data is: ", config)
		if elsetting in config:
			if verbose == 1:
				print(f'The {elsetting!r} changed from {config[elsetting]!r} to {elvalue!r}')
			
			#edit the data
			config[elsetting] = elvalue
			#write it back to the file
			with open(filename, 'w') as f:
				json.dump(config, f)
		else:
			if verbose == 1:
				print(f'Key {elsetting!r} data is not available!!! Adding it')
			with open(filename, 'r+') as f:
				new_dict = ({elsetting: elvalue})
				config.update(new_dict)
				json.dump(config,f)
	except:
		if verbose == 1:
			print("Unexpected error:", sys.exc_info()[0])
		with open(filename, 'w') as f:
			json.dump(config, f)


def get_Setting(elsetting, filename='', verbose = 0):
	config = {'': ''}
	try:
		with open(filename, 'r+') as f:
			config = json.load(f)

		if elsetting in config:
			#returning the setting. 
			if verbose == 1:
				print(f'The {elsetting!r} is returning the value: {config[elsetting]!r}')
			return config[elsetting]
		else:
			return None
	except:
		print("Unexpected error:", sys.exc_info()[0])


    
