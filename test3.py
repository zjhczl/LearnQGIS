from qgis.core import (
    QgsApplication,
    QgsProject,
    QgsVectorLayer,
)
from PyQt5.QtGui import QColor

from PyQt5.QtWidgets import QApplication
from qgis.PyQt.QtCore import Qt, QMetaObject, Q_ARG
from qgis.gui import QgsMapCanvas
import threading
import time


def changecolor(canvas):
    def run():
        time.sleep(2)
        print("Change color to red")
        # 这里需要注意的是，所有的GUI更新都应该在主线程中执行
        # 所以我们使用invokeMethod来确保安全地更新GUI
        QMetaObject.invokeMethod(
            canvas, "setCanvasColor", Qt.QueuedConnection, Q_ARG(QColor, Qt.red))
        QMetaObject.invokeMethod(canvas, "refresh", Qt.QueuedConnection)

    # 在新线程中执行延迟操作
    thread = threading.Thread(target=run)
    thread.start()


QgsApplication.setPrefixPath("/usr/share/qgis", True)
qgs = QgsApplication([], True)

# Load providers
qgs.initQgis()
app = QApplication([])

canvas = QgsMapCanvas()
canvas.show()
canvas.setWindowTitle('My Map Canvas2')
canvas.setCanvasColor(Qt.blue)
canvas.enableAntiAliasing(True)
vlayer = QgsVectorLayer('/home/zj/testroad.shp', "Airports layer", "ogr")

if not vlayer.isValid():
    print("Layer failed to load!")

QgsProject.instance().addMapLayer(vlayer)
canvas.setExtent(vlayer.extent())
canvas.setLayers([vlayer])

# 调用改变颜色的函数
changecolor(canvas)

# 启动Qt事件循环
app.exec_()

# 清理QGIS应用实例
qgs.exitQgis()
