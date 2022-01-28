from dataclass import dataclass
from Drawable.schemeText import schemeText
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPen, QFont
from PyQt5.QtCore import Qt


class Interactive(schemeText):

	def __init__(self, window_master, text: str, size: tuple, pos: tuple, inter_type: str, id_=-1):
		schemeText.__init__(self, window_master, text, size, pos, id_)
		self.inter_type = inter_type
		self.window_master = window_master
		if self.inter_type == dataclass.TEXT_INTER_TYPE:
			# Если заданный тип интерактивки -- кнопка, pet_widget_data дб строкой
			self.__pet_widget = QPlainTextEdit(text, self.window_master)
			self.__pet_widget.textChanged.connect(self.value_changed_event)
		elif self.inter_type == dataclass.TOGGLE_INTER_TYPE:
			self.__pet_widget = QCheckBox(text, self.window_master)
			self.__pet_widget.stateChanged.connect(self.value_changed_event)
		elif self.inter_type == dataclass.COMBO_INTER_TYPE:
			self.__label = QLabel(self.text, self.window_master)
			self.__label.setGeometry(self.pos[0], self.pos[1] - 30, self.size[0], 30)
			self.__label.show()
			# Виджет TextEdit, прописанный в классе schemeText
			self.label.hide()
			self.__pet_widget = QComboBox(self.window_master)
			self.pet_widget_items = []
			self.__pet_widget.currentTextChanged.connect(self.value_changed_event)
		self.__pet_widget.setGeometry(*[i + 5 for i in self.pos], *[i - 5 for i in self.size])
		self.__pet_widget.setMinimumSize(100, 40)
		self.__pet_widget.show()
		self.__edit_button = QPushButton('✎', self.window_master)
		self.__edit_button.setGeometry(self.pos[0] + self.size[0], self.pos[1] + self.size[1] - 30, 30, 30)
		self.__edit_button.setFixedHeight(30)
		self.__edit_button.setFixedWidth(30)
		self.__edit_button.clicked.connect(lambda: self.window_master.controller.edit_interactive(self))
		self.__edit_button.show()

		self.cur_value = None

	def value_changed_event(self):
		if self.inter_type == dataclass.TEXT_INTER_TYPE:
			self.cur_value = self.__pet_widget.toPlainText()
		elif self.inter_type == dataclass.COMBO_INTER_TYPE:
			self.cur_value = self.__pet_widget.currentText()
		elif self.inter_type == dataclass.TOGGLE_INTER_TYPE:
			self.cur_value = self.__pet_widget.isChecked()
		if self.cur_value:
			self.__pet_widget.setStyleSheet('background-color: #36ff79')
		else:
			self.__pet_widget.setStyleSheet('')

	def update_data(self, new_data):
		if self.inter_type == dataclass.COMBO_INTER_TYPE:
			self.pet_widget_items = new_data
		elif self.inter_type == dataclass.TEXT_INTER_TYPE:
			self.text = new_data
			self.__pet_widget.setPlainText(self.text)
		elif self.inter_type == dataclass.TOGGLE_INTER_TYPE:
			self.text = new_data
			self.__pet_widget.setText(self.text)

	def render(self, qp):
		if self.is_selected:
			style = Qt.DashDotLine
			color = Qt.darkBlue
			thickness = 2
			qp.setPen(QPen(color, thickness, style))
			qp.drawRoundedRect(QRect(*self.calculate_stroke_rect()), 0, 0)

		if self.inter_type == dataclass.COMBO_INTER_TYPE:
			self.__label.setText(self.text)
			# Проверяем, не изменил ли контроллер поле pet_widget_items
			current_data = [self.__pet_widget.itemText(i) for i in range(self.__pet_widget.count())]
			if self.pet_widget_items != current_data:
				for _ in range(self.__pet_widget.count()):
					self.__pet_widget.removeItem(0)
				for num, row in enumerate(self.pet_widget_items):
					self.__pet_widget.addItem(row, num)
		elif self.inter_type == dataclass.TEXT_INTER_TYPE:
			self.text = self.__pet_widget.toPlainText()

	def remove(self):
		schemeText.remove(self)
		self.__pet_widget.hide()
		self.__pet_widget.deleteLater()
		self.__edit_button.hide()
		self.__edit_button.deleteLater()
		if self.inter_type == dataclass.COMBO_INTER_TYPE:
			self.__label.hide()
			self.__label.deleteLater()

	def serialize_into_json(self):
		if self.inter_type == dataclass.TOGGLE_INTER_TYPE:
			text = self.__pet_widget.text()
		else:
			text = self.text
		for_return = {'class': self.__class__.__name__,
				'id': self.id_,
				'pos': list(self.pos),
				'size': list(self.size),
				'text': text,
				'inter_type': self.inter_type,
				'value': self.cur_value}
		if self.inter_type == dataclass.COMBO_INTER_TYPE:
			for_return['pet_items'] = self.pet_widget_items
		return for_return

	def resize(self, cur_pressed_x: int, cur_pressed_y: int):
		schemeText.resize(self, cur_pressed_x, cur_pressed_y)
		self.__pet_widget.resize(self.size[0] - 10, self.size[1] - 10)
		self.__edit_button.move(self.pos[0] + self.size[0], self.pos[1] + self.size[1] - 30)
		if hasattr(self, '_Interactive__label'):
			self.__label.move(self.pos[0], self.pos[1] - 30)

	def onDrag(self, x, y):
		schemeText.onDrag(self, x, y)
		self.__pet_widget.move(*self.pos)
		self.__edit_button.move(self.pos[0] + self.size[0], self.pos[1] + self.size[1] - 30)
		if hasattr(self, '_Interactive__label'):
			self.__label.move(self.pos[0], self.pos[1] - 30)

	def setComboItem(self, text):
		if isinstance(self.__pet_widget, QComboBox):
			index = self.__pet_widget.findText(text, Qt.MatchExactly)
			if index != -1:
				self.__pet_widget.setCurrentIndex(index)

	def toggle(self):
		if isinstance(self.__pet_widget, QCheckBox):
			self.__pet_widget.setChecked(True)