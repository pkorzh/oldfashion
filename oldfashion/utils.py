import sys
import os
import shutil
import stat

reload(sys)
sys.setdefaultencoding('UTF8')

from jinja2 import Template

def repo_path(app):
	return '/home/oldfashion/{}'.format(app)

def image_name(app):
	return 'oldfashion/{}'.format(app)

def container_label(app):
  return 'im.oldfashion.app={}'.format(app)

def nginx_config(app):
  return '/home/oldfashion/{}.conf'.format(app)  

def resource_path(path):
	return os.path.join(os.path.dirname(__file__), path)

def read_resource(path):
	with open(resource_path(path), 'r') as f:
		return f.read()

def detect(dir):
	files = map(lambda name: name.lower(), os.listdir(dir))

	if 'package.json' in files:
		return 'nodejs'
	elif 'manage.py' in files:
		return 'django'
	elif 'gemfile' in files:
		return 'rubyonrails'

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
