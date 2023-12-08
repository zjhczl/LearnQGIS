# 导入qgis
from qgis.core import (QgsApplication, QgsProject,
                       QgsVectorLayer)

# Supply path to qgis install location
QgsApplication.setPrefixPath("/usr", True)

# Create a reference to the QgsApplication.  Setting the
# second argument to False disables the GUI.
qgs = QgsApplication([], True)

# Load providers
qgs.initQgis()

# Get the project instance
project = QgsProject.instance()


# Load another project
project.read('/home/zj/share/ARC/111.qgz')
print(project.fileName())


# get the path to the shapefile e.g. /home/project/data/ports.shp
path_to_airports_layer = "/home/zj/share/ARC/yishankou.shp"

# The format is:
# vlayer = QgsVectorLayer(data_source, layer_name, provider_name)

vlayer = QgsVectorLayer(path_to_airports_layer, "Airports layer2", "ogr")
if not vlayer.isValid():
    print("Layer failed to load!")
else:
    project.addMapLayer(vlayer)


project.write()
qgs.exitQgis()
