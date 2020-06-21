import pprint

import controllerLibrary
from maya import cmds

reload(controllerLibrary)
from Qt import QtWidgets, QtCore, QtGui


class ControllerLibraryUI(QtWidgets.QDialog):
    """
    The ControllerLibraryUI is a dialog that lets us to save and import controllers
    """

    def __init__(self):
        super(ControllerLibraryUI, self).__init__()

        self.setWindowTitle('Controller Library UI')

        # The library variable points to an instance of our controller library
        self.library = controllerLibrary.ControllerLibrary()

        # Every time we create a new instance, we will automatically build our UI and populate it
        self.buildUI()
        self.populate()

    def buildUI(self):
        """This method builds UI"""
        # Master UI
        layout = QtWidgets.QVBoxLayout(self)

        # Child horizontal widget
        saveWidget = QtWidgets.QWidget()
        saveLayout = QtWidgets.QHBoxLayout(saveWidget)
        layout.addWidget(saveWidget)

        self.saveNameField = QtWidgets.QLineEdit()
        saveLayout.addWidget(self.saveNameField)

        saveBtn = QtWidgets.QPushButton('Save')
        saveBtn.clicked.connect(self.save)
        saveLayout.addWidget(saveBtn)

        # Parameters for thumbnail size
        size = 64
        buffer = 12

        # Grid list widget to display controller thumbnails
        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.setViewMode(QtWidgets.QListWidget.IconMode)
        self.listWidget.setIconSize(QtCore.QSize(size, size))
        self.listWidget.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.listWidget.setGridSize(QtCore.QSize(size + buffer, size + buffer))
        layout.addWidget(self.listWidget)

        # All the buttons
        btnWidget = QtWidgets.QWidget()
        btnLayout = QtWidgets.QHBoxLayout(btnWidget)
        layout.addWidget(btnWidget)

        importBtn = QtWidgets.QPushButton('Import')
        importBtn.clicked.connect(self.load)
        btnLayout.addWidget(importBtn)

        refreshBtn = QtWidgets.QPushButton('Refresh')
        refreshBtn.clicked.connect(self.populate)
        btnLayout.addWidget(refreshBtn)

        closeBtn = QtWidgets.QPushButton('Close')
        closeBtn.clicked.connect(self.close)
        btnLayout.addWidget(closeBtn)

    def populate(self):
        """Clears the listWidgets and populate library"""
        self.listWidget.clear()
        self.library.find()

        for name, info in self.library.items():
            item = QtWidgets.QListWidgetItem(name)
            self.listWidget.addItem(item)

            screenshot = info.get('screenshot')
            if screenshot:
                icon = QtGui.QIcon(screenshot)
                item.setIcon(icon)

            item.setToolTip(pprint.pformat(info))

    def load(self):
        """Load the currently selected controllers"""
        currentItem = self.listWidget.currentItem()
        if not currentItem:
            return

        name = currentItem.text()
        self.library.load(name)

    def save(self):
        """Save the controller with the given file name"""
        name = self.saveNameField.text()
        if not name.strip():
            cmds.warning("You must give a name!")
            return

        self.library.save(name)
        self.populate()
        self.saveNameField.setText('')


def showUI():
    """
        Shows and returns a handle to the ui
    Returns:
        QDialog
    """
    ui = ControllerLibraryUI()
    ui.show()
    return ui
