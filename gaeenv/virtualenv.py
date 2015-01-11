import os
import sys
import re
import textwrap

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
			file.write(textwrap.dedent("""\
				../../google_appengine
				import dev_appserver; dev_appserver.fix_sys_path()"""))

	logger.info(' * App Engine SDK path added to Python site packages')


def add_gae_activation(env_dir):
	activate = textwrap.dedent("""\
		# === GAEENV START ===

		deactivate_gae () {
		    # reset old environment variables
		    if [ -n "$_OLD_GAE_VIRTUAL_PATH" ] ; then
		        PATH="$_OLD_GAE_VIRTUAL_PATH"
		        export PATH
		        unset _OLD_GAE_VIRTUAL_PATH
		    fi
		    if [ -n "$_OLD_GAE_SDK_ROOT" ] ; then
		        GAE_SDK_ROOT="$_OLD_GAE_SDK_ROOT"
		        export GAE_SDK_ROOT
		        unset _OLD_GAE_SDK_ROOT
		    fi
		    
		    # This should detect bash and zsh, which have a hash command that must
		    # be called to get it to forget past commands.  Without forgetting
		    # past commands the $PATH changes we made may not be respected
		    if [ -n "$BASH" -o -n "$ZSH_VERSION" ] ; then
		        hash -r
		    fi
		    
		    if [ ! "$1" = "nondestructive" ] ; then
		        # Self destruct!
		        unset -f deactivate_gae
		    fi
		}
		
		# unset irrelevant variables
		deactivate_gae nondestructive
		
		_OLD_GAE_SDK_ROOT="$GAE_SDK_ROOT"
		GAE_SDK_ROOT="$VIRTUAL_ENV/lib/google_appengine"
		export GAE_SDK_ROOT
		
		_OLD_GAE_VIRTUAL_PATH="$PATH"
		PATH=$GAE_SDK_ROOT:$PATH
		export PATH
		
		# === GAEENV END ===""")

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