import json
import utils

from docker import Client


docker_client = Dokker(Client(base_url='unix://var/run/docker.sock'))

class ContainerList():
	def __init__(self, containers):
		self.containers = containers

	def kill(self):
		for container in self.containers:
			docker_client.stop(container)
			docker_client.remove_container(container, force=True)


class ImageList():
	def __init__(self, images):
		self.images = images

	def kill(self):
		for images in self.images:
			docker_client.remove_image(image=image, force=True)


class Dokker:
	def __init__(self):
		pass

	def spawn(self, **kwargs):
		kwargs['detach'] = True

		container = docker_client.create_container(**kwargs)

		docker_client.start(container)

		info = docker_client.inspect_container(container)

		return info['NetworkSettings']['IPAddress']

	def containers(self, **kwargs):
		return ContainerList(docker_client.containers(quiet=True, filters=kwargs))

	def images(self, **kwargs):
		name = kwargs.pop('name', None)
		quiet = kwargs.pop('quiet', True)

		return ImageList(docker_client.images(name=name, quiet=quiet, filters=kwargs))

	def build(self):
		rm = kwargs.pop('rm', False)
		forcerm = kwargs.pop('forcerm', True)

		for line in self.docker_client.build(**kwargs, rm=rm, forcerm=forcerm):
			yield val

	def purge(self, app):
		self.containers(app=app)
			.kill()

		self.images(app=app)
			.kill()