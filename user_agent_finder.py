import xml.etree.ElementTree as ET
from random import choice


global header_list
header_list = []
bad_list = ['Googlebot', 'bingbot', 'Yahoo!', 'WiiU', 'Nintendo', 'PlayStation', 'bot', 'http']


def get_user_agents():
	tree = ET.parse('useragents.xml')
	root = tree.getroot()

	for child in root:
		# print(child.tag, child.attrib)
		for child2 in child:
			# print(child2.attrib)
			for child3 in child2:
				try:
					user_agent = child3.attrib.get('useragent')
					if not any(word in user_agent for word in bad_list):
						# print(user_agent)
						header_list.append({'User-Agent': user_agent})
				except Exception as e:
					# print(e)
					pass
	return header_list


def random_header():
	get_user_agents()
	return choice(header_list)
