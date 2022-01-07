from dataclass import dataclass
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPen, QFont
from PyQt5.QtCore import Qt

class schemeText:

	def __init__(self, window_master, text: str, size: tuple, pos: tuple, id_=-1):
		if id_ != -1:
			self.id_ = id_
		else:
			self.id_ = dataclass.FIGURE_LAST_ID
		self.window_master = window_master
		dataclass.FIGURE_LAST_ID += 1

		self.pos = pos
		self.size = size
		self.__calculate_new_margins()
		# Нужны для корректного перемещения
		self.offset_x = -1
		self.offset_y = -1

		self.label = QPlainTextEdit()
		self.label.setGeometry(*pos, *size)
		self.text = text
		if self.text:
			self.label.setParent(self.window_master)
			self.label.hide()
		self.resize_button = QPushButton(text='⇲', parent=self.window_master)
		self.resize_button.setFixedHeight(30)
		self.resize_button.setFixedWidth(30)
		self.resize_button.setGeometry(self.pos[0] + self.size[0], self.pos[1] + self.size[1], 30, 30)
		self.is_selected = False
		self.is_being_resized = False
		self.resize_button.clicked.connect(self.onResizeButtonClick)
		self.resize_button.show()

	def render(self, qp):
		if self.is_selected:
			style = Qt.DashDotLine
			color = Qt.darkBlue
			thickness = 2
			if self.label.isHidden():
				self.label.setPlainText(self.text)
				self.label.show()
		else:
			style = Qt.SolidLine
			color = Qt.black
			thickness = 0
			qp.setFont(QFont('Decorative', 12))
			qp.setPen(QPen(Qt.black, 2, Qt.SolidLine))
			qp.drawText(*self.calculate_stroke_rect(), Qt.AlignCenter, self.text)
		qp.setPen(QPen(color, thickness, style))
		qp.drawRoundedRect(QRect(*self.calculate_stroke_rect()), 0, 0)

	def onResizeButtonClick(self):
		self.is_selected = True
		self.is_being_resized = True
		self.window_master.setCursor(Qt.SizeFDiagCursor)

	def resize(self, cur_pressed_x: int, cur_pressed_y: int):
		if cur_pressed_x > self.pos[0] and cur_pressed_y > self.pos[1]:
			self.size = (cur_pressed_x - self.pos[0], cur_pressed_y - self.pos[1])
			self.__calculate_new_margins()
			self.resize_button.move(self.pos[0] + self.size[0], self.pos[1] + self.size[1])
			self.label.resize(self.size[0], self.size[1])

	def calculate_stroke_rect(self):
		return self.pos[0] - 5, self.pos[1] - 5, self.size[0] + 10, self.size[1] + 10

	def onClick(self):
		if not self.is_selected:
			self.window_master.setCursor(Qt.SizeAllCursor)
			self.is_selected = True

	def selectionReset(self):
		self.text = self.label.toPlainText()
		self.label.hide()
		self.is_selected = False
		self.offset_x = -1
		self.offset_y = -1

	def onDrag(self, cur_pressed_x, cur_pressed_y):
		if self.offset_x == -1 and self.offset_y == -1:
			self.offset_x = self.pos[0] - self.window_master.original_press_x
			self.offset_y = self.pos[1] - self.window_master.original_press_y
			print(f'{"="*10} \n{self}. Current cursor pos: {cur_pressed_x};{cur_pressed_y} \n Current offset: {self.offset_x}; {self.offset_y}')
		self.pos = (cur_pressed_x + self.offset_x, cur_pressed_y + self.offset_y)
		self.__calculate_new_margins()
		self.label.move(*self.pos)
		self.resize_button.move(self.pos[0] + self.size[0], self.pos[1] + self.size[1])

	def remove(self):
		self.label.hide()
		self.label.deleteLater()
		self.resize_button.hide()
		self.resize_button.deleteLater()

	def __calculate_new_margins(self):
		self.margins = [i - 5 for i in self.pos]
		self.margins.extend([self.pos[i] + self.size[i] + 5 for i in (0, 1)])

	def serialize_into_json(self):
		return {'class': self.__class__.__name__,
				'id': self.id_,
				'pos': list(self.pos),
				'size': list(self.size),
				'text': self.text}

	def __str__(self):
		return f'{self.__class__.__name__} #{self.id_}: {self.pos}'
