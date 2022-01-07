from Drawable.schemeText import schemeText
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPen, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QRect


class Block(schemeText):

	def __init__(self, window_master, text, size, pos, id_=-1, block_parent_id=-1):
		schemeText.__init__(self, window_master, text, size, pos, id_)
		self.block_parent_id = block_parent_id
		# Хранит словари вида {'child_id': id, 'connection_type': str}
		self.children = []
		self.__addChildButton = QPushButton('+', self.window_master)
		self.__addChildButton.setFixedHeight(30)
		self.__addChildButton.setFixedWidth(30)
		self.__addChildButton.setGeometry(self.pos[0] + self.size[0], self.pos[1] + self.size[1] / 2 - 30, 30, 30)
		self.__addChildButton.clicked.connect(lambda: self.window_master.controller.add_child_to_block(self))
		self.__addChildButton.show()

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
			thickness = 1
			qp.setPen(QPen(Qt.black, 2, Qt.SolidLine))
			qp.setFont(QFont('Decorative', 15))
			qp.drawText(*schemeText.calculate_stroke_rect(self), Qt.AlignCenter, self.text)
		qp.setPen(QPen(color, thickness, style))
		if self.block_parent_id != -1:
			qp.drawRect(QRect(*schemeText.calculate_stroke_rect(self)))
			qp.drawRect(QRect(self.pos[0] - 10, self.pos[1] - 10, self.size[0] + 20, self.size[1] + 20))
		else:
			qp.drawRoundedRect(QRect(*schemeText.calculate_stroke_rect(self)), 40, 40)
			qp.drawRoundedRect(QRect(self.pos[0] - 10, self.pos[1] - 10, self.size[0] + 20, self.size[1] + 20), 40, 40)

	def resize(self, cur_pressed_x, cur_pressed_y):
		if cur_pressed_x > self.pos[0] and cur_pressed_y > self.pos[1]:
			schemeText.resize(self, cur_pressed_x, cur_pressed_y)
			self.__addChildButton.move(self.pos[0] + self.size[0], self.pos[1] + self.size[1] / 2 - 30)

	def onDrag(self, cur_x, cur_y):
		for child in self.children:
			child.onDrag(cur_x, cur_y)
		schemeText.onDrag(self, cur_x, cur_y)
		self.__addChildButton.move(self.pos[0] + self.size[0], self.pos[1] + self.size[1] / 2 - 30)

	def serialize_into_json(self):
		return {'class': self.__class__.__name__,
				'id': self.id_,
				'parent_id': self.block_parent_id,
				'children': [i.id_ for i in self.children],
				'pos': list(self.pos),
				'size': list(self.size),
				'text': self.text}

	def remove(self):
		for i in self.children:
			i.remove()
		self.__addChildButton.hide()
		self.__addChildButton.deleteLater()
		schemeText.remove(self)
