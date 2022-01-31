from PyQt5.QtWidgets import *
from Design.uploadDataDialog import Ui_uploadMapInfoDialog


class UploadDataDialog(QDialog):

	def __init__(self, parent):
		QDialog.__init__(self, parent)
		self.ui = Ui_uploadMapInfoDialog()
		self.ui.setupUi(self)
		self.result = {'nick': '',
					   'title': '',
					   'user_pass': '',
					   'admin_pass': ''}
		self.ui.okButton.clicked.connect(self.fill_data)

	def fill_data(self, event):
		self.result['nick'] = self.ui.nicknameLineEdit.text()
		self.result['title'] = self.ui.mapTitleLineEdit.text()
		self.result['user_pass'] = self.ui.userPassLineEdit.text() or '1'
		self.result['admin_pass'] = self.ui.adminPassLineEdit.text() or '1'
		self.accept()