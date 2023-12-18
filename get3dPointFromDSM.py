from qgis.core import (
    QgsApplication,
    QgsProject,
    QgsRasterLayer,
    QgsVectorLayer,
    QgsFeature,
    QgsGeometry,
    QgsPoint,
    QgsField,
    QgsFields,
    QgsVectorFileWriter,
    QgsWkbTypes,
    QgsCoordinateReferenceSystem
)
from qgis.PyQt.QtCore import QVariant


QgsApplication.setPrefixPath("/usr/share/qgis", True)
qgs = QgsApplication([], True)
# Load providers
qgs.initQgis()

import sys  # noqa: E402
sys.path.append('/usr/share/qgis/python/plugins')
# 导入processing
import processing  # noqa: E402
# 注册算法
from processing.core.Processing import Processing  # noqa: E402
Processing.initialize()
# from processing.tools import *  # noqa: E402


# Get the project instance
project = QgsProject.instance()
project.read('/home/zj/share/ARC/project/test.qgz')


point_layer_path = "/home/zj/share/ARC/shp/yishankouroad.shp"
raster_layer_path = "/home/zj/share/ARC/dom/yishankou/Production_3_DSM_merge.tif"
output_layer_path = "/home/zj/share/ARC/shp/yishankouroad_3d.shp"
try:
    print("平滑...")
    processing.run("native:smoothgeometry", {'INPUT': '/home/zj/share/ARC/shp/yishankouroad.shp', 'ITERATIONS': 10,
                                             'OFFSET': 0.5, 'MAX_ANGLE': 180, 'OUTPUT': '/home/zj/share/ARC/shp/yishankou_smooth.shp'})
except Exception:
    print("平滑失败")
    qgs.exitQgis()
    sys.exit()

try:
    print("加密...")
    processing.run("native:densifygeometriesgivenaninterval", {
        'INPUT': '/home/zj/share/ARC/shp/yishankou_smooth.shp', 'INTERVAL': 0.0001, 'OUTPUT': '/home/zj/share/ARC/shp/yishankouroad_add.shp'})
except Exception:
    print("平滑失败")
    qgs.exitQgis()
    sys.exit()

print("生成3d点...")
point_layer_path = "/home/zj/share/ARC/shp/yishankouroad_add.shp"

# 加载点矢量图层
point_layer = QgsVectorLayer(point_layer_path, "point layer", "ogr")
if not point_layer.isValid():
    print("点图层加载失败！")
    exit()

# 加载栅格图层
raster_layer = QgsRasterLayer(raster_layer_path, "raster layer")
if not raster_layer.isValid():
    print("栅格图层加载失败！")
    exit()

# 准备三维点矢量图层的字段
fields = QgsFields()
fields.append(QgsField("id", QVariant.Int))
fields.append(QgsField("x", QVariant.Double))
fields.append(QgsField("y", QVariant.Double))
fields.append(QgsField("z", QVariant.Double))

# 创建三维点矢量图层
crs = point_layer.crs().toWkt()
# print(crs)
writer = QgsVectorFileWriter(output_layer_path, "UTF-8", fields,
                             QgsWkbTypes.PointZ, QgsCoordinateReferenceSystem(crs), "ESRI Shapefile")

# 提取高程并创建三维点要素
for feature in point_layer.getFeatures():
    # print(feature)
    # print(feature.geometry())
    # point = feature.geometry().asPoint()
    multiline = feature.geometry().asMultiPolyline()  # 获取 MultiLineString 几何
    for linestring in multiline:
        for point in linestring:

            # 获取栅格图层上该点的高程值
            elevation = raster_layer.dataProvider().sample(point, 1)
            if elevation[1]:
                # 创建三维点
                new_point = QgsPoint(point.x(), point.y(), elevation[0])
                print(str(point)+"-->"+str(new_point))
                new_feature = QgsFeature()
                new_feature.setGeometry(new_point)  # 用三维点创建几何
                new_feature.setFields(fields)
                new_feature.setAttribute("id", feature.id())
                new_feature.setAttribute("x", point.x())
                new_feature.setAttribute("y", point.y())
                new_feature.setAttribute("z", elevation[0])
                writer.addFeature(new_feature)

# 清理和关闭写入器
del writer

# 将新的三维图层添加到QGIS项目中
new_layer = QgsVectorLayer(output_layer_path, "3D point layer", "ogr")
QgsProject.instance().addMapLayer(new_layer)


qgs.exitQgis()
