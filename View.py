import os

from PyQt5.QtCore import QRect, QPoint, QSize, QThread
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import *
from Design.MainWin import Ui_MainWindow
from Drawable.MapWidget import MapWidget
from Drawable.passwordDialog import PasswordDialog
from Drawable.uploadDataDialog import UploadDataDialog
from Drawable.UserAnswersWidget import UsersAnswersWidget


class MainWindow(QMainWindow):

	def __init__(self, controller):
		QMainWindow.__init__(self)
		self.controller = controller
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.ui.searchButton.clicked.connect(self.search_event)
		self.ui.searchMapsScroll.setWidgetResizable(True)
		self.ui.browseMapsFolderButton.clicked.connect(self.controller.open_file_manager)
		self.ui.createNewMapButton.clicked.connect(self.controller.create_new_map)

		self.searchTabContainer = QWidget()
		self.myMapsTabContainer = QWidget()
		self.maps_list = []

		self.showMaximized()

	def resizeEvent(self, a0: QResizeEvent):
		QMainWindow.resizeEvent(self, a0)
		self.ui.centralwidget.resize(self.width(), self.height())
		self.ui.gridLayout.setGeometry(QRect(0, 0, self.width(), self.height()))
		self.ui.gridLayoutWidget.resize(QSize(self.width(), self.height()))
		self.ui.verticalLayout_3.setGeometry(QRect(self.ui.verticalLayout_3.geometry().x(),
												   self.ui.verticalLayout_3.geometry().y(),
												   self.ui.tabWidget.size().width(),
												   self.ui.tabWidget.size().height()))
		self.ui.verticalLayoutWidget_3.resize(self.ui.tabWidget.size())
		self.ui.verticalLayout_2.setGeometry(QRect(self.ui.verticalLayout_3.geometry().x(),
												   self.ui.verticalLayout_3.geometry().y(),
												   self.ui.tabWidget.size().width(),
												   self.ui.tabWidget.size().height()))
		self.ui.verticalLayoutWidget_2.resize(self.ui.tabWidget.size())

	def fill_search_scroll(self, maps):
		for i in self.ui.scrollAreaWidgetContents.layout().count():
			self.ui.scrollAreaWidgetContents.layout().removeItem(self.ui.scrollAreaWidgetContents.layout().itemAt(i))
		for map_ in maps:
			self.ui.scrollAreaWidgetContents.layout().addWidget(MapWidget(self, map_['title'],
																		  map_['author_nick'],
																		  map_['date']))
		self.update()

	def search_event(self):
		search_str = self.ui.searchStringLineEdit.text()
		if search_str:
			self.controller.search_map(search_str)

	def show_crit_message(self, text):
		message = QMessageBox(QMessageBox.Critical, 'Error',
							  text,
							  parent=self)
		message.show()

	def get_password_from_user(self, admin=False):
		dial = PasswordDialog(self, admin)
		dial.exec_()
		return dial.result

	def get_upload_data_from_user(self):
		dial = UploadDataDialog(self)
		dial.exec_()
		if dial.accepted:
			return dial.result

	def ask_user(self, question: str, answer_vars: list):
		dial = QMessageBox()
		dial.setText(question)
		for ans in answer_vars:
			dial.addButton(ans, QMessageBox.AcceptRole)
		dial.exec_()
		user_answer = dial.clickedButton().text()
		return user_answer

	def get_file_path_to_open(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		dialogue = QFileDialog.getOpenFileName(self, 'Open...', options=options)[0]
		return dialogue

	def show_inters(self, inter_elems):
		self.table_window = UsersAnswersWidget(inter_elems)
		self.table_window.show()

	def paintEvent(self, a0):
		QMainWindow.paintEvent(self, a0)
		self.update_my_maps_tab()

	def update_my_maps_tab(self):
		maps_list = [i for i in os.listdir('UserMaps') if i.endswith('.deltamind')]
		if self.maps_list != maps_list:
			self.maps_list = maps_list
			layout = QVBoxLayout()
			for index, map_ in enumerate(maps_list):
				layout.addWidget(MapWidget(self, index, map_, '', '', False))
			self.myMapsTabContainer = QWidget()
			self.myMapsTabContainer.setLayout(layout)
			self.ui.myMapsScrollArea.setWidget(self.myMapsTabContainer)

	def show_info_message(self, text):
		message = QMessageBox(QMessageBox.Information, 'Information',
							  text,
							  parent=self)
		message.show()