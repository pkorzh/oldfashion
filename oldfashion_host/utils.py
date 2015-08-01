import sys
import os
import shutil
import stat
import pkg_resources

reload(sys)
sys.setdefaultencoding('UTF8')

from jinja2 import Template

class Bunch:
	def __init__(self, **kwds):
		self.__dict__.update(kwds)
		self.__cache = None

	def instance(self, *args):
		return self.load()(*args)


def plugins(type):
	return [Bunch(**dict(name=v.name, load=v.load)) for v in pkg_resources.iter_entry_points(group='oldfashion.{}'.format(type), name=None)]

def buildpacks():
	return plugins('buildpack')

def applets():
	return plugins('applet')

def copytree(src, dst, context={}, symlinks = False, ignore = None):
	if ignore is None:
		ignore = shutil.ignore_patterns('.DS_Store')

	if not os.path.exists(dst):
		os.makedirs(dst)
		shutil.copystat(src, dst)
	lst = os.listdir(src)
	if ignore:
		excl = ignore(src, lst)
		lst = [x for x in lst if x not in excl]
	for item in lst:
		s = os.path.join(src, item)
		d = os.path.join(dst, item)
		if symlinks and os.path.islink(s):
			if os.path.lexists(d):
				os.remove(d)
			os.symlink(os.readlink(s), d)
			try:
				st = os.lstat(s)
				mode = stat.S_IMODE(st.st_mode)
				os.lchmod(d, mode)
			except:
				pass # lchmod not available
		elif os.path.isdir(s):
			copytree(s, d, symlinks, ignore)
		else:
			with open(s, 'r') as f:
				content = f.read()

			with open(d, 'w+') as df:
				template = Template(content)
				df.write(template.render(context))
