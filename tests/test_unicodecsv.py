#This test validates different types of data(bytes,unicode,string) in python2 and python3 using a sample csv file and
#checking for corresponding key-value pair in different data types. 

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import unittest

import csv
import sys


class TestUnicodeCsv(unittest.TestCase):

	def test_unicode(self):
		dct=dict()
		with open('data/sample.csv', 'r') as file_in:
			reader = csv.DictReader(file_in)
			for entry in reader:
				assert entry["License Identifier"] == "Glide"
				assert entry[u"License Identifier"] == u"Glide"
				if sys.version_info[0] < 3:
					assert entry[b"License Identifier"] == b"Glide"
				else :
					assert not b"License Identifier" in entry
if __name__ == '__main__':
	unittest.main()

