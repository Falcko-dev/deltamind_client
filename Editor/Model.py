import json

class Model:

	def __init__(self, controller):
		self.controller = controller

	def save_object_into_the_file(self, objects: list, file_path):
		with open(file_path, 'w') as FILE:
			FILE.write('')
		with open(file_path, 'a') as FILE:
			for obj in objects:
				FILE.write(obj + ';\n')

	def open_file(self, path):
		with open(path, 'r') as FILE:
			raw_objects = [i for i in FILE.read().split(';\n') if i]
			for_return = []
			for raw_obj in raw_objects:
				for_return.append(json.loads(raw_obj))
		return for_return