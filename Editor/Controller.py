import json
from View import MainWindow
from Model import Model
import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from dataclass import dataclass
from Drawable.schemeText import schemeText
from Drawable.Block import Block
from Drawable.Connection import Connection
from Drawable.Interactive import Interactive


class Controller:

	def __init__(self, filepath=''):
		self.object_is_being_created = -1
		if filepath:
			print('Create the attr fp')
			self.filepath = filepath
		self.app = QApplication(sys.argv)
		self.view = MainWindow(self)
		self.model = Model(self)
		self.load_objects_from_file(filepath)
		self.start_app()

	def save_objects_into_file(self):
		path = self.view.get_file_path_to_save()
		# При нажатии на кнопку Cancel файловый диалог возвращает ".deltamind"
		if path != '.deltamind':
			json_objs = []
			to_save = [i for i in self.view.drawable_objects if i.__class__.__name__ != 'Connection'] + \
					  [i for i in self.view.drawable_objects if i.__class__.__name__ == 'Connection']
			for obj in to_save:
				diction = obj.serialize_into_json()
				json_objs.append(json.dumps(diction))
			self.model.save_object_into_the_file(json_objs, path)
			self.view.show_message_on_saving()

	def load_objects_from_file(self, argpath=''):
		self.create_new_document(ask_to_save=False)
		print('Controller: entered loading')
		if not argpath:
			path = self.view.get_file_path_to_open()
		else:
			path = argpath
			print('Controller: got the path')
		if path:
			# Дополнительная проверка на случай, если пользователь закроет диалог
			jsons = self.model.open_file(path)
			for j_obj in jsons:
				if j_obj['class'] == 'Block':
					new_block = Block(self.view, j_obj['text'], j_obj['size'],
															j_obj['pos'], j_obj['id'], j_obj['parent_id'])
					self.view.drawable_objects.append(new_block)
					new_block.children = j_obj['children']
				elif j_obj['class'] == 'Connection':
					self.view.drawable_objects.insert(0, Connection(self.view, j_obj['text'],
																	(120, 30),
																	[i for i in self.view.drawable_objects if i.id_ == j_obj['parent']][0],
																	[i for i in self.view.drawable_objects if i.id_ == j_obj['child']][0],
																	j_obj['type'],
																	j_obj['id']))
				elif j_obj['class'] == 'schemeText':
					self.view.drawable_objects.append(schemeText(self.view, j_obj['text'], j_obj['size'],
																 j_obj['pos'], j_obj['id']))
				elif j_obj['class'] == 'Interactive':
					inter_obj = Interactive(self.view, j_obj['text'],
																  j_obj['size'], j_obj['pos'], j_obj['inter_type'], j_obj['id'])
					if j_obj['inter_type'] == dataclass.COMBO_INTER_TYPE:
						inter_obj.update_data(j_obj['pet_items'])
						inter_obj.setComboItem(j_obj['value'])
					elif j_obj['inter_type'] == dataclass.TOGGLE_INTER_TYPE:
						if j_obj['value']:
							inter_obj.toggle()
					inter_obj.cur_value = j_obj['value']
					self.view.drawable_objects.append(inter_obj)

			for new_obj in self.view.drawable_objects:
				if isinstance(new_obj, Block):
					for child_id, cur_index in zip(new_obj.children, range(len(new_obj.children))):
						new_obj.children[cur_index] = [i for i in self.view.drawable_objects if i.id_ == child_id][0]
			dataclass.FIGURE_LAST_ID = max([i.id_ for i in self.view.drawable_objects])

	def add_child_to_block(self, parent_block):
		child_type, conn_type = self.view.new_child_and_connection_type_dialog()
		if child_type != -1 and conn_type != -1:
			if child_type == dataclass.BLOCK_TYPE:
				self.view.drawable_objects.append(Block(self.view,
										   'Новый блок',
										   (150, 100),
										   (parent_block.pos[0] + parent_block.size[0] + 10, parent_block.pos[1]),
										   block_parent_id=parent_block.id_))
			elif child_type == dataclass.SCHEME_TEXT_TYPE:
				self.view.drawable_objects.append(schemeText(self.view,
												'Новый текст',
												(150, 100),
												(parent_block.pos[0] + parent_block.size[0] + 10, parent_block.pos[1])))

			parent_block.children.append(self.view.drawable_objects[-1])
			self.view.drawable_objects.insert(0, Connection(self.view, '', (150, 30),
														 parent_block, self.view.drawable_objects[-1], conn_type))

	def del_drawable_objects(self):
		def recursively_find_children(obj_):
			if isinstance(obj_, Block):
				for_return = obj_.children
				if for_return:
					for child in obj_.children:
						for_return += recursively_find_children(child)
					return for_return
			return []

		objects = [i for i in self.view.drawable_objects if i.is_selected and not isinstance(i, Connection)]
		for obj in objects:
			objects += recursively_find_children(obj)
		objects += [i for i in self.view.drawable_objects if isinstance(i, Connection)
					and (i.parent_block in objects or i.child_elem in objects)]
		objects = set(objects)
		for obj in objects:
			for parent_obj in self.view.drawable_objects:
				if isinstance(parent_obj, Block):
					if obj in parent_obj.children:
						parent_obj.children.remove(obj)
			obj.remove()
			self.view.drawable_objects.remove(obj)

	def start_app(self):
		sys.exit(self.app.exec_())

	def create_object(self, obj_type=None, mouse_pos: tuple=()):
		if not mouse_pos:
			if obj_type:
				self.object_is_being_created = obj_type
			if obj_type in (dataclass.CONNECTION_HIER_TYPE, dataclass.CONNECTION_NUM_ORDER_TYPE, dataclass.CONNECTION_KINDS_TYPE):
				try:
					self.view.drawable_objects.insert(0, Connection(self.view, '', (150, 30),
																	self.view.selected_objects()[0],
																	self.view.selected_objects()[1],
																	self.object_is_being_created))
					if isinstance(self.view.selected_objects()[0], Block):
						self.view.selected_objects()[0].children.append(self.view.selected_objects()[1])
					if isinstance(self.view.selected_objects()[1], Block):
						if self.view.selected_objects()[1].block_parent_id == -1:
							self.view.selected_objects()[1].block_parent_id = self.view.selected_objects()[0].id_
				except IndexError:
					self.view.show_no_figures_selected_error()
				self.object_is_being_created = -1
		elif self.object_is_being_created != -1:
			if self.object_is_being_created == dataclass.BLOCK_TYPE:
				self.view.drawable_objects.append(Block(self.view,
														'Новый блок',
														(150, 100),
														mouse_pos))
			elif self.object_is_being_created == dataclass.SCHEME_TEXT_TYPE:
				self.view.drawable_objects.append(schemeText(self.view,
															 'Новый текст',
															 (150, 100),
															 mouse_pos))
			elif self.object_is_being_created in (dataclass.TEXT_INTER_TYPE,
												  dataclass.TOGGLE_INTER_TYPE,
												  dataclass.COMBO_INTER_TYPE):
				self.view.drawable_objects.append(Interactive(self.view, 'Interactive Element', (150, 40), mouse_pos, self.object_is_being_created))
			self.object_is_being_created = -1

	def create_new_document(self, ask_to_save=True):
		if ask_to_save:
			user_choice = self.view.ask_whether_to_save_current_file()
			if user_choice == QMessageBox.Save:
				self.save_objects_into_file()
				dataclass.FIGURE_LAST_ID = 0
				for obj in self.view.drawable_objects:
					obj.remove()
				self.view.drawable_objects = []
			elif user_choice == QMessageBox.Discard:
				dataclass.FIGURE_LAST_ID = 0
				for obj in self.view.drawable_objects:
					obj.remove()
				self.view.drawable_objects = []
		else:
			dataclass.FIGURE_LAST_ID = 0
			for obj in self.view.drawable_objects:
				obj.remove()
			self.view.drawable_objects = []

	def edit_interactive(self, inter_object):
		if isinstance(inter_object, Interactive):
			new_data = self.view.inter_edit_dialog(inter_object)
			if new_data:
				inter_object.update_data(new_data)


if __name__ == '__main__':
	if len(sys.argv) - 1:
		try:
			print('Loading from arg... ' + sys.argv[1])
			C = Controller(sys.argv[1])
		except FileNotFoundError:
			pass
	else:
		C = Controller()