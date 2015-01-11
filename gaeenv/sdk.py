import os
import sys
import shutil
import requests
import re
import xml.etree.ElementTree as ET

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

	# change file mode for executable files
	sdk_dir = os.path.join(lib_dir, 'google_appengine')
	py_files = [ os.path.join(sdk_dir, f) for f in os.listdir(sdk_dir) if os.path.isfile(os.path.join(sdk_dir,f)) and f.endswith('.py') ]
	for f in py_files:
		st = os.stat(f)
		os.chmod(f, st.st_mode | 0111)					

	# remove temp zip file
	logger.debug(" * Cleaning up".format(lib_dir))
	os.remove(zip_file)

def download(version=None):
	"""
    Download App Engine SDK
    """
	if not version:
		version = get_latest_version()

	response = requests.get('https://storage.googleapis.com/appengine-sdks')
	response.raise_for_status()
	tree = ET.fromstring(response.text)

	path = None
	for key in tree.iter('{http://doc.s3.amazonaws.com/2006-03-01}Key'):
		match = re.match('^.*google_appengine_{0}.{1}.{2}\.zip$'.format(*version), key.text)
		if match:
			path = key.text
			break

	url = 'https://storage.googleapis.com/appengine-sdks/{path}'.format(**locals())

	logger.debug(' * Starting SDK download for version {0}.{1}.{2}'.format(*version))
	response = requests.get(url)
	response.raise_for_status()

	temp_zip = os.path.join(gettempdir(), 'google_appengine_{0}.{1}.{2}.zip'.format(*version))
	writefile(temp_zip, response.content, encode=None)
	return temp_zip

def get_versions():
	"""
	Retrieves all available App Engine SDK get_versions
	"""
	versions = []
	response = requests.get('https://storage.googleapis.com/appengine-sdks')
	response.raise_for_status()

	tree = ET.fromstring(response.text)

	for key in tree.iter('{http://doc.s3.amazonaws.com/2006-03-01}Key'):
		match = re.match(r'^.*google_appengine_([0-9]+)\.([0-9]+)\.([0-9]+)\.zip$', key.text)
		if match:
			versions.append((
				int(match.group(1)),
				int(match.group(2)),
				int(match.group(3))
			))

	def compare(x, y):
		return  sum(y) - sum(x)
	
	return sorted(versions, cmp=compare)

def get_latest_version():
	"""
	Retrieves the latest App Engine SDK version
	"""
	versions = get_versions()
	return versions[0]
