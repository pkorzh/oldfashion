#!/usr/bin/python -u

import argparse
import subprocess

import oldfashion, utils
from argparse_actions import StoreGitDirectoryAction


def main():
	parser = argparse.ArgumentParser(prog='oldfashion')
	subparsers = parser.add_subparsers()
 
	parser_git_receive_pack = subparsers.add_parser('git-receive-pack')
	parser_git_receive_pack.add_argument('app', action=StoreGitDirectoryAction) 
	parser_git_receive_pack.set_defaults(handle=lambda args: oldfashion.git_receive_pack(args.app))

	parser_git_upload_pack  = subparsers.add_parser('git-upload-pack')
	parser_git_upload_pack.add_argument('app', action=StoreGitDirectoryAction)
	parser_git_upload_pack.set_defaults(handle=lambda args: subprocess.call(['git-upload-pack', utils.repo_path(args.app)]))

	parser_build  = subparsers.add_parser('deploy')
	parser_build.add_argument('app', action=StoreGitDirectoryAction)
	parser_build.set_defaults(handle=lambda args: oldfashion.deploy(args.app))

	parser_build  = subparsers.add_parser('remove')
	parser_build.add_argument('app', action=StoreGitDirectoryAction)
	parser_build.set_defaults(handle=lambda args: oldfashion.remove(args.app))

	parser_build  = subparsers.add_parser('acl')
	parser_build.add_argument('action', choices=['add', 'remove'])
	parser_build.add_argument('name')
	parser_build.set_defaults(handle=lambda args: oldfashion.acl(args.action, args.name))

	args = parser.parse_args()
	args.handle(args)