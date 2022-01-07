from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from Design.EditInteractiveDialog import Ui_EditInterDial
from dataclass import dataclass


class EditInteractiveDialog(QDialog):

	def __init__(self, parent, interactive):
		QDialog.__init__(self, parent)
		self.ui = Ui_EditInterDial()
		self.ui.setupUi(self)
		self.interactive = interactive
		if interactive.inter_type == dataclass.COMBO_INTER_TYPE:
			for text in interactive.pet_widget_items:
				self.ui.tableWidget.insertRow(self.ui.tableWidget.rowCount())
				text_item = QTableWidgetItem(text)
				text_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable)
				self.ui.tableWidget.setItem(self.ui.tableWidget.rowCount() - 1, 0, text_item)
			self.ui.tableWidget.insertRow(self.ui.tableWidget.rowCount())
		else:
			self.ui.tableWidget.setEnabled(False)
			self.ui.lineEdit.setText(interactive.text)
		self.new_data = None
		self.ui.saveButton.clicked.connect(self.finish_editing)
		self.ui.tableWidget.itemChanged.connect(self.add_new_row)

	def finish_editing(self, event):
		if self.interactive.inter_type == dataclass.COMBO_INTER_TYPE:
			for_return = []
			for row_num in range(self.ui.tableWidget.rowCount() - 1):
				for_return.append(self.ui.tableWidget.item(row_num, 0).text())
		else:
			for_return = self.ui.lineEdit.text()
		self.new_data = for_return
		self.accept()

	def add_new_row(self, signal_item):
		if self.ui.tableWidget.item(self.ui.tableWidget.rowCount() - 1, 0).text():
			self.ui.tableWidget.insertRow(self.ui.tableWidget.rowCount())
