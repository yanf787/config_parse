from aux_functions import ios_style_list_into_dictionary
import pyparsing as pp
from collections import OrderedDict
from mergedeep import merge, Strategy
import os
import sys
import re
import itertools
import pprint
sys.setrecursionlimit(10000) 


class junos_config:



	def __init__(self, config_file):
		junos_symbols = "=:/.-_*$"
		#junos_value = pp.dblQuotedString() |  pp.Word(pp.alphas + pp.nums + junos_symbols)
		junos_value = pp.QuotedString('"', multiline = True, convert_whitespace_escapes = True, unquoteResults=False) | pp.Word(pp.alphas + pp.nums + junos_symbols) 
		junos_quoted_value = pp.QuotedString('"', escQuote='\'')
		junos_comment = pp.Group(pp.pythonStyleComment)
		junos_multi_value = pp.Group('[' + pp.ZeroOrMore(junos_value) + "]")
		junos_statement = (pp.Group(pp.OneOrMore(junos_value) + pp.Optional(junos_multi_value)) + pp.Suppress(";") + pp.Optional(junos_comment)) | pp.Group(pp.cStyleComment)
		junos_block_name_part = pp.Word(pp.alphas + pp.nums + "-_.*/:<>$" )
		junos_block_name = pp.Group(pp.OneOrMore(junos_block_name_part))
		junos_block = pp.Forward()
		#junos_block <<= pp.Group(pp.OneOrMore(junos_block_name + pp.Suppress("{") + pp.Group(pp.OneOrMore(junos_statement | junos_block))+ pp.Suppress("}"))) + pp.Optional(junos_comment)
		junos_oci_style_comment = pp.Regex('(\#\#)(.*)')
		#junos_block <<= pp.Group(junos_block_name + pp.Suppress("{") + pp.OneOrMore(junos_statement | junos_block)+ pp.Suppress("}")) + pp.Optional(junos_comment)
		junos_config = pp.ZeroOrMore(pp.Group(pp.cStyleComment) | pp.Group(pp.pythonStyleComment) | junos_block | junos_statement)
		junos_block <<= pp.Group(junos_block_name + pp.Suppress("{") + pp.Group(junos_config)+ pp.Suppress("}"))
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

		
		#split_contents = contents.split("\n")
		#pprint.pprint (entity_lines)
		
		#pprint.pprint (split_contents)
		tokens = junos_config.parse_string(contents).as_list()
		
		#print (tokens)
		config_groups = OrderedDict()
		new_parse_tree = {}
		dict_index = ''

		self.config_dict = self._list_into_dictionary_junos(tokens, 1)

	def regenerate_config(self):
		self.list_config = self.junos_dictionary_print(self.config_dict, 0, [])
		self.regenerated_config = "\n".join(self.list_config)

	def _list_into_dictionary_junos(self, list_of_lists, comment_counter):
		#print ("Entrance")
		#pprint.pprint(temp_list)
		#pprint.pprint(list_of_lists)
		current_dict = OrderedDict()
		
	 
		occurence_count = {}
		temp_unused_list = []
		temp_list = OrderedDict()
		for list_part in list_of_lists:

			if (not(isinstance(list_part[0], list))):
					if (not(list_part[0] in occurence_count.keys())):
						occurence_count[list_part[0]] = 1
					else:
						occurence_count[list_part[0]] += 1

		#print (occurence_count)

	 
	 
		#exit()
		#for list_part in list_of_lists:
		#	print (list_part[0])
		for list_part in list_of_lists:
			#print (list_part)
			#if (not(isinstance(list_part, list))):
			#	current_dict [list_part] = {}
			#elif isinstance(list_part, list) and 
			if (not(isinstance(list_part[0], list))):
					#print ("Another part", list_part)
					if (list_part[0][0] == "#"):
						#print ("Comment", list_part)
						current_dict["comment" + str(comment_counter)] = list_part
						comment_counter = comment_counter + 1
					elif (list_part[0][0] == "/") and (list_part[0][1] == "*"):
						#print ("Comment", list_part)
						current_dict["comment" + str(comment_counter)] = list_part
						comment_counter = comment_counter + 1
					else:
						#print (type(current_dict))
						#print ("In Else", list_part)
						if (len(list_part) == 2):
							#print ("2")
							#if (list_part[0] in current_dict.keys()):
							#	current_dict[list_part[0] + " " + list_part[1]] = {}
							#else:
							#print (list_part, list_of_lists)
							if (occurence_count[list_part[0]] == 1):
								current_dict[list_part[0]] = list_part[1]
							else:
								current_dict[list_part[0] + " " + list_part[1]] = ''
							#return (current_dict)
						elif(len(list_part) == 1):
							#print ("1")
							current_dict [list_part[0]] = ''
							#return (current_dict)
						#elif (len(list_part) > 3):
						#	#print (list_part, list_part[2:])
						#	current_dict[(list_part[0], list_part[1])]	= list_into_dictionary_junos5(OrderedDict(), list_part[2:], 0)
						elif (len(list_part) > 2):
							#print ("Complete Else", list_part)
						#	current_dict[(list_part[0], list_part[1])] = list_part[2]
							#current_dict[list_part[0]] = {}
							#current_dict[list_part[0]][list_part[1]] = list_part[2]
							last_member_list = 0
							current_dict_index = []
							for small_list_part in list_part:
								#print (small_list_part)
								if (not(isinstance(small_list_part, list))):
									current_dict_index.append(small_list_part)
								else:
									current_dict_index.append(' '.join(small_list_part))
								
							#current_dict_index.append(str(small_list_part))
							current_dict[tuple(current_dict_index)] = ''
			


			else:

				if (len(list_part[0]) == 1):
					#print("List part 1", list_part[0], "----", list_part[0][0])
					#pprint.pprint (list_part[1:])
					for list_subpart in list_part[1:]:
						#print (list_subpart)
						if (not(list_part[0][0] in current_dict.keys())):
							current_dict[list_part[0][0]] = self._list_into_dictionary_junos(list_subpart, comment_counter)
						else:
							current_dict[list_part[0][0]] = merge(current_dict[list_part[0][0]], self._list_into_dictionary_junos(list_subpart, comment_counter), strategy=Strategy.ADDITIVE)
 
				else:
					for list_subpart in list_part[1:]:
						if (not(tuple(list_part[0]) in current_dict.keys())):
							current_dict[tuple(list_part[0])] = self._list_into_dictionary_junos(list_subpart, comment_counter)
						else:
							current_dict[tuple(list_part[0])] = merge(current_dict[tuple(list_part[0])], self._list_into_dictionary_junos(list_subpart, comment_counter), strategy=Strategy.ADDITIVE)
 							

		return(current_dict)


	def junos_dictionary_print(self, start_dict, indent_level, regen_config_list):
		#print (start_dict)
		for key in start_dict.keys():
			if (not(isinstance(key, tuple))):
				if re.match("comment", key):
	
					regen_config_list.append("   " * indent_level + start_dict[key][0])
				else:
					if isinstance(start_dict[key], OrderedDict):
						if (len(start_dict[key]) == 0):
							regen_config_list.append("   " * indent_level + " " + key + ";")
						else:
							regen_config_list.append("   " * indent_level + " " + key +  " {")
							regen_config_list = regen_config_list + self.junos_dictionary_print(start_dict[key], indent_level + 1, [])
							regen_config_list.append("   " * (indent_level + 1) + "}")
					else:
						if (not(isinstance(start_dict[key], list))):
							regen_config_list.append("   " * indent_level + " " + key + " " + start_dict[key] + ";")
						else:
					    
							if (len(start_dict[key]) == 1):
								regen_config_list.append("   " * indent_level + " " + key + " " + " ".join(str(config_part) for config_part in start_dict[key]) + ";")
							else:
								if (isinstance(start_dict[key][1], list)):
									regen_config_list.append("   " * indent_level + " " + key + " " + start_dict[key][0] + " " + " ".join(str(config_part) for config_part in start_dict[key][1]) + ";")
								else:
									regen_config_list.append("   " * indent_level + " " + key + " " + " ".join(str(config_part) for config_part in start_dict[key]) + ";")
			else:
				if isinstance(start_dict[key], OrderedDict):
					if (len(start_dict[key]) == 0):
						regen_config_list.append("   " * indent_level +  " ".join(key) + ";")
					else:

						regen_config_list.append("   " * indent_level + " " + " ".join(key) + " {")
						regen_config_list = regen_config_list + self.junos_dictionary_print(start_dict[key], indent_level + 1, [])
						regen_config_list.append("   " * (indent_level + 1) + "}")
				else:
					if (not(start_dict[key])):
						regen_config_list.append("   " * indent_level + " ".join(key) + ";")
		return(regen_config_list)

