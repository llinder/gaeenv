"""
gaeenv
~~~~~~~

Google App Engine Virtual Environment builder.
"""
import os
from setuptools import setup, find_packages
from gaeenv.main import gaeenv_version
from pip.req import parse_requirements

def read_file(file_name):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
    with open(path) as f:
        return f.read()

required = read_file('requirements.txt').splitlines()

ldesc = read_file('README')
ldesc += "\n\n" + read_file('CHANGES')

setup(
    name='gaeenv',
    version=gaeenv_version,
    url='https://github.com/llinder/gaeenv',
    license='Apache 2.0',
    author='Lance Linder',
    author_email='llinder@gmail.com',
    description="Goole App Engine Virtualenv tools",
    long_description=ldesc,
    packages = find_packages(exclude="test"),
    install_requires = required,
    entry_points={
        'console_scripts': ['gaeenv = gaeenv.main:main']
    },
    zip_safe=False,
    platforms='any',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
