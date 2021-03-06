import argparse

class StoreGitDirectoryAction(argparse.Action):
	def __init__(self, option_strings, dest, nargs=None, const=None, default=None, type=None, choices=None, required=False, help=None, metavar=None):
		if nargs == 0:
			raise ValueError('nargs for store actions must be > 0; if you have nothing to store, actions such as store true or store const may be more appropriate')
		if const is not None and nargs != OPTIONAL:
			raise ValueError('nargs must be %r to supply const' % OPTIONAL)
		super(StoreGitDirectoryAction, self).__init__(option_strings=option_strings, dest=dest, nargs=nargs, const=const, default=default, type=type, choices=choices, required=required, help=help, metavar=metavar)

	def __call__(self, parser, namespace, values, option_string=None):
		setattr(namespace, self.dest, values.replace("'", ""))