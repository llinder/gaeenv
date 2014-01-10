import os
import sys
import shutil
import requests
import re

from tempfile import gettempdir
from utils import logger, writefile
from zipfile import ZipFile


def install(env_dir, version=None):
	"""
	Install App Engine SDK
	"""
	# download SDK
	zip_file = download(version)

	lib_dir = os.path.join(env_dir, 'lib')

	# make lib directory if it doesn't exist
	if not os.path.exists(lib_dir):
		os.makedirs(lib_dir)

	# remove existing sdk if present
	if os.path.exists(os.path.join(lib_dir, 'google_appengine')):
		logger.debug(' * Removing existing SDK directory')
		shutil.rmtree(os.path.join(lib_dir, 'google_appengine'))

	# unzip SDK
	logger.debug(" * Installing SDK to dir '{0}'".format(lib_dir))
	with ZipFile(zip_file) as z:
		z.extractall(lib_dir)

	# remove temp zip file
	logger.debug(" * Cleaning up".format(lib_dir))
	os.remove(zip_file)

def download(version=None):
	"""
    Download App Engine SDK
    """
	if not version:
		lvt = get_latest_version()
		version = '{0}.{1}.{2}'.format(*lvt)

	gae_url = 'http://googleappengine.googlecode.com/files/google_appengine_{0}.zip'.format(version)

	logger.debug(' * Starting SDK download for version %s' % version)
	response = requests.get(gae_url)
	response.raise_for_status()

	temp_dir = gettempdir()
	temp_zip = os.path.join(temp_dir, 'google_appengine_%s.zip' % version)
	writefile(temp_zip, response.content, encode=None)
	return temp_zip

def get_versions():
	"""
	Retrieves all available App Engine SDK get_versions
	"""
	response = requests.get('https://code.google.com/p/googleappengine/downloads/list?can=1&q=&colspec=Filename&num=2000')
	response.raise_for_status()

	versions = []
	for match in re.finditer(r'google_appengine_([0-9]+)\.([0-9]+)\.([0-9]+)\.zip', response.text):
		versions.append((match.group(1),match.group(2),match.group(3)))

	return sorted(set(versions), key=lambda tup: str(tup), reverse=True)

__latest_version = None
def get_latest_version():
	"""
	Retrieves the latest App Engine SDK version
	"""
	global __latest_version
	if not __latest_version:
		response = requests.get('https://code.google.com/p/googleappengine/downloads/list?can=2&q=&colspec=Filename')
		response.raise_for_status()
		
		match = re.search(r'google_appengine_([0-9]+)\.([0-9]+)\.([0-9]+)\.zip', response.text)
		if match:
			__latest_version = (match.group(1),match.group(2),match.group(3))
		else:
			raise Exception('App Engine SDK version not found') 

	return __latest_version