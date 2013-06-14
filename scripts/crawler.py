#!/usr/bin/python
__author__ = 'chenxm'
__email__ = 'chenxm35@gmail.com'

import sys, os
import urllib2

import html5lib
import html5lib.treebuilders as tb


prefix = "http://www.fileinfo.com/filetypes"

categories = [
"text", "data", "audio", "video", "ebook", "3d_image",
"raster_image", "vector_image", "camera_raw", "page_layout",
"spreadsheet", "database", "executable", "game", "cad", "gis",
"web", "plugin", "font", "system", "settings", "encoded", "compressed",
"disk_image", "developer", "backup", "misc"]


def _valid_XML_char_ordinal(i):
	## As for the XML specification, valid chars must be in the range of
	## Char ::= #x9 | #xA | #xD | [#x20-#xD7FF] | [#xE000-#xFFFD] | [#x10000-#x10FFFF]
	## [Ref] http://stackoverflow.com/questions/8733233/filtering-out-certain-bytes-in-python
    return (# conditions ordered by presumed frequency
		0x20 <= i <= 0xD7FF 
	    or i in (0x9, 0xA, 0xD)
	    or 0xE000 <= i <= 0xFFFD
	    or 0x10000 <= i <= 0x10FFFF
	    )


def parse_filetypes(url):
	"""
	"""
	print url
	filetypes = []
	wholepage = urllib2.urlopen(url).read()
	if wholepage == None: return filetypes

	parser = html5lib.HTMLParser(tree = tb.getTreeBuilder("lxml"))

	try:
		html_doc = parser.parse(wholepage)
	except ValueError:
		wholepage_clean = ''.join(c for c in wholepage if _valid_XML_char_ordinal(ord(c)))
		html_doc = parser.parse(wholepage_clean)

	filetypetable = html_doc.find("//{*}table[@id='filetypetable']")
	if filetypetable == None:
		print("can't find id='filetypetable' element"); sys.exit(-1)

	tbody = filetypetable.find("./{*}tbody")
	if tbody is None:
		print("can't find 'tbody' element"); sys.exit(-1)

	for entry in tbody.findall("./{*}tr/{*}td[1]/{*}a"):
		filetypes.append(entry.text.split('.')[1])

	return filetypes


def runMain():
	folder = './database'
	if not os.path.exists(folder):
		os.mkdir(folder)

	for cat in categories:
		filetypes = parse_filetypes(prefix + '/' + cat)
		with open(os.path.join(folder, cat), 'wb') as of:
			of.write('\n'.join(filetypes))


if __name__ == "__main__":
	runMain()


# EOF