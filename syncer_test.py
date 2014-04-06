#!/usr/bin/env python

from syncer import Syncer 

class Photo(object):
	def __init__(self, dict):
		self.__dict__.update(dict)

class Tests():

	def test_date_path_zero_pads_months(self):
		testee = Syncer("/storage")
		photo = Photo({
			"dateTakenYear" : "2014",
			"dateTakenMonth" : "4",
			"dateTakenDay" : "16",
			"filenameOriginal" : "monkey.png" })
		path = testee._getDatePathTo(photo)
		assert "/storage/date/2014/04/16/monkey.png" == path


	def test_date_path_zero_pads_days(self):
		testee = Syncer("/storage")
		photo = Photo({
			"dateTakenYear" : "2014",
			"dateTakenMonth" : "12",
			"dateTakenDay" : "6",
			"filenameOriginal" : "monkey.png" })
		path = testee._getDatePathTo(photo)
		assert "/storage/date/2014/12/06/monkey.png" == path
