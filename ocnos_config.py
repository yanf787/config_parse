from aux_functions import ios_style_list_into_dictionary
import pyparsing as pp
from collections import OrderedDict
import os
import sys
import re
import itertools
sys.setrecursionlimit(10000) 


class ocnos_config:



	def __init__(self, config_file):
		ocnos_config_statement = pp.Forward()
		ocnos_comment = pp.Regex('(\\!)(.*)')
		ocnos_config_line_comment = pp.Regex('(\\!)(.*)(\\;\\;\\;)')
		ocnos_config_line = pp.Regex('(\\w)(.*)(\\;\\;\\;)')
		ocnos_header_line = pp.Regex('(\\w)(.*)(\\:\\:\\:)') 
		ocnos_config_statement <<= (pp.Group(ocnos_config_line | ocnos_config_line_comment | pp.Group(ocnos_header_line + pp.IndentedBlock(ocnos_config_statement))))
		ocnos_config = pp.OneOrMore(ocnos_comment | ocnos_config_statement)
		self.config_dict = {}
		self.list_config = []
		self.regenerated_config = ''
		if os.path.isfile(config_file):
			try:
				with open(config_file, 'r') as file:
					contents = file.read()
					#print (contents)
					
					
			except Exception as e:
				print(f"Error opening {config_file}: {e}")

		config_preprocessed = re.sub('(\n)+',"\n",contents)
		config_preprocessed = re.sub('(\\!)+',"!",config_preprocessed)
		split_contents = contents.split("\n")
		#pprint.pprint (entity_lines)
		new_config_file = self._prepare_ocnos_config(split_contents)
		tokens = ocnos_config.parse_string(new_config_file).as_list()
		#print (tokens)
		config_groups = OrderedDict()
		new_parse_tree = {}
		dict_index = ''

		self.config_dict = ios_style_list_into_dictionary(OrderedDict(), tokens)





	def regenerate_config(self):
		self.list_config = self.ocnos_dictionary_print(self.config_dict, '', 0, [])
		self.regenerated_config = "\n".join(self.list_config)



	def _prepare_ocnos_config(self, entity_lines):
		#print(entity_lines)
		counter = 0
		previous_indent_counter = 1
		comment_flag = 0
		new_config_file_list = []
		#print ("---------")
		address_family_flag = 0
		new_entity_lines = []
		for line in entity_lines:
			line_list = line.split(" ")
			#print(line_list, address_family_flag)
			if ('address-family' in line_list):
				af_line = 1
				address_family_flag = 1
				new_entity_lines.append(line)

			elif ('exit-address-family' in line_list and address_family_flag == 1):
				address_family_flag = 0
				new_entity_lines.append(" " + line)

			elif(address_family_flag == 1):
				new_entity_lines.append(" " + line)

			else:
				new_entity_lines.append(line)

		for line in new_entity_lines:
		
			#print(line)
			full_line = line.split(" ")
			#print (full_line)
			#print (len(full_line), full_line[-1], comment_flag)
			whitespaces = sum(1 for _ in itertools.takewhile(str.isspace, line))
			#print (len(full_line), full_line[-1], comment_flag, whitespaces)
			line_list = full_line
			#print(line_list)
			indent_counter = whitespaces
			if (line_list[0] == "!"):
				new_config_file = new_config_file_list.append(" " * (indent_counter - 1) * 3 + " ".join(full_line))
				if (comment_flag == 2):
					new_config_file_list[counter-1] = new_config_file_list[counter-1] + " ;;;"
				previous_indent_counter = indent_counter
				counter = counter + 1
				comment_flag = 1
				continue
			

			#if(line_list[1] =='address-family'):
			#	#print (line_list)
			#	new_config_file = new_config_file_list.append(" " * (indent_counter - 1) * 3 + full_line[-1])
			#	new_config_file_list[counter-1] = new_config_file_list[counter-1] + " :::"

			if(indent_counter > previous_indent_counter):
				new_config_file = new_config_file_list.append(" " * (indent_counter - 1) * 3 + " ".join(full_line))
				new_config_file_list[counter-1] = new_config_file_list[counter-1] + " :::"
			if (indent_counter <= previous_indent_counter):
				new_config_file = new_config_file_list.append(" " * (indent_counter - 1) * 3 + " ".join(full_line))
				if (comment_flag == 2):
					new_config_file_list[counter-1] = new_config_file_list[counter-1] + " ;;;"
			previous_indent_counter = indent_counter
			counter = counter + 1
			comment_flag = 2
		new_config_file_list[counter - 1] = new_config_file_list[counter - 1] + " ;;;"
		#for line in new_config_file_list:
		new_config_file = "\n".join(new_config_file_list)
		return (new_config_file)	

	def ocnos_dictionary_print(self, start_dict, running_string, indent_level, regen_config_list):
		for key in start_dict.keys():
			if len(start_dict[key].keys()) == 0:
				regen_config_list.append("  " * indent_level + running_string + " " + key)
				#print("  " * indent_level + running_string + " " + key)
				dummy = 0
			elif len(start_dict[key].keys()) >= 1 and isinstance(start_dict[key], dict) and not(isinstance(start_dict[key], OrderedDict)):
				#print ("here")
				self.ocnos_dictionary_print(start_dict[key], running_string + " " + key, indent_level, regen_config_list)
			elif len(start_dict[key].keys()) >= 1 and isinstance(start_dict[key], OrderedDict):
				#print ("here")
				#print ("    " * indent_level + running_string + " " + key)
				regen_config_list.append(" !")
				regen_config_list.append("    " * indent_level + running_string + " " + key) 
				self.ocnos_dictionary_print(start_dict[key], '', indent_level + 1, regen_config_list)
		return(regen_config_list)




