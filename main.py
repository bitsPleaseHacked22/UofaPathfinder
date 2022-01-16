import PathFinderDialog
from PyQt5.QtWidgets import QMessageBox, QDialog, QApplication
import pyqtgraph as pg
import cv2 as cv
import sys

class MainDialog(QDialog):
    def __init__(self, parent=None):
        super(MainDialog, self).__init__(parent)
        # ui initializaation
        self.ui = PathFinderDialog.Ui_PathfinderDialog()
        self.ui.setupUi(self)
        self.mapHolder = pg.ImageItem()
        self.map = cv.imread('./assets/map.png')
        self.mapHolder.setImage(self.map)
        self.ui.UofaMap.addItem(self.mapHolder)



def main():
    app = QApplication(sys.argv)

    dialog = MainDialog()
    dialog.exec_()
    # app.exec()

main()


