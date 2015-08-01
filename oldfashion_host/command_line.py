#!/usr/bin/python -u

import argparse
import subprocess

import oldfashion, utils
from argparse_actions import StoreGitDirectoryAction

from dokker import Dokker
docker_client = Dokker()


def handle_applet(applet, action, name):
	methodToCall = getattr(applet.instance(docker_client), action)
	methodToCall(name)

def main():
	parser = argparse.ArgumentParser(prog='oldfashion')
	subparsers = parser.add_subparsers()
 
	subparser = subparsers.add_parser('git-receive-pack')
	subparser.add_argument('app', action=StoreGitDirectoryAction) 
	subparser.set_defaults(handle=lambda args: oldfashion.git_receive_pack(args.app))

	subparser = subparsers.add_parser('git-upload-pack')
	subparser.add_argument('app', action=StoreGitDirectoryAction)
	subparser.set_defaults(handle=lambda args: subprocess.call(['git-upload-pack', app.repo()]))

	subparser = subparsers.add_parser('deploy')
	subparser.add_argument('app', action=StoreGitDirectoryAction)
	subparser.set_defaults(handle=lambda args: oldfashion.deploy(args.app))

	subparser = subparsers.add_parser('remove')
	subparser.add_argument('app', action=StoreGitDirectoryAction)
	subparser.set_defaults(handle=lambda args: oldfashion.remove(args.app))

	subparser = subparsers.add_parser('acl')
	subparser.add_argument('action', choices=['add', 'remove'])
	subparser.add_argument('name')
	subparser.set_defaults(handle=lambda args: oldfashion.acl(args.action, args.name))

	for applet in utils.applets():
		subparser = subparsers.add_parser(applet.name)
		subparser.add_argument('action', choices=['spawn', 'kill'])
		subparser.add_argument('name')
		subparser.set_defaults(handle=lambda args: handle_applet(applet, args.action, args.name))

	args = parser.parse_args()
	args.handle(args)