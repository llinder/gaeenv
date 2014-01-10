import os
import sys
import re

from utils import logger

def add_gae_pth(env_dir):
	site_packages_dir = os.path.join(
		env_dir, 
		'lib', 'python{0}.{1}'.format(sys.version_info.major, sys.version_info.minor),
		'site-packages')

	if not os.path.exists(site_packages_dir):
		logger.error('Python site packages directory doesn\'t exist. Please ensure Virtualenv is activated.')
	else:
		with open(os.path.join(site_packages_dir, 'gae.pth'), 'wb') as file:
			file.write((
				'../../google_appengine\n'
				'import dev_appserver; dev_appserver.fix_sys_path()'))

	logger.info(' * App Engine SDK path added to Python site packages')


def add_gae_activation(env_dir):
	activate = (
		'# === GAEENV START ===\n'
		'\n'
		'deactivate_gae () {\n'
    	'	# reset old environment variables\n'
    	'	if [ -n "$_OLD_GAE_VIRTUAL_PATH" ] ; then\n'
        '		PATH="$_OLD_GAE_VIRTUAL_PATH"\n'
        '		export PATH\n'
        '		unset _OLD_GAE_VIRTUAL_PATH\n'
    	'	fi\n'
    	'	if [ -n "$_OLD_GAE_SDK_ROOT" ] ; then\n'
    	'		GAE_SDK_ROOT="$_OLD_GAE_SDK_ROOT"\n'
        '		export GAE_SDK_ROOT\n'
        '		unset _OLD_GAE_SDK_ROOT\n'
        '	fi\n'
    	'	\n'
		'	# This should detect bash and zsh, which have a hash command that must\n'
    	'	# be called to get it to forget past commands.  Without forgetting\n'
    	'	# past commands the $PATH changes we made may not be respected\n'
    	'	if [ -n "$BASH" -o -n "$ZSH_VERSION" ] ; then\n'
        '		hash -r\n'
    	'	fi\n'
    	'	\n'
    	'	if [ ! "$1" = "nondestructive" ] ; then\n'
    	'		# Self destruct!\n'
        '		unset -f deactivate_gae\n'
    	'	fi\n'
		'}\n'
		'\n'
		'# unset irrelevant variables\n'
		'deactivate_gae nondestructive\n'
		'\n'
		'_OLD_GAE_SDK_ROOT="$GAE_SDK_ROOT"\n'
		'GAE_SDK_ROOT="$VIRTUAL_ENV/lib/google_appengine"\n'
		'export GAE_SDK_ROOT\n'
		'\n'
		'_OLD_GAE_VIRTUAL_PATH="$PATH"\n'
		'PATH=$GAE_SDK_ROOT:$PATH\n'
		'export PATH\n'
		'\n'
		'# === GAEENV END ===\n')

	activate_script = os.path.join(env_dir, 'bin', 'activate')
	if not os.path.exists(activate_script):
		logger.error('Virtualenv activation script doesn\'t exist. Please ensure Virtualenv is activated')
	else:
		source_code = ''
		with open(activate_script, 'r') as file:
			source_code = file.read()

		if '# === GAEENV START ===' not in source_code:
			logger.info(' * Adding App Engine configuration to Virutalenv activate script')
			with open(activate_script, 'ab') as file:
				file.write(activate)
		else:
			logger.info(' * App Engine Virtualenv activation already exists')


def remove_gae_activation(env_dir):
	activate_script = os.path.join(env_dir, 'bin', 'activate')
	if not os.path.exists(activate_script):
		logger.error('Virtualenv activation script does\'t exist. Please ensure Virtualenv is activated')
	else:
		source_code = ''
		with open(activate_script, 'r') as file:
			source_code = file.read()

		source_code = re.sub(r'# === GAEENV START ===.*?# === GAEENV END ===', '', source_code, flags=re.DOTALL)
		with open(activate_script, 'wb') as file:
			file.write(source_code)