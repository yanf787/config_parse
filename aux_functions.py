from collections import OrderedDict

def ios_style_list_into_dictionary(current_dict, list_of_lists):
	#print ("Enter Function")
	for list_part in list_of_lists:
		

		active_dict = current_dict
		if list_part[0] == "!":
			current_dict[list_part] = {}
			continue
		
		if (not(isinstance(list_part[0], list))):
			for part_list_part in list_part[0].split(" ")[:-1]:
				#print ("List part", part_list_part)
				if (part_list_part in active_dict.keys()):
					#print (active_dict[part_list_part])
					if (active_dict[part_list_part] == {}):
						#print ("Empty dictionary")
						active_dict = active_dict[part_list_part]
						active_dict[' '] = {} 
					else:
						active_dict = active_dict[part_list_part]
					#print (active_dict)
				else:
					#print ("In else")
					active_dict[part_list_part] = {}
					active_dict = active_dict[part_list_part]
			#print (current_dict, active_dict)
		elif (isinstance(list_part[0], list)):
			new_list_part = list_part[0][0].split(" ")[:-1]
			#print (list_part[0][0], list_part[0][1])
			for index, part_list_part in enumerate(new_list_part):
				if (part_list_part in active_dict.keys()):
					active_dict = active_dict[part_list_part]

				else:
					if (index == len(new_list_part) - 1):
						active_dict[part_list_part] = ios_style_list_into_dictionary(OrderedDict(), list_part[0][1])
						active_dict = active_dict[part_list_part]
					else:
						active_dict[part_list_part] = {}
						active_dict = active_dict[part_list_part]
				#print (index, part_list_part, len(new_list_part))
			#print (previous_active_dict)



	#print ("About to return", current_dict)
	return(current_dict)