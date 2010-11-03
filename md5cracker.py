#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import cookielib
import string

__id__ = "md5searcher.py"
__version__ = "v1.1"
__author__ = "Javier Rascón Mesa"
__license__ = "GPL"

class md5web:
	"""
	Class to encode a web for searching md5sums
	"""
	
	rpc_str = '#hash#' # str to replace by the hash
	
	def __init__(self, url, prev_str, post_str, post_params=[]):
		"""
		Constructor
		
		Params:
			url(str): URL where to find the checksums
			prev_str(str): string before the searched string
			post_str(str): string after the searched string
			post_params(list): Parameters for the request
			
			NOTE: The 'url' or 'post_params' have to contain the string
			'#hash#' where the hash string will be placed
		"""
		
		self.url = url
		self.prev_str = prev_str
		self.post_str = post_str
		self.post_params = post_params
		
		if self.rpc_str in url:
			self.mode = "GET"
		else:
			self.mode = "POST"
			
		# set up cookies
		cJar=cookielib.LWPCookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cJar))
		urllib2.install_opener(opener)
	
	def get(self, hash):
		"""
		Method to search a text in a web
		
		Params:
			hash(str): Searched hash
		
		Return:
			(str): Text found
		"""
		found = ''
		
		try:
			
			url = self.url
			params = self.post_params
			
			if self.mode == "GET":
				url = url.replace(self.rpc_str, hash)
			else:
				for k, v in self.post_params.items():
					if self.rpc_str in v:
						v = v.replace(self.rpc_str, hash)
						params[k] = v
						
			encoded_params = urllib.urlencode(params)
			req = urllib2.Request(url, encoded_params)
			page = urllib2.urlopen(req).read()
			
			if self.prev_str in page and self.post_str in page:
				found = page.split(self.prev_str)[1]
				found = found.split(self.post_str)[0]

		finally:
			return found
		
class md5cracker:
	
	webs = []
	
	def __init__(self):
		"""
		Constructor
		"""
		
		self.webs.append(md5web(\
		'http://md5-db.de/#hash#.html',\
		'verwenden:</strong><ul><li>',\
		'</li>'))
		
		self.webs.append(md5web(\
		'http://md5online.net/',\
		'<br>pass : <b>',\
		'</b></p>',\
		{'pass':'#hash#', 'option':'hash2text', 'send':'submit'}))
		
		self.webs.append(md5web(\
		'http://md5crack.com/crackmd5.php',\
		'("',\
		'")',\
		{'term': "#hash#", 'crackbtn': 'Crack+that+hash+baby%21'}))
		
		self.webs.append(md5web(\
		'http://md5pass.info',\
		'Password - <b>',\
		'</b>',\
		{'hash': '#hash#', 'get_pass': 'Get+Pass'}))
		
		self.webs.append(md5web(\
		'http://md5decryption.com',\
		'Decrypted Text: </b>',\
		'</font>',\
		{'hash': '#hash#', 'submit': 'Decrypt+It%21'}))
		
		#self.webs.append(md5web(\
		#'http://',\
		#'',\
		#'',\
		#{}))
	
	def find(self, _hash):
		"""
		Method to find a hash
		
		Params:
			_hash(srt): hash to fond
			
		Return:
			(str): string found
		"""
		
		found = ''
		
		hash = _hash.strip(string.whitespace)
		
		for w in self.webs:
		
			found = w.get(hash)
			if not found:
				print "DEBUG: Failed to recover hash at %s" % (w.url, )
			else:
				print "DEBUG: Found --> '%s' <-- at %s" % (found, w.url)
			
		return found.strip(string.whitespace)

#P.O.C.
if __name__ == "__main__":
	md5cracker().find('e10adc3949ba59abbe56e057f20f883e') # 123456
