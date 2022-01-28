from PyQt5.QtCore import QRect

from Design.mapWidget import Ui_mapWidget
from PyQt5.QtWidgets import QWidget


class MapWidget(QWidget):

	def __init__(self, window_master, map_id, map_title, map_author, date, is_on_search_tab):
		QWidget.__init__(self, window_master)
		self.window_master = window_master
		self.ui = Ui_mapWidget()
		self.ui.setupUi(self)
		self.map_id = map_id
		self.ui.mapIdLabel.setText(f'id: {self.map_id}')
		self.ui.mapTitleLabel.setText(map_title.strip('.deltamind'))
		self.ui.mapCreatorNameLabel.setText(map_author)
		self.ui.creatingDateLabel.setText(date)
		self.setMaximumSize(781*4, 91*4)
		self.setMinimumSize(int(781/2), int(91))
		if is_on_search_tab:
			self.ui.uploadButton.deleteLater()
			self.ui.downloadButton.clicked.connect(lambda event: self.window_master.controller.download_map(self.map_id))
			self.ui.forkButton.clicked.connect(lambda event: self.window_master.controller.fork_map(self.map_id))
			self.ui.viewIntersButton.clicked.connect(lambda event: self.window_master.controller.view_inters(self.map_id))
		else:
			self.ui.downloadButton.deleteLater()
			self.ui.viewIntersButton.deleteLater()
			self.ui.forkButton.clicked.connect(lambda event: self.window_master.controller.start_editor(map_title))
			self.ui.uploadButton.clicked.connect(lambda event: self.window_master.controller.upload_map(f'UserMaps/{map_title}'))
		self.show()