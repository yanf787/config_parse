#!/usr/bin/python3
from ocnos_config import ocnos_config
from junos_config import junos_config
from eos_config import eos_config

from optparse import OptionParser



if __name__ == '__main__':
	parser = OptionParser()
	parser.add_option("-f", "--file", dest="config_file", default="", help="Path to config file")
	(options, args) = parser.parse_args()
	config_file = options.config_file


	#print (config_file)
	#new_ocnos_config = ocnos_config(config_file)

	#print(new_ocnos_config.config_dict)

	#new_ocnos_config.regenerate_config()

	#print(new_ocnos_config.regenerated_config)



	new_junos_config = junos_config(config_file)

	print(new_junos_config.config_dict)


	new_junos_config.regenerate_config()

	print(new_junos_config.regenerated_config)


