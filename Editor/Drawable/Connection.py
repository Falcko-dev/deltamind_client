from Drawable.schemeText import schemeText
from dataclass import dataclass
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPen, QFont, QBrush
from PyQt5.QtCore import Qt


class Connection(schemeText):

	def __init__(self, window_master, text: str, text_rect_size: tuple,
				 parent_block, child_elem, connection_type, id_=-1):
		self.parent_block = parent_block
		self.child_elem = child_elem
		self.type = connection_type
		text_rect_pos = self.calculate_text_rect_pos()
		schemeText.__init__(self, window_master, text, text_rect_size, text_rect_pos, id_)
		self.resize_button.hide()
		self.text = text
		if not self.text:
			labels = {dataclass.CONNECTION_HIER_TYPE: 'Иерархия',
					  dataclass.CONNECTION_KINDS_TYPE: 'Разновидность',
					  dataclass.CONNECTION_NUM_ORDER_TYPE: 'Порядок'}
			self.text = labels[self.type]
		self.label = QLineEdit(self.text, self.window_master)
		self.label.setGeometry(*text_rect_pos, *text_rect_size)
		self.label.show()
		self.label.setParent(self.window_master)

	def render(self, qp):
		self.label.move(*self.calculate_text_rect_pos())
		color = None
		if self.is_selected:
			color = Qt.darkBlue
			if self.label.isHidden():
				self.label.setText(self.text)
		else:
			qp.setFont(QFont('Decorative', 12))
		line_start_pos, line_end_pos = self.calculate_start_end_pos()
		if self.type == dataclass.CONNECTION_HIER_TYPE:
			qp.setPen(QPen(color or Qt.cyan, 3, Qt.SolidLine))
			qp.setBrush(QBrush(Qt.cyan, Qt.SolidPattern))
			qp.drawRect(*line_start_pos, 20, 20)
			qp.setBrush(Qt.NoBrush)
		elif self.type == dataclass.CONNECTION_KINDS_TYPE:
			qp.setPen(QPen(color or Qt.darkGreen, 3, Qt.DashLine))
		elif self.type == dataclass.CONNECTION_NUM_ORDER_TYPE:
			qp.setPen(QPen(color or Qt.darkYellow, 3, Qt.SolidLine))
			qp.setBrush(QBrush(Qt.darkYellow, Qt.SolidPattern))
			qp.drawRect(*line_end_pos, 20, 20)
			qp.setBrush(Qt.NoBrush)
		qp.drawLine(*line_start_pos, *line_end_pos)

	def selectionReset(self):
		self.text = self.label.text()
		self.is_selected = False

	def calculate_start_end_pos(self):
		start_pos = [0, 0]
		end_pos = [0, 0]

		# Расчет высоты привязок
		if self.child_elem.pos[1] in range(self.parent_block.pos[1], self.parent_block.pos[1] + self.parent_block.size[1]):
			start_pos[1] = int(self.parent_block.pos[1] + (self.parent_block.size[1] / 2))
			end_pos[1] = int(self.child_elem.pos[1] + (self.child_elem.size[1] / 2))
		elif self.child_elem.pos[1] < self.parent_block.pos[1]:
			start_pos[1] = self.parent_block.pos[1]
			end_pos[1] = self.child_elem.pos[1] + self.child_elem.size[1]
		else:
			start_pos[1] = self.parent_block.pos[1] + self.parent_block.size[1]
			end_pos[1] = self.child_elem.pos[1]

		# Расчет x-координаты привязок
		if self.child_elem.pos[0] in range(self.parent_block.pos[0] - self.child_elem.size[0],
										   self.parent_block.pos[0] + self.parent_block.size[0]):
			start_pos[0] = int(self.parent_block.pos[0] + (self.parent_block.size[0] / 2))
			end_pos[0] = int(self.child_elem.pos[0] + (self.child_elem.size[0] / 2))
		elif self.child_elem.pos[0] < self.parent_block.pos[0]:
			if self.child_elem.pos[0] + self.child_elem.size[0] > self.parent_block.pos[0]:
				start_pos[0] = int(self.parent_block.pos[0] + self.parent_block.size[0] / 2)
				end_pos[0] = self.child_elem.pos[0] + self.child_elem.size[0]
			elif self.child_elem.pos[0] + self.child_elem.size[0] < self.parent_block.pos[0]:
				start_pos[0] = self.parent_block.pos[0]
				end_pos[0] = self.child_elem.pos[0] + self.child_elem.size[0]
		else:
			start_pos[0] = self.parent_block.pos[0] + self.parent_block.size[0]
			end_pos[0] = self.child_elem.pos[0]

		return start_pos, end_pos

	def calculate_text_rect_pos(self):
		return (self.parent_block.pos[0] + (self.child_elem.pos[0] - self.parent_block.pos[0]) / 2,
						 self.parent_block.pos[1] + (self.child_elem.pos[1] - self.parent_block.pos[1]) / 2)

	def serialize_into_json(self):
		return {'class': self.__class__.__name__,
				'id': self.id_,
				'type': self.type,
				'parent': self.parent_block.id_,
				'child': self.child_elem.id_,
				'text': self.text}

	def remove(self):
		schemeText.remove(self)
