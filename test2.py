
from qgis.core import (
    QgsApplication,
    QgsProject,
    QgsVectorLayer,
)
from PyQt5.QtWidgets import QApplication
from qgis.PyQt.QtCore import Qt
from qgis.gui import QgsMapCanvas
import time
import sys
import threading


def changecolor(canvas):
    time.sleep(2)
    print("change")
    canvas.setWindowTitle('My Map Canvas')
    canvas.setCanvasColor(Qt.red)
    canvas.refresh()


QgsApplication.setPrefixPath("/usr/share/qgis", True)
qgs = QgsApplication([], True)

# Load providers
qgs.initQgis()
app = QApplication([])

# print("创建画布")
canvas = QgsMapCanvas()
canvas.show()
canvas.setWindowTitle('My Map Canvas2')
canvas.setCanvasColor(Qt.blue)
canvas.enableAntiAliasing(True)
vlayer = QgsVectorLayer(
    '/home/zj/testroad.shp', "Airports layer", "ogr")

if not vlayer.isValid():
    print("Layer failed to load!")


QgsProject.instance().addMapLayer(vlayer)
canvas.setExtent(vlayer.extent())
canvas.setLayers([vlayer])
time.sleep(3)
app.exec_()


qgs.exitQgis()
