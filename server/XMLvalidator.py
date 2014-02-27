from lxml import etree
from hashlib import sha384
import xml.etree.ElementTree as ET

version = '0.0.1'

class XMLValidate(object):

	@staticmethod
	def validate(xml):

		# check that the version number is correct
		if xml.find('version').text != version:
			return 0

		# check that the checksum is correct
		checksum = xml.find('checksum')
		xml.remove(checksum)
		without_checksum = ET.tostring(xml)
		checksum_validate = sha384(without_checksum).hexdigest()
		valid = checksum.text == checksum_validate

		return valid