import json
import utils

class Dokker:
	def __init__(self, docker_client):
		self.docker_client = docker_client

	def clean(self, app):
		self.clean_containers(self.containers(app))
		self.clean_images(self.images(app))

	def clean_containers(self, containers):
		for container in containers:
			id = container.get('Id')

			self.docker_client.stop(container=id)
			self.docker_client.remove_container(container=id, force=True)

	def clean_images(self, images):
		for image in images:
			self.docker_client.remove_image(image=image, force=True)

	def build(self, build_path, app):
		for line in self.docker_client.build(path=build_path, tag=utils.image_name(app), rm=True, forcerm=True):
			val = ''

			try:
				d = json.loads(line)

				if 'stream' in d:
					val = d['stream']
				elif 'status' in d:
					val = d['status']
				else:
					val = line
			except:
				val = line

			yield val

	def run(self, app):
		container = self.docker_client.create_container(image=utils.image_name(app), detach=True, labels={'im.oldfashion.app': app})

		self.docker_client.start(container)

		info = self.docker_client.inspect_container(container)

		return info['NetworkSettings']['IPAddress']

	def containers(self, app):
		return self.docker_client.containers(quiet=True, filters={'label': utils.container_label(app)})

	def images(self, app):
		return self.docker_client.images(name=utils.image_name(app), quiet=True)
