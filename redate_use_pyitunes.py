from pyItunes import *
import dicttoxml

from time import mktime
from datetime import datetime

import re
#N.B. I had to comment out a line of code in the pyitunes library.py file as there was some utf8 error when 
#getting the file location info of songs in my lib (moving from pc to mac)


class Track:
	def __init__(self, artist, track, length, added, wrong_added):
		self.artist = artist
		self.track = track
		self.length = length
		self.added = added
		self.wrong_added = wrong_added

target = "Itunes Music Library.xml"

print "Reading source library..."
#l = Library("practice_library_sample.xml")
l = Library("Library.xml")

print "Reading target library..."
lt = Library(target)
#lt = Library("test_lib_update.xml")

print "opens files fine!"

print "%i source songs" % len(l.songs)
print "%i target songs\n" % len(lt.songs)

print "building up dictionary"
trackDict = {}

count = 0
percent = 0
print "0%"

for iSource, song in l.songs.items():

	if int(100 * count / len(l.songs)) != percent:
		percent = int(100 * count / len(l.songs))
		print "%s%%" % percent


	for iTarget, tsong in lt.songs.items():
		if song.name == tsong.name and song.artist == tsong.artist and song.length == tsong.length:
			#print "Found: \t %s - %s" % (song.artist, datetime.fromtimestamp(mktime(song.date_added)))
			#print "%s - %s - %s" % (tsong.id, tsong.artist, datetime.fromtimestamp(mktime(tsong.date_added)))
			trackDict[iTarget] = Track(song.artist, song.name, song.length, datetime.fromtimestamp(mktime(song.date_added)), datetime.fromtimestamp(mktime(tsong.date_added)))
	count += 1

for one in trackDict:
	print one

#f = open("test_lib_update.xml", 'r')
f = open(target, 'r')
edit_lib = f.readlines()
f.close()
counter = 0
for line in range(13, len(edit_lib)):
	if '<key>' in edit_lib[line] and '<dict>' in edit_lib[line + 1]:
		#print edit_lib[line]
		thisID = int(edit_lib[line][7:(len(edit_lib[line])-7)])
		print thisID
		try:
			print "%s - %s - %s" % (str(thisID), trackDict[thisID].track, trackDict[thisID].artist)
			for i in range(0, 20):
				if 'Date Added' in edit_lib[line+i]:	
					edit_lib[line+i] = edit_lib[line+i].replace(str(trackDict[thisID].wrong_added)[:10], str(trackDict[thisID].added)[:10])

					print "|%s| -> |%s|" % (str(trackDict[thisID].wrong_added)[:10], str(trackDict[thisID].added)[:10])
					i = 20
					counter += 1
		except:
			v = 1
		#print "couldn't find key %s" % thisID

print "%s tracks updates" % str(counter)
new_file = open('new_lib.xml', 'w')
new_file.seek(0)
new_file.writelines(edit_lib)
new_file.close()







