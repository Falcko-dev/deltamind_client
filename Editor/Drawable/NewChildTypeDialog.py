from PyQt5.QtWidgets import *
from Design.getNewChildTypeDialog import Ui_Dialog
from dataclass import dataclass


class newChildTypeDialog(QDialog):

	def __init__(self, parent):
		QDialog.__init__(self, parent)
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)

		self.new_child_type = -1
		self.new_connection_type = -1
		self.ui.childTypeComboBox.addItem('Блок', dataclass.BLOCK_TYPE)
		self.ui.childTypeComboBox.addItem('Текст', dataclass.SCHEME_TEXT_TYPE)
		self.ui.childTypeComboBox.setPlaceholderText('Тип дочернего элемента')
		self.ui.connectionTypeComboBox.addItem('Иерархия', dataclass.CONNECTION_HIER_TYPE)
		self.ui.connectionTypeComboBox.addItem('Различные виды', dataclass.CONNECTION_KINDS_TYPE)
		self.ui.connectionTypeComboBox.addItem('Порядок', dataclass.CONNECTION_NUM_ORDER_TYPE)
		self.ui.connectionTypeComboBox.setCurrentText('Тип связи')
		self.ui.chooseNewChildTypeButton.clicked.connect(self.set_user_choice)

	def set_user_choice(self):
		type_val = self.ui.childTypeComboBox.currentData()
		conn_val = self.ui.connectionTypeComboBox.currentData()
		self.new_child_type = type_val
		self.new_connection_type = conn_val
		self.accept()

