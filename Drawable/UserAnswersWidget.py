from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from Design.AnswersWidget import Ui_Form
from PyQt5.QtWidgets import QWidget, QTableWidgetItem


class UsersAnswersWidget(QWidget):

	def __init__(self, answers: list):
		QWidget.__init__(self)
		self.ui = Ui_Form()
		self.ui.setupUi(self)
		elems_ids = sorted(list(set([i['id'] for j in answers for i in j])))
		self.ui.tableWidget.setColumnCount(len(elems_ids) + 1)
		self.ui.tableWidget.setRowCount(len(answers))
		self.ui.tableWidget.setHorizontalHeaderLabels(['Никнейм пользователя'] + [str(i) for i in elems_ids])
		for index, answer in enumerate(answers):
			name_item = QTableWidgetItem(answer[0]['map_author_nick'])
			name_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
			self.ui.tableWidget.setItem(index, 0, name_item)
			for inter_elem in answer:
				if inter_elem['value']:
					cur_column_id = elems_ids.index(inter_elem['id']) + 1
					value_item = QTableWidgetItem(str(inter_elem['value']))
					value_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
					self.ui.tableWidget.setItem(index, cur_column_id,
												value_item)
