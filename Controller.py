from View import MainWindow
from Model import Model
import sys
import json
from PyQt5.QtWidgets import QApplication, QVBoxLayout
from PyQt5.QtCore import Qt
from Drawable.MapWidget import MapWidget
import datetime
import os


class Controller:

	def __init__(self):
		self.app = QApplication(sys.argv)
		self.view = MainWindow(self)
		self.model = Model(self)

	def start_app(self):
		self.app.exec_()

	def search_map(self, searchstring):
		maps = self.handle_web_errors(self.model.search_map, None, searchstring)
		if maps:
			lay = QVBoxLayout(self.view)
			for map_ in maps:
				lay.addWidget(MapWidget(self.view, map_['map_id'], map_['title'], map_['author_nick'], map_['creating_date'], True), alignment=Qt.AlignTop)
			self.view.ui.scrollAreaWidgetContents.setLayout(lay)

	def download_map(self, map_id, temporal=False):
		password = self.view.get_password_from_user()
		# Странная проверка равенства на случай, если пароль -- пустая строка
		if password != None:
			map_ = self.handle_web_errors(self.model.download_map, None, map_id, password)
			if map:
				if not temporal:
					FILE = open(f'UserMaps/{map_["title"]}_downloaded_{datetime.datetime.now().strftime("%d-%m-%Y_%H:%M")}.deltamind', 'w')
				else:
					FILE = open('Temporal.deltamind', 'w')
				FILE.write(json.dumps({'author': map_['author_nick'], 'date': map_['creating_date'], 'class': 'meta'}) + ';\n')
				FILE.write(map_['map_code'])
				FILE.close()
			self.view.show_info_message('Ваш файл был загружен')

	def upload_map(self, map_filepath: str, fork_id=-1):
		if map_filepath:
			with open(map_filepath, 'r') as FILE:
				map_code = FILE.read()
			upload_info = self.view.get_upload_data_from_user()
			upload_info['fork'] = fork_id
			if upload_info:
				map_ = self.handle_web_errors(self.model.upload_map, None, map_code, upload_info)
				if map_:
					self.view.show_info_message(f'Ваш файл был загружен на сервер. Id: {map_}')

	def fork_map(self, map_id):
		new_version_map_path = self.view.get_file_path_to_open()
		self.upload_map(new_version_map_path, map_id)

	def view_inters(self, map_id):
		admin_password = self.view.get_password_from_user(admin=True)
		user_answers = self.handle_web_errors(self.model.view_interactives, None, map_id, admin_password)
		if user_answers:
			self.view.show_inters(user_answers)

	def open_file_manager(self, event):
		os.system(f'{self.model.file_manager} {os.getcwd()}/UserMaps')

	def start_editor(self, path=''):
		os.system(f'venv/bin/python Editor/Controller.py UserMaps/"{path}"')

	def create_new_map(self, event):
		os.chdir(os.getcwd())
		self.start_editor()

	def handle_web_errors(self, callback, success_message, *args):
		result = callback(*args)
		if result == self.model.server_unavailable_code:
			self.view.show_crit_message(
				'Нет связи с сервером. Проверьте свое Интернет-соединение или свяжитесь с разработчиками')
		elif result == self.model.server_not_found:
			self.view.show_crit_message(
				'Такой интеллект-карты не существует. Может быть, ее создадите именно вы?')
		elif result == self.model.wrong_password:
			self.view.show_crit_message('Неверный пароль.')
		elif result == self.model.internal_server_error:
			self.view.show_crit_message(
				'На сервере произошел сбой. Пожалуйста, свяжитесь с разработчиками')
		else:
			if success_message:
				self.view.show_info_message(success_message)
			return result


if __name__ == '__main__':
	C = Controller()
	C.start_app()