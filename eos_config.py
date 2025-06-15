from aux_functions import ios_style_list_into_dictionary
import pyparsing as pp
from collections import OrderedDict
import os
import sys
import re
import itertools
sys.setrecursionlimit(10000) 


class eos_config:



	def __init__(self, config_file):
		eos_config_statement = Forward()

		eos_comment = pp.Regex('(\!)(.*)')
		eos_config_line_comment = pp.Regex('(\!)(.*)(\;\;\;)')
		eos_config_line = pp.Regex('(\w)(.*)(\;\;\;)')
		eos_header_line = pp.Regex('(\w)(.*)(\:\:\:)') 
		eos_config_statement <<= (pp.Group(eos_config_line | eos_config_line_comment | Group(eos_header_line + pp.IndentedBlock(eos_config_statement))))
		eos_config = pp.OneOrMore(eos_comment | eos_config_statement)
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
		new_config_file = self._prepare_eos_config(split_contents)
		tokens = eos_config.parse_string(new_config_file).as_list()
		#print (tokens)
		config_groups = OrderedDict()
		new_parse_tree = {}
		dict_index = ''

		self.config_dict = ios_style_list_into_dictionary(OrderedDict(), tokens)


	def prepare_ios_style_config(entity_lines):
		counter = 0
		previous_indent_counter = 1
		comment_flag = 0
		new_config_file_list = []
		#print ("---------")
		for line in entity_lines:
			full_line = line.split("   ")
			#print (len(full_line), full_line[-1], comment_flag)
			line_list = full_line[-1].split(" ")
			indent_counter = len(full_line)
			if (line_list[0] == "!"):
				new_config_file = new_config_file_list.append(" " * (indent_counter - 1) * 3 + full_line[-1])
				if (comment_flag == 2):
					new_config_file_list[counter-1] = new_config_file_list[counter-1] + " ;;;"
				previous_indent_counter = indent_counter
				counter = counter + 1
				comment_flag = 1
				continue
			if(indent_counter > previous_indent_counter):
				new_config_file = new_config_file_list.append(" " * (indent_counter - 1) * 3 + full_line[-1])
				new_config_file_list[counter-1] = new_config_file_list[counter-1] + " :::"
			if (indent_counter <= previous_indent_counter):
				new_config_file = new_config_file_list.append(" " * (indent_counter - 1) * 3 + full_line[-1])
				if (comment_flag == 2):
					new_config_file_list[counter-1] = new_config_file_list[counter-1] + " ;;;"
			previous_indent_counter = indent_counter
			counter = counter + 1
			comment_flag = 2
		new_config_file_list[counter - 1] = new_config_file_list[counter - 1] + " ;;;"
		#for line in new_config_file_list:
		new_config_file = "\n".join(new_config_file_list)
		return (new_config_file)	



	def regenerate_config(self):
		self.list_config = self.eos_dictionary_print(self.config_dict, '', 0, [])
		self.regenerated_config = "\n".join(self.list_config)


	def eos_dictionary_print(self, start_dict, running_string, indent_level, regen_config_list):
		for key in start_dict.keys():
			if len(start_dict[key].keys()) == 0:
				regen_config_list.append("  " * indent_level + running_string + " " + key)
				#print("  " * indent_level + running_string + " " + key)
				dummy = 0
			elif len(start_dict[key].keys()) >= 1 and isinstance(start_dict[key], dict) and not(isinstance(start_dict[key], OrderedDict)):
				#print ("here")
				self.eos_dictionary_print(start_dict[key], running_string + " " + key, indent_level, regen_config_list)
			elif len(start_dict[key].keys()) >= 1 and isinstance(start_dict[key], OrderedDict):
				#print ("here")
				#print ("    " * indent_level + running_string + " " + key)

				regen_config_list.append("    " * indent_level + running_string + " " + key) 
				self.eos_dictionary_print(start_dict[key], '', indent_level + 1, regen_config_list)
		return(regen_config_list)