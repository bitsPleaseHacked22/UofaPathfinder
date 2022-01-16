import PathFinderDialog
from PyQt5.QtWidgets import QMessageBox, QDialog, QApplication
import pyqtgraph as pg
import cv2 as cv
import sys
import csv
import numpy as np
from Graph import Graph

class MainDialog(QDialog):
    def __init__(self, parent=None):
        super(MainDialog, self).__init__(parent)
        # ui initializaation
        self.ui = PathFinderDialog.Ui_PathfinderDialog()
        self.ui.setupUi(self)
        self.mapHolder = pg.ImageItem()
        self.map = cv.imread('./assets/map.png')
        self.map = np.rot90(self.map, k=1, axes=(1,0))
        self.mapHolder.setImage(self.map)
        self.ui.UofaMap.addItem(self.mapHolder)
        self.xCords = []
        self.yCords = []
        self.buildingsDict = dict()
        self.buildingsDictInverse = dict()
        self.buildingNamesPathFinding = []
        self.currentPath = None
        self.clickedObject = None
        with open('./assets/buildingDetails.csv') as csvFile:
            csvReader = csv.reader(csvFile, delimiter=',')
            count = 0
            for row in csvReader:
                if count == 0:
                    count +=1
                    continue
                text = pg.TextItem(row[0], color=(255,0,0), fill=(255,255,255))
                text.setPos(float(row[1]), float(row[2])+10)
                self.ui.UofaMap.addItem(text)
                self.xCords.append(float(row[1]))
                self.yCords.append(float(row[2]))
                self.buildingsDict[row[1]+row[2]] = row[0]
                self.buildingsDictInverse[row[0]] = row[1] + row[2]
                count +=1
        self.pointsObjects = self.ui.UofaMap.plot(self.xCords, self.yCords, pen=None, symbol = 'o', symbolBrush= (255,0,0))
        self.pointsObjects.sigPointsClicked.connect(self.addBuildingName)
    
    def addBuildingName(self, event, point):
        if self.clickedObject != None:
            self.ui.UofaMap.removeItem(self.clickedObject)
            self.clickedObject = None
        p_ellipse = pg.QtGui.QGraphicsEllipseItem(point[0].pos().x() - 10, point[0].pos().y() - 10, 25, 25)  # x, y, width, height
        p_ellipse.setPen(pg.mkPen((0, 0, 0, 255)))
        p_ellipse.setBrush(pg.mkBrush((0, 0, 255)))
        self.ui.UofaMap.addItem(p_ellipse)
        self.clickedObject = p_ellipse
        if self.currentPath != None:
            self.ui.UofaMap.removeItem(self.currentPath)
        x = point[0].pos().x()
        y = point[0].pos().y()
        key = str(int(x)) + str(int(y))
        self.buildingNamesPathFinding.append(self.buildingsDict[key])
        if len(self.buildingNamesPathFinding) == 2:
            # call pathfinding algorithm here
            graph = Graph()
            result = graph.print_result(self.buildingNamesPathFinding[0], self.buildingNamesPathFinding[1])
            xCoords = []
            yCoords = []
            for ele in result:
                coords = self.buildingsDictInverse[ele]
                xCoords.append(int(coords[:3]))
                yCoords.append(int(coords[3:]))
            self.currentPath = self.ui.UofaMap.plot(xCoords, yCoords, pen=pg.mkPen('r', width=3), symbolBrush=(0,0,255))
            self.buildingNamesPathFinding.clear()
            



def main():
    app = QApplication(sys.argv)

    dialog = MainDialog()
    dialog.exec_()
    # app.exec()

main()


