import sys
import os
import subprocess
import tempfile
import shutil

from jinja2 import Template

import utils
from dokker import Dokker

reload(sys)
sys.setdefaultencoding('UTF8')

class controlled_execution:
	def __init__(self, msg, rollbackFn=None):
		self.msg = msg
		self.rollbackFn = rollbackFn

	def __enter__(self):
		print('\033[1m----> {}\033[0m'.format(self.msg))
		return self

	def __exit__(self, type, value, traceback):
		if type is not None and self.rollbackFn is not None:
			print('\033[1m----> Rolling back {}\033[0m'.format(self.msg))
			self.rollbackFn()

		return False

	def log(self, msg):
		print(u'      {}'.format(msg))

def git_receive_pack(app):
	repo_path = utils.repo_path(app)

	if not os.path.isdir(os.path.join(repo_path, 'refs')):
		subprocess.call(['git', 'init', '--bare', repo_path], stdout=subprocess.PIPE)

		with open(os.path.join(repo_path, 'hooks/post-receive'), 'w') as f:
			template = Template('''#!/usr/bin/python -u
import os
import sys
import oldfashion

if __name__ == '__main__':
	for line in sys.stdin.xreadlines():
		old, new, ref = line.strip().split(' ')
		if ref == 'refs/heads/master':
			oldfashion.deploy('{{app}}')
''')

			f.write(template.render(app=app))

		subprocess.call(['chmod', '+x', os.path.join(repo_path, 'hooks/post-receive')])
	subprocess.call(['git-receive-pack', repo_path])

def acl(action, name):
	if action == 'add':
		key = sys.stdin.read()

		with open('/home/oldfashion/.ssh/authorized_keys', 'a') as f:
			f.write('command="PYTHONUNBUFFERED=1 NAME={} oldfashion $SSH_ORIGINAL_COMMAND",no-agent-forwarding,no-user-rc,no-X11-forwarding,no-port-forwarding {}'.format(name, key))

	elif action == 'remove':
		pass

def remove(app):
	with controlled_execution('Removing app src') as context:
		shutil.rmtree(utils.repo_path(app))

		with controlled_execution('Removing nginx config') as context:
			if os.path.isfile(utils.nginx_config(app)):
				os.remove(utils.nginx_config(app))

			context.log('Reloading nginx configuration')

			subprocess.call(['sudo', '/etc/init.d/nginx', 'reload'], stdout=subprocess.PIPE)

			with controlled_execution('Removing containers and images') as context:
				docker_client.clean(app)

def deploy(app):
	repo_path = utils.repo_path(app)
	build_path = tempfile.mkdtemp()

	with controlled_execution('Exporting code', rollbackFn=lambda: shutil.rmtree(build_path)) as context:
		subprocess.call(['git', 'clone', '--depth', '1', '--branch', 'master', repo_path, build_path], stdout=subprocess.PIPE)

		context.log('Cloning into {}'.format(build_path))

		app_type = utils.detect(build_path)

		with controlled_execution('Building %s app' % app, rollbackFn=lambda: docker_client.clean_images(docker_client.images(app))) as context:
			utils.copytree(utils.resource_path('builders/{}'.format(app_type)), build_path, {'app': app})

			for line in docker_client.build(build_path, app):
				context.log(line)
			
			with controlled_execution('Running', rollbackFn=lambda: docker_client.clean_containers(docker_client.containers(app))) as context:
				old_containers = docker_client.containers(app)

				container_ip = docker_client.run(app)

				with controlled_execution('Handling nginx') as context:
					def rollback():
						if os.path.isfile(utils.nginx_config(app)):
							os.remove(utils.nginx_config(app))
					context.rollbackFn = rollback

					hostname = subprocess.check_output(['hostname', '-f']).strip()
					domain = '{}.{}'.format(app, hostname)

					context.log('Hostname {}'.format(hostname))

					with open(utils.nginx_config(app), 'w+') as f:
						template = Template('''
upstream {{app}}_upstream {
  {% for ip in ips %}
    server {{ip}};
  {% endfor %}
}

server {
  listen 80;

  server_name www.{{domain}};
  return 301 $scheme://{{domain}};
}

server {
    listen 80;

    server_name {{domain}};

    location / {
      proxy_redirect     off;
      proxy_set_header   X-Real-IP         $remote_addr;
      proxy_set_header   X-Forwarded-For   $proxy_add_x_forwarded_for;
      proxy_set_header   X-Forwarded-Proto $scheme;
      proxy_set_header   Host              $http_host;
      proxy_set_header   X-NginX-Proxy     true;
      proxy_set_header   Connection        "";
      proxy_http_version 1.1;

      proxy_pass         http://{{app}}_upstream;
    }
}
''')

						f.write(template.render(app=app, domain=domain, ips=[container_ip]))

					context.log('Reloading nginx configuration')

					subprocess.call(['sudo', '/etc/init.d/nginx', 'reload'], stdout=subprocess.PIPE)

					with controlled_execution('Cleanup') as context:
						context.log('Cleaning old containers')
						docker_client.clean_containers(old_containers)

						context.log('Cleaning tmp files')
						shutil.rmtree(build_path)

						with controlled_execution('App is running at http://{}'.format(domain)) as context:
							context.log('done.')
