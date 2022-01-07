import sys
from PyQt5.QtCore import Qt, QRect, QTimer
from PyQt5.QtWidgets import *
from Design.MainWin import Ui_MainWindow
from PyQt5.QtGui import QPainter, QPaintEvent, QPen, QMouseEvent, QResizeEvent, QPixmap, QBrush, QKeyEvent, QIcon
from Drawable.NewChildTypeDialog import newChildTypeDialog
from Drawable.EditInteractiveDialog import EditInteractiveDialog
from Drawable.Connection import Connection
from dataclass import dataclass


class MainWindow(QMainWindow):

	def __init__(self, controller):
		QMainWindow.__init__(self)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.controller = controller

		self.drawable_objects = list()
		self.timer = QTimer()
		self.timer.timeout.connect(self.update)
		self.timer.start(50)

		self.original_press_x = -1
		self.original_press_y = -1
		self.cur_pressed_x = -1
		self.cur_pressed_y = -1

		self.pressed = False

		saveAction = QAction('Save', self)
		saveAction.setShortcuts(('Ctrl+S', 'Ctrl+Ы'))
		saveAction.triggered.connect(self.controller.save_objects_into_file)

		openAction = QAction('Open', self)
		openAction.setShortcuts(('Ctrl+O', 'Ctrl+Щ'))
		openAction.triggered.connect(self.controller.load_objects_from_file)

		newFileAction = QAction('New...', self)
		newFileAction.setShortcuts(('Ctrl+N',))
		newFileAction.triggered.connect(self.controller.create_new_document)

		fileMenu = self.ui.menubar.addMenu('&File')
		fileMenu.addAction(newFileAction)
		fileMenu.addAction(saveAction)
		fileMenu.addAction(openAction)

		addBlock = QAction(QIcon('Editor/Design/addBlockIcon.png'), 'Add Block', self)
		addBlock.triggered.connect(lambda: self.controller.create_object(dataclass.BLOCK_TYPE))
		self.ui.toolBar.addAction(addBlock)

		addKindsConnection = QAction(QIcon('Editor/Design/addKindsConIcon.png'), 'Add Kinds Connection\nSelect a block and '
																	 'another element and then press this button', self)
		addKindsConnection.triggered.connect(lambda: self.controller.create_object(dataclass.CONNECTION_KINDS_TYPE))
		self.ui.toolBar.addAction(addKindsConnection)

		addHierarchyConnection = QAction(QIcon('Editor/Design/addHierarchyIcon.png'), 'Add Hierarchy\nSelect a block and '
																		  'another element and then press this button. The first pressed '
																		   'figure will be the parent, the second -- the child.',
										 self)
		addHierarchyConnection.triggered.connect(lambda: self.controller.create_object(dataclass.CONNECTION_HIER_TYPE))
		self.ui.toolBar.addAction(addHierarchyConnection)

		addOrderConnection = QAction(QIcon('Editor/Design/addOrderIcon.png'), 'Add Order\nSelect a block and '
																		  'another element and then press this button',
									 self)
		addOrderConnection.triggered.connect(lambda: self.controller.create_object(dataclass.CONNECTION_NUM_ORDER_TYPE))
		self.ui.toolBar.addAction(addOrderConnection)

		addText = QAction(QIcon('Editor/Design/addTextIcon.png'), 'Add Text', self)
		addText.triggered.connect(lambda: self.controller.create_object(dataclass.SCHEME_TEXT_TYPE))
		self.ui.toolBar.addAction(addText)

		removeObject = QAction(QIcon('Editor/Design/deleteDrawableObject.png'), 'Delete Object', self)
		removeObject.triggered.connect(self.controller.del_drawable_objects)
		self.ui.toolBar.addAction(removeObject)

		addTextEdit = QAction(QIcon('Editor/Design/addInterText.png'), 'Add an interactive Text field', self)
		addTextEdit.triggered.connect(lambda: self.controller.create_object(dataclass.TEXT_INTER_TYPE))
		self.ui.toolBar.addAction(addTextEdit)

		addToggle = QAction(QIcon('Editor/Design/addInterToggle.png'), 'Add an interactive Toggle', self)
		addToggle.triggered.connect(lambda: self.controller.create_object(dataclass.TOGGLE_INTER_TYPE))
		self.ui.toolBar.addAction(addToggle)

		addCombo = QAction(QIcon('Editor/Design/addInterCombo.png'), 'Add an interactive ComboBox', self)
		addCombo.triggered.connect(lambda: self.controller.create_object(dataclass.COMBO_INTER_TYPE))
		self.ui.toolBar.addAction(addCombo)

		self.showMaximized()

	def paintEvent(self, event: QPaintEvent):
		qp = QPainter()
		qp.begin(self)
		qp.setRenderHint(QPainter.Antialiasing)
		qp.setBrush(QBrush(Qt.white, Qt.SolidPattern))
		qp.drawRect(0, 0, self.width(), self.height())
		qp.setBrush(Qt.NoBrush)

		for obj in self.drawable_objects:
			obj.render(qp)

		if self.pressed:
			if not self.selected_objects():
				if self.original_press_x >= 0 and self.original_press_y >= 0:
					if self.cur_pressed_x >= 0 and self.cur_pressed_y >= 0:
						style = Qt.DashDotLine
						color = Qt.darkBlue
						thickness = 2
						qp.setPen(QPen(color, thickness, style))
						qp.drawRoundedRect(QRect(*self.calculate_selection_coords()), 0,
										   0)
		qp.end()

	def calculate_selection_coords(self):
		if -1 not in (self.original_press_x, self.original_press_y, self.cur_pressed_x, self.cur_pressed_y):
			left_corner = min((self.original_press_x, self.cur_pressed_x))
			top_corner = min((self.original_press_y, self.cur_pressed_y))
			height = abs(self.original_press_y - self.cur_pressed_y)
			width = abs(self.original_press_x - self.cur_pressed_x)
			return left_corner, top_corner, width, height

	def mousePressEvent(self, event: QMouseEvent):
		self.pressed = True
		self.original_press_x = event.x()
		self.original_press_y = event.y()
		self.setFocus()

	def mouseMoveEvent(self, event: QMouseEvent):
		if self.pressed:
			self.cur_pressed_x = event.x()
			self.cur_pressed_y = event.y()
			if abs(self.cur_pressed_x - self.original_press_x) >= 10 \
				and abs(self.cur_pressed_y - self.original_press_y) >= 10:
					for i in self.drawable_objects:
						if i.is_selected:
							if not i.is_being_resized:
								i.onDrag(self.cur_pressed_x, self.cur_pressed_y)
							else:
								i.resize(self.cur_pressed_x, self.cur_pressed_y)

	def mouseReleaseEvent(self, event: QMouseEvent):
		clicked = [i for i in self.drawable_objects if i.margins[0] <= event.x() <= i.margins[2]
				   and i.margins[1] <= event.y() <= i.margins[3]]
		selection_borders = self.calculate_selection_coords()
		if selection_borders:
			clicked.extend([i for i in self.drawable_objects if not isinstance(i, Connection) and
							selection_borders[0] < i.pos[0] < selection_borders[2]
							and selection_borders[1] < i.pos[1] < selection_borders[3]])
		if clicked:
			for obj in clicked:
				obj.onClick()
		else:
			for i in self.drawable_objects:
				if i.is_selected:
					i.selectionReset()
					i.is_being_resized = False
			self.setCursor(Qt.ArrowCursor)
			self.controller.create_object(mouse_pos=(event.x(), event.y()))
		self.pressed = False
		self.original_press_x = -1
		self.original_press_y = -1
		self.cur_pressed_x = -1
		self.cur_pressed_y = -1

	def resizeEvent(self, a0: QResizeEvent):
		self.ui.centralwidget.resize(self.width(), self.height())
		self.ui.gridLayout.setGeometry(QRect(0, 0, self.width(), self.height()))
		self.ui.gridLayoutWidget.resize(self.width(), self.height())

	def get_file_path_to_save(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		dialogue = QFileDialog.getSaveFileName(self, 'Saving', options=options)[0]
		if dialogue.endswith('.deltamind'):
			return dialogue
		else:
			return dialogue + '.deltamind'

	def get_file_path_to_open(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		dialogue = QFileDialog.getOpenFileName(self, 'Open...', options=options)[0]
		return dialogue

	def show_message_on_saving(self):
		message = QMessageBox(QMessageBox.NoIcon, 'Saved', 'Your mindmap has been saved.', QMessageBox.Ok, self)
		message.setIconPixmap(QPixmap('Editor/Design/saveIcon.png'))
		message.setDefaultButton(QMessageBox.Ok)
		message.exec_()

	def new_child_and_connection_type_dialog(self):
		dial = newChildTypeDialog(self)
		dial.exec_()
		return dial.new_child_type, dial.new_connection_type

	def keyPressEvent(self, event: QKeyEvent):
		if event.key() == Qt.Key_Delete:
			self.controller.del_drawable_objects()

	def selected_objects(self):
		return [i for i in self.drawable_objects if i.is_selected]

	def show_no_figures_selected_error(self):
		message = QMessageBox(QMessageBox.Critical, 'Error', 'Not enough elements are selected. Select 2 elements, please', parent=self)
		message.show()

	def ask_whether_to_save_current_file(self):
		message = QMessageBox(QMessageBox.Question, 'Save?..', 'Would you like to save the current file?', parent=self)
		message.setStandardButtons(QMessageBox.Cancel | QMessageBox.Discard | QMessageBox.Save)
		message.setDefaultButton(QMessageBox.Save)
		result = message.exec_()
		return result

	def closeEvent(self, event):
		if self.drawable_objects:
			user_choice = self.ask_whether_to_save_current_file()
			if user_choice == QMessageBox.Save:
				self.controller.save_objects_into_file()
				QMainWindow.closeEvent(self, event)
			elif user_choice == QMessageBox.Cancel:
				pass
			else:
				QMainWindow.closeEvent(self, event)

	def inter_edit_dialog(self, inter_obj):
		dial = EditInteractiveDialog(self, inter_obj)
		dial.exec_()
		return dial.new_data


if __name__ == '__main__':

	app = QApplication(sys.argv)
	main_win = MainWindow(None)
	sys.exit(app.exec_())