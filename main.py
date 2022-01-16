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
        self.buildingNamesPathFinding = []
        with open('./assets/buildingDetails.csv') as csvFile:
            csvReader = csv.reader(csvFile, delimiter=',')
            count = 0
            for row in csvReader:
                if count == 0:
                    count +=1
                    continue
                print("row1",row[1])
                text = pg.TextItem(row[0], color=(255,0,0), fill=(255,255,255))
                text.setPos(float(row[1]), float(row[2])+10)
                self.ui.UofaMap.addItem(text)
                self.xCords.append(float(row[1]))
                self.yCords.append(float(row[2]))
                self.buildingsDict[row[1]+row[2]] = row[0]
                count +=1
        print("xcords", self.xCords)
        self.pointsObjects = self.ui.UofaMap.plot(self.xCords, self.yCords, pen=None, symbol = 'o', symbolBrush= (0,255,0))
        self.pointsObjects.sigPointsClicked.connect(self.addBuildingName)
    def addBuildingName(self, event, point):
        x = point[0].pos().x()
        y = point[0].pos().y()
        key = str(int(x)) + str(int(y))
        print(key)
        print('testing: ',self.buildingsDict[key])
        self.buildingNamesPathFinding.append(self.buildingsDict[key])
        if len(self.buildingNamesPathFinding) == 2:
            # call pathfinding algorithm here
            graph = Graph()
            graph.print_result(self.buildingNamesPathFinding[0], self.buildingNamesPathFinding[1])
            self.buildingNamesPathFinding.clear()
            



def main():
    app = QApplication(sys.argv)

    dialog = MainDialog()
    dialog.exec_()
    # app.exec()

main()


