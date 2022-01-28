import requests
import json
import traceback


class Model:

	server_unavailable_code = 'unavailable'
	server_not_found = 'nf'
	wrong_password = 'wp'
	internal_server_error = 'ise'

	def __init__(self, controller):
		self.controller = controller
		with open('config.json', 'r') as FILE:
			cfg_dict = json.load(FILE)
			self.host = cfg_dict['host']
			self.protocol = cfg_dict['protocol']
			self.file_manager = cfg_dict['filemanager']

	def __send_get_req(self, address) -> dict or str or int:
		try:
			response = requests.get(f'{self.protocol}://{self.host}/{address}', timeout=120)
			if response.status_code == 200:
				return response.json()
			elif response.status_code == 404:
				return Model.server_not_found
			elif response.status_code == 403 and response.reason == 'Wrong Password':
				return Model.wrong_password
			elif response.status_code == 500:
				print('Internal server error ' + response.text)
				return Model.internal_server_error
			else:
				print(response.text)
				return response.text
		except requests.exceptions.ConnectionError:
			print(traceback.format_exc())
			pass
			return Model.server_unavailable_code

		except Exception as e:
			print(traceback.format_exc())

	def search_map(self, searchstring: str):
		resp_json = self.__send_get_req(f'search_maps/{searchstring}')
		if isinstance(resp_json, dict):
			return resp_json['maps']
		else:
			return resp_json

	def download_map(self, map_id: str, password: str):
		response = self.__send_get_req(f'get_map/{map_id}/{password}')
		return response

	def upload_map(self, map_code, metadata):
		try:
			json_body = json.dumps({'map_title': metadata['title'],
									'author_nick': metadata['nick'],
									'user_pass': metadata['user_pass'],
									'admin_pass': metadata['admin_pass'],
									'fork': metadata['fork'],
									'map_code': map_code})
			response = requests.post(f'{self.protocol}://{self.host}/create_map', json=json_body, timeout=120)
			if response.status_code == 200:
				return response.text
			elif response.status_code == 404:
				return Model.server_not_found
			elif response.status_code == 403 and response.text == 'Wrong Password':
				return Model.wrong_password
			elif response.status_code == 500:
				print('Internal server error ' + response.text)
		except requests.exceptions.ConnectionError:
			print(traceback.format_exc())
			pass
			return Model.server_unavailable_code

	def view_interactives(self, map_id, admin_password):
		resp_json = self.__send_get_req(f'show_inters/{map_id}/{admin_password}')
		return resp_json

if __name__ == '__main__':
	m = Model(None)
	resp_json = m.search_map('map1')
	pass