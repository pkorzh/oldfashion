import json
import utils

from docker import Client


docker_client = Client(base_url='unix://var/run/docker.sock')

class ContainerList():
	def __init__(self, containers):
		self.containers = containers

	def any(self):
		return len(self.containers) > 0

	def kill(self):
		for container in self.containers:
			docker_client.stop(container)
			docker_client.remove_container(container, force=True)


class ImageList():
	def __init__(self, images):
		self.images = images

	def any(self):
		return len(self.images) > 0

	def kill(self):
		for image in self.images:
			docker_client.remove_image(image, force=True)


class Dokker:
	def __init__(self):
		pass

	def pull(self, image):
		docker_client.pull(image, stream=False)

	def spawn(self, image, **kwargs):
		kwargs.update({
			'detach': True,
			'image': image
		})

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

	def build(self, **kwargs):
		kwargs.update({
			'rm': True,
			'forcerm': True
		})

		for line in docker_client.build(**kwargs):
			yield line

	def purge(self, app):
		self.containers(name=app.name).kill()

		self.images(name=app.image()).kill()