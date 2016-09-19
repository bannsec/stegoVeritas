from struct import unpack
import sys

class gif:
	"""
	GIF Parser written completely in Python3
	Owner/Copyright: Michael Bann 2015 (bannsecurity.com)
	Originally designed for StegoVeritas tool (https://github.com/Owlz/stegoVeritas)
	"""
	
	# http://www.w3.org/Graphics/GIF/spec-gif89a.txt
		
	# Known gif types
	validGifTypes = [b'GIF87a',b'GIF89a']
	
	def __init__(self,fileName=None):
		"""
		Init the gif class.
		(optional) fileName -- string path to file (i.e.: "mygif.gif" or "/home/blerg/mygif.gif")
		"""
		
		# self.gif == Loaded gif file (not file handle, this is a bytes)
		self.gif = None
		
		# gifType should either be GIF87a or GIF89a
		self.gifType = None

		# Extention info
		self.extentionFunctionLookup = {
			0xfe: self._parseCommentExtension,
			0xf9: self._parseGraphicControlExtension,
			0xff: self._parseApplicationExtension
		}

		# Comments extension
		self.comments = []
		
		# Load up the gif
		self.load(fileName=fileName)
		
		return
	
	def load(self,fileName=None):
		"""
		Input:
			(optional) fileName -- string path to file (i.e.: "mygif.gif" or "/home/blerg/mygif.gif")
		Action:
			Load up the gif specified. If nothing specified, nothing is loaded.
		Return:
			Nothing
		"""
		
		# If we're given the optional gif name param
		if fileName != None:
			self.gif = open(fileName,"rb").read()
		
		return
	
	def _parseHeader(self):
		"""
		Input: None
		Action:
			Parses the header of the already loaded gif and sets class variables.
			Destructive process. Updates the internal gif buffer.
		Returns: None
		"""
		
		t = self.gif[0:6]
		
		# Check if this file has the right header
		if t not in self.validGifTypes:
			raise Exception("Header Error: {0} not a known GIF header".format(t))
		
		self.gifType = t
		
		# Now that we've parsed it, remove it.
		self.gif = self.gif[6:]
	
	def _parseLogicalScreenDescriptor(self):
		"""
		Input: None
		Action:
			Parses the Logical Screen Descriptor section and sets class variables.
			Destructive process. Updates the internal gif buffer.
		Returns: None
		"""

		# Unpack the info		
		self.width, self.height, packed, self.backgroundColorIndex, self.pixelAspectRatio = unpack("<HHBBB",self.gif[:7])
		
		self.globalColorTable = bool((packed & 2**7) >> 7)
		self.colorResolution = ((packed & 0b01110000) >> 4) + 1
		self.sortFlag = bool(((247 & 0b00001000) >> 3))
		self.sizeGlobalColorTable = 2 ** ((247 & 0b00000111) + 1)
		
		# Fix up the aspect ratio if needed
		if self.pixelAspectRatio != 0:
			self.pixelAspectRatio = (self.pixelAspectRatio + 15) / 64
		
		# Update internal gif
		self.gif = self.gif[7:]
		
	def _parseGlobalColorTable(self):
		"""
		Input: None
		Action:
			Parses the Global Color Table. Due to the nature of gif, this needs to be determined by the header first (globalColorTable flag)
		Returns: None
		"""
		
		# Calculate the size
		size = 3 * self.sizeGlobalColorTable
		
		# Just cut out the global color table portion
		gct = self.gif[:size]
		
		self.globalColorTableRed = []
		self.globalColorTableGreen = []
		self.globalColorTableBlue = []
		
		# Loop through the table and save the values off into the respective arrays
		for x in range(0,size,3):
			self.globalColorTableRed.append(gct[x])
			self.globalColorTableGreen.append(gct[x+1])
			self.globalColorTableBlue.append(gct[x+2])
		
		# Update internal gif
		self.gif = self.gif[size:]

	def _parseExtensionBlock(self):
		"""
		Input: None
		Action:
			Assumes that it is called from parse and that the current portion of the input is at an extention block.
			Determines type of extention block and forwards call along to proper handler
		Returns: None
		"""
		
		# Sanity check
		if self.gif[0] != ord("!"):
			raise Exception("_parseExtentionBlock: Something went wrong. We should be at an extension block and we're not")
			return
		
		# Dynamically function calling to make this easier

		if self.gif[1] in self.extentionFunctionLookup:
			self.extentionFunctionLookup[self.gif[1]]()
		else:
			raise Exception("Extension {0} not implimented yet.".format(self.gif[1]))
			return
		
	def _parseCommentExtension(self):
		"""
		Input: None
		Action:
			Parse a comment extension block.
		Returns: None
		"""
		
		# Sanity check
		if self.gif[:2] != b"!\xfe":
			raise Exception("_parseCommentExtension: We're not at a comment extension block.")
			return
		
		# Update our position
		self.gif = self.gif[2:]
		
		length = self.gif[0]
		self.gif = self.gif[1:]
	
		# Loop through all the comments
		while length != 0:
			comment = self.gif[:length]
			# Save the comment off
			self.comments.append(comment)
			self.gif = self.gif[length:]
			length = self.gif[0]
			self.gif = self.gif[1:]
	
	def _parseGraphicControlExtension(self):
		"""
		Input: None
		Action:
			Parse a graphic control extension block
		Return: None
		"""
		
		# Sanity check
		if self.gif[:2] != b"!\xf9":
			raise Exception("_parseGraphicControlExtension: We're not at a graphic control extension block.")
			return
		
		#print("Not parsing GraphicControlExtention for now")
			
		# Skip this for now
		self.gif = self.gif[8:]
	
	def _parseApplicationExtension(self):
		"""
		Input: None
		Action:
			Parse an Application Extension
		Return: None
		"""
		
		# Sanity check
		if self.gif[:2] != b"!\xff":
			raise Exception("_parseApplicationExtension: We're not at an Application Extension block.")
			return
		
		# In actuality this should be static size of 11
		blockSize = self.gif[2]
		
		# ASCII Identifier
		appID = self.gif[3:11]
		appAuthCode = self.gif[11:14]
		
		# Update gif block
		self.gif = self.gif[14:]

		# I only know of one Application Extension... The Netscape extension for looping animations
		if appID == b"NETSCAPE" and appAuthCode == b"2.0":
			"""
			http://www6.uniovi.es/gifanim/gifabout.htm
			byte   1       : 33 (hex 0x21) GIF Extension code
			byte   2       : 255 (hex 0xFF) Application Extension Label
			byte   3       : 11 (hex (0x0B) Length of Application Block 
			                 (eleven bytes of data to follow)
			bytes  4 to 11 : "NETSCAPE"
			bytes 12 to 14 : "2.0"
			byte  15       : 3 (hex 0x03) Length of Data Sub-Block 
			                 (three bytes of data to follow)
			byte  16       : 1 (hex 0x01)
			bytes 17 to 18 : 0 to 65535, an unsigned integer in 
			                 lo-hi byte format. This indicate the 
			                 number of iterations the loop should 
			                 be executed.
			bytes 19       : 0 (hex 0x00) a Data Sub-block Terminator. 
			"""
			# Mainly concerned with the number of times to loop the gif
			self.looping = unpack("<H",self.gif[2:4])[0]
			# Update gif
			self.gif = self.gif[5:]
			return

		else:
			# We should stop parsing at this point since we don't know how to continue
			raise Exception("_parseApplicationExtension: Unknown Application Extension \"{0}\"".format((appID + appAuthCode).decode('ascii')))

	def _parseImageDescriptor(self):
		"""
		Input: None
		Action:
			Parse the image descriptor section of the gif
		Returns: None
		"""
		
		# Sanity check
		if self.gif[0] != ord(","):
			raise Exception("_parseImageDescriptor: File not at Image Descriptor section")
			return
		
		# Parse out the fields
		leftPos,rightPos,imWidth,imHeight,packed = unpack("<HHHHB",self.gif[1:10])
		
		localColorTable = bool(packed & 0b10000000 >> 7)
		sizeLocalColorTable = 2 ** ((packed & 0b00000111)+1)
		
		# Update gif
		self.gif = self.gif[10:]

		# Need extra parsing if this frame is using a local color table
		if localColorTable:
			# Skip it for now
			self.gif = self.gif[sizeLocalColorTable * 3:]
			#print("Skipping local color table parsing for now")
			#raise Exception("_parseImageDescriptor: No support currently for local color tables")
		
		# Not really parsing the data for now. Looping through it
		lzwMinCodeSize = self.gif[0]
		length = self.gif[1]
		self.gif = self.gif[length+2:]
		
		# Loop through all the sub blocks
		while length > 0:
			length = self.gif[0]
			self.gif = self.gif[length+1:]
		


	def parse(self):
		"""
		Input: None
		Action:
			Given the already loaded gif, parse it. Setting internal variables.
		Returns: None
		"""
		
		# Header first
		self._parseHeader()
		
		# Required section -- Logical Screen Descriptor
		self._parseLogicalScreenDescriptor()
		
		# If we are dealing with a global color table
		if self.globalColorTable:
			self._parseGlobalColorTable()
		
		# Now we need to loop through the rest since it's not linear from here
		while len(self.gif) > 0:
			
			# Are we looking at an extention block?
			if self.gif[0] == ord("!"):
				self._parseExtensionBlock()
			# Image Descriptor
			elif self.gif[0] == ord(","):
				self._parseImageDescriptor()
			# Descriptor telling us we're done parsing
			elif self.gif[0] == ord(";"):
				self.gif = self.gif[1:]
				return
			# Something went wrong
			else:
				raise Exception("Unknown identifier: {0}".format(self.gif[0]))

