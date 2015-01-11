#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    gaeenv
    ~~~~~~~
    Google App Engine virtual environment helper

    :copyright: (c) 2013 by Lance Linder
    :license: Apache 2.0, see LICENSE for more details.
"""

gaeenv_version = '0.1.3'

import sys
import os
import logging
import argparse
import sdk
import virtualenv
import requirements as req

from utils import logger
from pkg_resources import parse_version

VIRTUAL_ENV = 'VIRTUAL_ENV'

def main():
    # parse cli args
    args = parse_args(sys.argv[1:])

    # set log level
    if args.verbose is 1:
        logger.setLevel(logging.INFO)
    elif args.verbose > 1:
        logger.setLevel(logging.DEBUG)

    args.func(args)


def parse_args(args):
    """
    Parses command line arguments
    """
    parser = argparse.ArgumentParser(description='Utilities to manage Google App Engine in an existing Virtualenv')

    parser.add_argument('-v', '--verbose', action='count')

    subparsers = parser.add_subparsers(title='commands', dest="command")

    # --- list commands ---
    list_parser = subparsers.add_parser('list')
    list_subparsers = list_parser.add_subparsers(title='list commands', dest='list_command')
    
    # list sdk
    list_sdk_command = list_subparsers.add_parser('sdk', description='List available App Engine SDK versions')
    list_sdk_command.set_defaults(func=list_sdk_versions)

    # list requirements
    list_req_command = list_subparsers.add_parser('requirements', description='List Python requirements')
    list_req_command.add_argument('-r', '--requirements', 
                                  type=str, default='requirements.txt', 
                                  help='Python requirements file')
    list_req_command.set_defaults(func=list_requirements)
    

    # --- latest commands ---
    latest_parser = subparsers.add_parser('latest')
    latest_subparsers = latest_parser.add_subparsers(title='latest commands', dest='latest_command')
    latest_sdk_command = latest_subparsers.add_parser('sdk', description='Prints the latest App Engine SDK version')
    latest_sdk_command.set_defaults(func=latest_sdk_version)
    

    # --- install commands ---
    install_parser = subparsers.add_parser('install')
    install_subparsers = install_parser.add_subparsers(title='install commands', dest='install_command')

    # install sdk
    install_sdk_command = install_subparsers.add_parser('sdk', description='Installs App Engine SDK in Virtualenv')
    install_sdk_command.add_argument('-v', '--version', help='App Engine SDK version. For a list of available versions use "list sdk"')
    install_sdk_command.set_defaults(func=install_sdk)    

    # install requirements links
    install_req_command = install_subparsers.add_parser('requirements', description='Installs requirements links')
    install_req_command.add_argument('-r', '--requirements', 
                                     type=str, default='requirements.txt', 
                                     help='Python requirements file')
    install_req_command.add_argument('-d', '--directory', 
                                     type=str, default='src/lib', 
                                     help='Directory where Python requirements will be linked')
    install_req_command.set_defaults(func=install_requirements)    



    # --- remove commands ---

    # remove sdk

    # remove requirements links


    return parser.parse_args(args)


def list_sdk_versions(args):
    logger.debug(' * Retreiving list of App Engine SDK versions')
    versions = sdk.get_versions()
    for version in sdk.get_versions():
        print '{0}.{1}.{2}'.format(*version)

    sys.exit(0)


def list_requirements(args):
    if not os.path.exists(args.requirements):
        logger.error('requirements file {0} not found'.format(args.requirements))
        sys.exit(1)

    req.list(args.requirements)
    sys.exit(0)


def latest_sdk_version(args):
    logger.info(' * Retreiving latest App Engine SDK version')
    version = sdk.get_latest_version()
    print '{0}.{1}.{2}'.format(*version)
    sys.exit(0)


def install_sdk(args):
    logger.info(' * Installing App Engine SDK')
    # validate virtualenv directory
    virtual_env_dir = os.environ.get(VIRTUAL_ENV)
    if not virtual_env_dir:
        logger.error("Virtualenv doesn't exist. Please ensure one is activated.")
        sys.exit(1)

    sdk.install(os.path.abspath(virtual_env_dir), args.version)
    
    logger.info(' * Adding App Engine environment variables to Virtualenv activation script')
    virtualenv.add_gae_activation(virtual_env_dir)

    logger.info(' * Adding App Engine SDK path to Virtualenv site packages')
    virtualenv.add_gae_pth(virtual_env_dir)

    logger.info(' * App Engine SDK installation complete')
    sys.exit(0)

def install_requirements(args):
    logger.info(' * Installing Python requirements')

    # validate requirements file
    if not os.path.exists(args.requirements):
        logger.error('requirements file {0} not found'.format(args.requirements))
        sys.exit(1)

    # make target directory if it doesn't exist
    curr_dir = os.getcwd()
    target_dir = os.path.join(curr_dir, args.directory)
    if not os.path.exists(target_dir):
        logger.debug(' * Target link directory doesn\'t exist. One will be created at {0}'.format(target_dir))
        os.makedirs(target_dir)

    req.link(args.requirements, target_dir)

    sys.exit(0)

def remove(args):
    logger.error('Not implemented')
    sys.exit(1)


if __name__ == '__main__':
    main()
