# coding=utf-8
#!/usr/local/opt/python/libexec/bin/python
import fnmatch
import os
from bs4 import BeautifulSoup
from mutagen.mp4 import MP4, MP4Cover
from PIL import Image, ImageDraw, ImageFilter

#iTunes				=M4B Tag		#Plex						|Calibre				|ABB
M4B_ARTIST			= "\xa9ART"		#Artist						|calibre.creator		|Author
M4B_ALBUM_ARTIST	= "aART"		#Will override artist field	|calibre.creator		|Narrator
M4B_TRACK_TITLE		= "\xa9nam"		#Title						|calibre.title			|Title
M4B_ALBUM			= "\xa9alb"		#Album						|calibre.bookSeries		|Title
M4B_YEAR			= "\xa9day"		#Originally Available		|calibre.date			|
M4B_DESCRIPTION		= "desc"		#Review						|calibre.description	|
M4B_GENRE			= "\xa9gen"		#Tags						|calibre.subject		|Genre
M4B_COVER			= "covr"		#Poster						|cover.jpg				|over

pattern = '*.m4b'


#*********************************
#** Path to your Calibre Library**
#*********************************
path = '/volumes/Bay 4 HD/Calibre Library'
#path = '/users/mra/Calibre Library'


	
class calibre:
	def __init__(self):
		self.test = 'Test'
		self.title = ''
		self.lastTagged = ''
		self.creator = ''
		self.date = ''
		self.html = ''
		self.description = ''
		self.publisher = ''
		self.subject = ''
		self.series = ''
		self.bookSeries = ''
		
	def fetch(self,opfFile):
		print ('Processing: ',opfFile)
		with open(opfFile,"r") as f:
			soup = BeautifulSoup(f, 'xml')
			try:
				self.lastTagged=soup.find("audioTagged").string
			except:
				self.lastTagged=''
				self.title           = soup.find("dc:title").string
				self.bookSeries      = self.title
				self.creator         = soup.find("dc:creator").string
				try:
					self.date        = soup.find("dc:date").string
				except :
					self.date        =''
				try:
					self.html        = soup.find("dc:description").string.replace('&lt;','<').replace('&gt;','>')
				except:
					self.html        = ''
					self.description = ''
				else:
					innerSoup = BeautifulSoup(self.html.replace(' \n','<br>'),'lxml')
					self.description     = innerSoup.get_text()
				try:
					self.publisher   = soup.find("dc:publisher").string
				except:
					self.publisher=''
				try:
					self.subject     = soup.find("dc:subject").string
				except:
					self.subject     = ''
				try:
					self.series = soup.find("meta", {"name" : "calibre:series"})['content']
					self.bookSeries = self.bookSeries+' - '+self.series
					try:
						self.seriesIndex = soup.find("meta", {"name" : "calibre:series_index"})['content']
						self.bookSeries = self.bookSeries+' - '+self.seriesIndex
					except:
						self.seriesIndex=''
				except:
					self.series=''
			finally:
				f.close()

def transparentSquare(pil_img, background_color):
	width, height = pil_img.size
	if width == height:
		return pil_img
	elif width > height:
		result = Image.new(pil_img.mode, (width, width), background_color)
		result.putalpha(0)
		result.paste(pil_img, (0, (width - height) // 2))
		return result
	else:
		result = Image.new(pil_img.mode, (height, height), background_color)
		result.putalpha(0)
		result.paste(pil_img, ((height - width) // 2, 0))
		return result



for calibreDir, dirnames, filenames in os.walk(path):
	if not filenames:
		continue
	pythonic_files = fnmatch.filter(filenames, pattern)
	if pythonic_files:
		for file in pythonic_files:
			m4bFile        =('{}/{}'.format(calibreDir, file))
			opfFile        = calibreDir+'/metadata.opf'
			coverImageFile = calibreDir+"/cover.jpg"
			
#			****************************
#			** Parse the the OPF      **
#			****************************
			if (os.path.exists(opfFile) == True):
				calibreData=calibre()
				calibreData.fetch(opfFile)
				if (calibreData.lastTagged != ''):
					print ('Skipping; last updated: ', calibreData.lastTagged)
				else:
# 					****************************
# 					** Create The Cover       **
# 					****************************
					im_rgb = Image.open(coverImageFile)
					im_square = transparentSquare(im_rgb, 0)
					im_square.save(calibreDir+'/poster.png', quality=95)
					with open(calibreDir+'/poster.png', "rb") as f:
						coverArt=MP4Cover(f.read(),imageformat=MP4Cover.FORMAT_PNG)
					

# 					****************************
# 					** Update the MB4         **
# 					****************************
					if (os.path.exists(m4bFile[0:-3]+'original_m4b') == False):
						os.popen('cp "'+m4bFile+'" "'+m4bFile[0:-3]+'original_m4b"') 
					m4bTags = MP4(m4bFile)
					m4bTags[M4B_ARTIST]			= calibreData.creator
					m4bTags[M4B_ALBUM_ARTIST]	= calibreData.creator
					m4bTags[M4B_TRACK_TITLE]	= calibreData.title
					m4bTags[M4B_ALBUM]			= calibreData.bookSeries
					m4bTags[M4B_YEAR]			= calibreData.date
					m4bTags[M4B_DESCRIPTION]	= calibreData.description
					m4bTags[M4B_GENRE]			= calibreData.subject
					m4bTags[M4B_COVER] 			= [bytes(coverArt)]
					m4bTags.save(m4bFile)
				
# 					****************************
# 					** Update the OPF         **
# 					****************************
					f1 = open(opfFile)
					contents = f1.read()
					contents = contents[0:-11]+'\n    <audioTagged>v1</audioTagged>\n</package>'
					f1.close()
					f2 = open(opfFile,'w')
					f2.write(contents)
					f2.close()
