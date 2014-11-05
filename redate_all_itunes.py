#!/usr/bin/python

from xml.dom.minidom import parse, parseString
import xml.dom.minidom
import dicttoxml

import xml.etree.ElementTree as ET
tree = ET.parse('practice_library_sample.xml')
root = ET.Element("plist")

print root.tag
print "Reading source file..."
DOMsource = xml.dom.minidom.parse("practice_library_sample.xml")
collection = DOMsource.documentElement

print "Reading target file..."
DOMtarget = xml.dom.minidom.parse("Library_updated_hopefully.xml")
targetCollection = DOMtarget.documentElement

print "finding all source tracks"
tracks = collection.getElementsByTagName("dict")

targetTracks = targetCollection.getElementsByTagName("dict")

xml_string = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd"><plist version="1.0"><dict><key>Major Version</key><integer>1</integer><key>Minor Version</key><integer>1</integer><key>Date</key><date>2014-09-21T14:46:27Z</date><key>Application Version</key><string>11.2.2</string><key>Features</key><integer>5</integer><key>Show Content Ratings</key><true/><key>Music Folder</key><string>file://localhost/C:/Users/Jonas/Music/iTunes%20Music/</string><key>Library Persistent ID</key><string>EA2DB1675A96EFB7</string><key>Tracks</key>'

for track in tracks:
	keys=track.getElementsByTagName('key')
	vals=[key.nextSibling.firstChild for key in keys]
	keys=[key.firstChild.data for key in keys]
	vals=[val.data if val else None for val in vals]
	data=dict(zip(keys,vals))

	correct_added = data["Date Added"]

	print "%s - %s \t Added %s \n" % (data["Name"], data["Artist"], data["Date Added"])

	for tTrack in targetTracks:
		tkeys=tTrack.getElementsByTagName('key')
		tvals=[tkey.nextSibling.firstChild for tkey in tkeys]
		tkeys=[tkey.firstChild.data for tkey in tkeys]
		tvals=[tval.data if tval else None for tval in tvals]
		tdata=dict(zip(tkeys,tvals))


		if data["Name"] == tdata["Name"] and data["Artist"] == tdata["Artist"] and data["Total Time"] == tdata["Total Time"]:
			print "Done!"
			print "%s - %s, \t Duration: %s \t Rrong date: %s" % (data["Name"], data["Artist"], data["Total Time"], data["Date Added"])
			print "%s - %s, \t Duration: %s \t Wight date: %s" % (tdata["Name"], tdata["Artist"], tdata["Total Time"], tdata["Date Added"])
			print "------------------------------------------- \n"

			tdata["Date Added"] = data["Date Added"]
			xml_tdata = dicttoxml.dicttoxml(tdata, root=False)
			xml_string += xml_tdata
			break

xml_string += '</dict></plist>'

f = open('new_lib.xml', 'w')

f.write(xml_string)

f.close()

tdata_node = parseString(xml_string)
tdata_node.toprettyxml()


f = open('new_lib.xml', 'w')

f.write(str(tdata_node.data))

f.close()

