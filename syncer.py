#!/usr/bin/env python

#
# Syncs all images from a Trovebox account.
# Setup needed:
# * install Trovebox' Python lib
# * configure ~/.config/trovebox/default
# * modify paths in __init__ below (or improve script :-)
#

#
# Downloads all images, stored with their hash in ''storageDir''.
# A symlink is created in the "by date" folder, ''dateDir''.
# For each tag, a directory with that name is created in ''tagsDir'', with a symlink to the actual file.
# For each album, a directory with that name is created in ''albumsDir'', with a symlink to the actual file.
#

from trovebox import Trovebox
import os, re

class Syncer():
	def __init__(self):
		self.client = Trovebox()
		self._storageDir = '/home/ceda/trovebox/raw'
		self._dateDir = '/home/ceda/trovebox/date'
		self._tagsDir = '/home/ceda/trovebox/tags'
		self._albumsDir = '/home/ceda/trovebox/albums'

	def sync(self):
		# page is 1 based in the API
		page = 1
		while True:
			print "Syncing photos %s to %s (page %s)" % (100*page-100, 100*page, page)
			photos = self.client.photos.list(pageSize=100, page=page)
			if len(photos) > 0:
				for photo in photos:
					self._process(photo)
				page = page + 1
			else:
				print "All photos synced"
				return

	def _process(self, photo):
		print "Processing %s" % photo.filenameOriginal
		self._makeSureWeHaveTheRawImage(photo)
		self._makeSureWeHaveTheDateLinked(photo)
		self._makeSureWeHaveTheTagsLinked(photo)
		self._makeSureWeHaveTheAlbumsLinked(photo)

	def _makeSureWeHaveTheDateLinked(self, photo):
		source = self._getRawPathTo(photo)
		path = self._getDatePathTo(photo)
		self._makeSureWeHaveASymlinkFromTo(path, source)

	def _makeSureWeHaveTheAlbumsLinked(self, photo):
		source = self._getRawPathTo(photo)
		paths = self._getAlbumPathsTo(photo)
		for path in paths:
			self._makeSureWeHaveASymlinkFromTo(path, source)

	def _makeSureWeHaveTheTagsLinked(self, photo):
		source = self._getRawPathTo(photo)
		paths = self._getTagPathsTo(photo)
		for path in paths:
			self._makeSureWeHaveASymlinkFromTo(path, source)

	def _makeSureWeHaveTheRawImage(self, photo):
		file_name = self._getRawPathTo(photo)
		if os.path.exists(file_name):
			return
		self._downloadUrl(photo.pathOriginal, file_name)

	def _makeSureWeHaveASymlinkFromTo(self, path, source):
		if not os.path.exists(path):
			print "Symlinking source %s to %s" % (source, path)
			self._makeSureDirectoryExistsForFile(path)
			os.symlink(source, path)

	def _makeSureDirectoryExistsForFile(self, file_name):
		directory = os.path.dirname(file_name)
		if not os.path.isdir(directory):
			os.makedirs(directory)

	def _downloadUrl(self, url, file_name):
		self._makeSureDirectoryExistsForFile(file_name)
		import urllib2
		u = urllib2.urlopen(url)
		f = open(file_name, 'wb')
		meta = u.info()
		file_size = int(meta.getheaders("Content-Length")[0])
		print "Downloading: %s Bytes: %s" % (file_name, file_size)

		file_size_dl = 0
		block_sz = 8192
		while True:
			buffer = u.read(block_sz)
			if not buffer:
				break

			file_size_dl += len(buffer)
			f.write(buffer)
			status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
			status = status + chr(8)*(len(status)+1)
			print status,

		f.close()

	def _getRawPathTo(self, photo):
		h = photo.hash
		h1 = h[0:2]
		h2 = h[2:4]
		return os.path.join(self._storageDir, h1, h2, h)

	def _getDatePathTo(self, photo):
		return os.path.join(self._dateDir, photo.dateTakenYear, photo.dateTakenMonth, 
					photo.dateTakenDay, photo.filenameOriginal)

	def _getAlbumPathsTo(self, photo):
		result = []
		for album in photo.albums:
			result.append(os.path.join(self._albumsDir, album, photo.filenameOriginal))
		return result

	def _getTagPathsTo(self, photo):
		result = []
		for tag in photo.tags:
			# ignore "2013" tag
			if re.match("^\d+$", tag):
				continue
			result.append(os.path.join(self._tagsDir, tag, photo.filenameOriginal))
		return result


if __name__ == '__main__':
	Syncer().sync()
