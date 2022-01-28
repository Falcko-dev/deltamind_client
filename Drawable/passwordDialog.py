from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from Design.passwordDialog import Ui_passwordDialog


class PasswordDialog(QDialog):

	def __init__(self, parent, admin: bool):
		QDialog.__init__(self, parent)
		self.ui = Ui_passwordDialog()
		self.ui.setupUi(self)
		if admin:
			self.ui.label.setText('ведите пароль администратора')
		self.ui.enterButton.clicked.connect(self.ok_button_clicked)
		self.result = ''

	def ok_button_clicked(self, event):
		self.result = self.ui.lineEdit.text()
		self.accept()